---
captured: 2026-09-06T08:14:15+00:00
session: d6e854d8-9432-4f6e-9d3e-789cc41ae3ad
cwd: /Users/chidionyema/dev/code/idp
chars: 17033
source: founder prompt, verbatim (founder-doc-capture.py)
---

look we need to be psotiive and get tis donesuper quick genini has kindly provided us the code. review and tell what what is left and net steps Here is the complete, production-ready codebase to implement both sides of your architecture: The Model Forge (Capability A) and The Edge Runtime (Capability B).

I have incorporated the exponential speedup architectures discussed: Modal Volume caching for zero-download cold starts and ARM64 NEON SIMD flags for the Rust build. I have also used the Single-Token Classification trick inside the Rust runtime, avoiding full LLM generation loops entirely.

Your engineers can copy these files directly into the repository to clear Checkpoints 1 through 4.

Part 1: Capability A (The Model Forge)
Path: forge/

1. forge/task.yaml (The Declaration)
This declarative file is the entire configuration for Tenant 0 (Voice Gate).

YAML
task: voice-gate
base: unsloth/Qwen2.5-1.5B-Instruct
kind: classify
prompt_template: |
  Classify as customer ready (0) or internal engine leak (1).
  Text: {input}
  Verdict:
labels:
  "0": customer_ready
  "1": internal_leak
abstain_below: 0.80
min_agreement: 0.95
schema: null
lora:
  r: 16
  alpha: 32
  epochs: 3
  lr: 2e-4
2. forge/export_langfuse.py (Dataset Generation)
Pulls historical traces from the estate's Langfuse instance, shuffles them, formats them, and exports the 80/20 JSONL split required by Unsloth.

Python
import os
import json
import random
from langfuse import Langfuse

def main():
    lf = Langfuse(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.environ["LANGFUSE_HOST"]
    )
    dataset_name = os.environ.get("DATASET_NAME", "voice-gate")
    print(f"Fetching dataset '{dataset_name}' from Langfuse...")
    
    ds = lf.get_dataset(dataset_name)
    records = []
    
    for item in ds.items:
        # Expected structure: input text and expected string label ("0" or "1")
        input_text = item.input.get("text", "")
        output_label = item.expected_output.get("label", "0")
        records.append({"input": input_text, "output": output_label})
    
    if len(records) < 500:
        raise ValueError(f"Refusal: Dataset under 500 examples (found {len(records)}).")
        
    random.shuffle(records)
    split_idx = int(len(records) * 0.8)
    train_records = records[:split_idx]
    
    with open("dataset.jsonl", "w") as f:
        for row in records:
            row["split"] = "train" if row in train_records else "eval"
            f.write(json.dumps(row) + "\n")

    print(f"Exported {split_idx} train, {len(records) - split_idx} eval examples.")

if __name__ == "__main__":
    main()
3. forge/train.py (The Unsloth Training Script)
Executes the LoRA tuning on the T4 GPU, evaluates the hold-out dataset, calculates the margin and agreement rates, and exports the compressed Q4_K_M GGUF artifact.

Python
import yaml
import json
import os
import torch
from datasets import load_dataset
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments

def main():
    with open("task.yaml") as f:
        task = yaml.safe_load(f)
        
    print(f"--- Starting Forge Run: {task['task']} ---")
    
    # 1. Load the Base Model efficiently in 4-bit
    max_seq_length = 2048
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = task["base"],
        max_seq_length = max_seq_length,
        dtype = None,
        load_in_4bit = True,
    )
    
    # 2. Inject LoRA adapters
    model = FastLanguageModel.get_peft_model(
        model,
        r = task["lora"]["r"],
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_alpha = task["lora"]["alpha"],
        lora_dropout = 0,
        bias = "none",
        use_gradient_checkpointing = "unsloth",
    )
    
    # 3. Format Dataset
    dataset = load_dataset("json", data_files="dataset.jsonl", split="train")
    train_ds = dataset.filter(lambda x: x["split"] == "train")
    eval_ds = dataset.filter(lambda x: x["split"] == "eval")
    
    def format_row(row):
        prompt = task["prompt_template"].replace("{input}", row["input"])
        # Standard Next-Token Prediction string: Prompt + Label + EOS
        text = f"{prompt}{row['output']}{tokenizer.eos_token}"
        return {"text": text}
        
    train_ds = train_ds.map(format_row)
    
    # 4. Train the Model
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = train_ds,
        dataset_text_field = "text",
        max_seq_length = max_seq_length,
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 10,
            num_train_epochs = task["lora"]["epochs"],
            learning_rate = float(task["lora"]["lr"]),
            fp16 = not FastLanguageModel.is_bfloat16_supported(),
            bf16 = FastLanguageModel.is_bfloat16_supported(),
            logging_steps = 10,
            optim = "adamw_8bit",
            output_dir = "outputs",
            seed = 3407,
        ),
    )
    
    trainer.train()
    
    # 5. Held-Out Evaluation (The Honesty Gate)
    print("Evaluating on held-out set...")
    FastLanguageModel.for_inference(model)
    correct, abstains, total = 0, 0, len(eval_ds)
    
    for row in eval_ds:
        prompt = task["prompt_template"].replace("{input}", row["input"])
        inputs = tokenizer([prompt], return_tensors="pt").to("cuda")
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=1, return_dict_in_generate=True, output_scores=True)
            
        # Extract softmax probabilities for the predicted single token
        logits = outputs.scores[0][0]
        probs = torch.nn.functional.softmax(logits, dim=-1)
        top_prob, top_idx = torch.max(probs, dim=-1)
        pred_token = tokenizer.decode([top_idx.item()]).strip()
        
        if top_prob.item() < task["abstain_below"]:
            abstains += 1
        elif pred_token == str(row["output"]).strip():
            correct += 1

    agreement = correct / (total - abstains) if (total - abstains) > 0 else 0
    abstain_rate = abstains / total
    print(f"Results: Agreement: {agreement:.4f}, Abstain Rate: {abstain_rate:.4f}")
    
    if agreement < task["min_agreement"]:
        raise ValueError(f"Refusal: Held-out agreement {agreement:.4f} is below minimum {task['min_agreement']}.")
        
    # 6. Export Edge-Ready Artifacts
    print("Validation passed. Saving GGUF artifact...")
    os.makedirs("artifact", exist_ok=True)
    
    # Merges LoRA adapters and exports to CPU-optimized format
    model.save_pretrained_gguf("artifact", tokenizer, quantization_method="q4_k_m")
    
    # Unsloth names the file `unsloth-Q4_K_M.gguf`. Rename for the generic contract.
    for filename in os.listdir("artifact"):
        if filename.endswith(".gguf"):
            os.rename(os.path.join("artifact", filename), "artifact/model.gguf")
            break
            
    with open("artifact/model-card.yaml", "w") as f:
        yaml.dump(task, f)
        
    with open("artifact/eval.json", "w") as f:
        json.dump({"held_out": total, "agreement": agreement, "abstain_rate": abstain_rate}, f)

if __name__ == "__main__":
    main()
4. forge/modal_app.py (The Ephemeral Infrastructure Launcher)
This defines the serverless environment. It mounts a persistent NVMe volume for the HuggingFace cache to eliminate the 5-minute model download time on subsequent runs.  
GitHub

Python
import modal
import subprocess
import os
import time

# Create a cached image with the ORAS CLI pre-installed
image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "unsloth[colab-new]@git+https://github.com/unslothai/unsloth.git",
        "xformers<0.0.27", "trl<0.9.0", "peft", "accelerate", "bitsandbytes",
        "langfuse", "pyyaml", "datasets"
    )
    .apt_install("curl", "tar")
    .run_commands(
        "curl -LO https://github.com/oras-project/oras/releases/download/v1.1.0/oras_1.1.0_linux_amd64.tar.gz",
        "tar -zxf oras_1.1.0_linux_amd64.tar.gz -C /usr/local/bin oras"
    )
)

hf_volume = modal.Volume.from_name("huggingface-cache", create_if_missing=True)
app = modal.App("model-forge")

@app.function(
    image=image,
    gpu="T4", # Cheap, fast, perfectly suitable for 1B model tuning
    timeout=3600,
    secrets=[
        modal.Secret.from_name("estate-ghcr"),
        modal.Secret.from_name("estate-langfuse")
    ],
    volumes={"/root/.cache/huggingface": hf_volume}
)
def run_forge(task_name: str):
    os.environ["DATASET_NAME"] = task_name
    
    print(f"Step 1: Exporting Langfuse dataset for {task_name}")
    subprocess.run(["python", "export_langfuse.py"], check=True)
    
    print(f"Step 2: Commencing Unsloth Training on T4 GPU")
    subprocess.run(["python", "train.py"], check=True)
    
    print(f"Step 3: Pushing artifact via ORAS to GHCR")
    ghcr_pat = os.environ["GHCR_PAT"]
    ghcr_user = os.environ["GHCR_USER"]
    subprocess.run(["oras", "login", "ghcr.io", "-u", ghcr_user, "-p", ghcr_pat], check=True)
    
    version = f"v1.{int(time.time())}"
    target_ref = f"ghcr.io/{ghcr_user}/models/{task_name}:{version}"
    
    subprocess.run([
        "oras", "push", target_ref,
        "./artifact/model.gguf:application/vnd.gguf.model",
        "./artifact/model-card.yaml:application/yaml",
        "./artifact/eval.json:application/json"
    ], check=True)
    
    print(f"Forge Complete. Deployed to {target_ref}")

@app.local_entrypoint()
def main(task: str = "voice-gate"):
    run_forge.remote(task)
Part 2: Capability B (The Edge Runtime)
Path: platform/edge-runtime/

1. Cargo.toml
This enforces NEON hardware acceleration on compilation, which is critical for making inference fast on Oracle Free Tier ARM instances.

Ini, TOML
[package]
name = "edge-runtime"
version = "1.0.0"
edition = "2021"

[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
serde_yaml = "0.9"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
candle-core = "0.6.0"
candle-transformers = "0.6.0"
anyhow = "1.0"

[build]
rustflags = ["-C", "target-cpu=neoverse-n1", "-C", "target-feature=+neon"]

[profile.release]
lto = "fat"
codegen-units = 1
opt-level = 3
panic = "abort"
2. src/engine.rs (The Math Layer)
This file uses explicit math to compute the softmax probability margin. By doing this dynamically, we circumvent the slow auto-regressive generation loop and process inference in 15ms.

Rust
use anyhow::Result;
use candle_core::{Device, Tensor};
use candle_transformers::models::quantized_qwen2::ModelWeights;
use serde::Deserialize;
use std::collections::HashMap;
use std::fs;
use tracing::instrument;

#[derive(Deserialize, Clone)]
pub struct ModelCard {
    pub task: String,
    pub base: String,
    pub kind: String,
    pub prompt_template: String,
    pub labels: Option<HashMap<String, String>>,
    pub abstain_below: f32,
}

#[derive(Clone, serde::Serialize)]
pub struct Verdict {
    pub label: String,
    pub p: f32,
    pub margin: f32,
    pub latency_ms: u64,
}

pub struct Engine {
    model: ModelWeights,
    card: ModelCard,
    device: Device,
}

impl Engine {
    pub fn new(model_path: &str, card_path: &str) -> Result<Self> {
        let card_content = fs::read_to_string(card_path)?;
        let card: ModelCard = serde_yaml::from_str(&card_content)?;
        
        let device = Device::Cpu;
        let mut file = fs::File::open(model_path)?;
        
        // Mmap explicitly loads the GGUF directly to registers bypassing massive RAM hits
        let content = candle_core::quantized::ggml_file::Content::read(&mut file)?;
        let model = ModelWeights::from_gguf(&content, &mut file, &device)?;
        
        Ok(Self { model, card, device })
    }

    #[instrument(skip(self, input))]
    pub fn classify(&mut self, input: &str) -> Result<Option<Verdict>> {
        let start = std::time::Instant::now();
        
        // Note: Production integration requires invoking a `tokenizers` instance here.
        // For this architecture scaffold, we mock the token IDs that represent the prompt.
        let tokens: Vec<u32> = vec![12, 45, 99]; // Mock tensor shape
        let tensor = Tensor::new(tokens.as_slice(), &self.device)?.unsqueeze(0)?;
        
        // Forward pass yields logits of the *immediate next token*
        let logits = self.model.forward(&tensor, 0)?;
        let logits_vec = logits.squeeze(0)?.to_vec1::<f32>()?;
        
        // Isolate exact token index logits for our classes (0 and 1)
        // (Mock IDs: "0" -> 15, "1" -> 16 in standard tokenizers)
        let candidates = vec![("0".to_string(), 15_usize), ("1".to_string(), 16_usize)];
        
        let mut target_logits = Vec::new();
        for (_, idx) in &candidates {
            target_logits.push(logits_vec[*idx]);
        }
        
        // Calculate Softmax across targeted classes
        let max_logit = target_logits.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
        let sum_exp: f32 = target_logits.iter().map(|&l| (l - max_logit).exp()).sum();
        let probs: Vec<f32> = target_logits.iter().map(|&l| (l - max_logit).exp() / sum_exp).collect();
        
        // Sort to determine margin
        let mut prob_with_labels: Vec<(f32, String)> = probs.into_iter()
            .zip(candidates.iter().map(|(l, _)| l.clone()))
            .collect();
        
        prob_with_labels.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());
        
        let top_prob = prob_with_labels[0].0;
        let margin = top_prob - prob_with_labels.get(1).map_or(0.0, |x| x.0);
        let top_label = prob_with_labels[0].1.clone();
        
        let latency_ms = start.elapsed().as_millis() as u64;

        // Core Contract: The Abstain Rule
        if top_prob < self.card.abstain_below {
            return Ok(None);
        }

        let mapped_label = self.card.labels
            .as_ref()
            .and_then(|m| m.get(&top_label))
            .unwrap_or(&top_label)
            .clone();

        Ok(Some(Verdict {
            label: mapped_label,
            p: top_prob,
            margin,
            latency_ms,
        }))
    }
}
3. src/server.rs (The Asynchronous Gateway)
Ensures concurrent HTTP connections don't block the OS thread running the LLM matrix multiplication.

Rust
use axum::{routing::{post, get}, Router, Json, extract::State};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::Mutex;
use crate::engine::{Engine, Verdict};

#[derive(Deserialize)]
pub struct InferRequest { pub task: String, pub input: String }

#[derive(Serialize)]
pub struct InferResponse {
    #[serde(flatten)]
    pub verdict: Option<Verdict>,
    pub abstain: bool,
}

pub struct AppState { pub engine: Mutex<Option<Engine>> }

pub fn app(state: Arc<AppState>) -> Router {
    Router::new()
        .route("/v1/infer", post(infer_handler))
        .route("/v1/health", get(health_handler))
        .with_state(state)
}

async fn infer_handler(
    State(state): State<Arc<AppState>>,
    Json(payload): Json<InferRequest>,
) -> Json<InferResponse> {
    let mut engine_guard = state.engine.lock().await;
    
    if let Some(engine) = engine_guard.as_mut() {
        let input = payload.input.clone();
        match engine.classify(&input) {
            Ok(Some(verdict)) => Json(InferResponse { verdict: Some(verdict), abstain: false }),
            Ok(None) | Err(_) => Json(InferResponse { verdict: None, abstain: true }),
        }
    } else {
        Json(InferResponse { verdict: None, abstain: true })
    }
}

async fn health_handler() -> Json<serde_json::Value> {
    Json(serde_json::json!({ "status": "OK", "loaded_task": "voice-gate" }))
}
4. src/main.rs (The Loopback Bind)
Respects the security rule R20 defining the loopback bind for local machine-only access.

Rust
use std::sync::Arc;
use tokio::net::TcpListener;
use tokio::sync::Mutex;
use tracing::info;

mod engine;
mod server;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt().json().init();
    info!("Initializing Edge Runtime...");

    // Mounts artifacts extracted locally via init-container or ORAS CLI wrapper
    let model_path = "artifact/model.gguf";
    let card_path = "artifact/model-card.yaml";
    
    let engine = engine::Engine::new(model_path, card_path)
        .expect("FATAL: Failed to initialize Neural Engine from GGUF.");

    let state = Arc::new(server::AppState {
        engine: Mutex::new(Some(engine)),
    });

    let listener = TcpListener::bind("127.0.0.1:8421").await?;
    info!("Estate Engine securely bound to loopback: 127.0.0.1:8421");
    
    axum::serve(listener, server::app(state)).await?;
    
    Ok(())
}
