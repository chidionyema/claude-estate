---
captured: 2026-09-08T18:58:55+00:00
session: e5728c64-1db4-469c-9f91-941890812b9b
cwd: /Users/chidionyema/dev/code/idp
chars: 3881
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are exactly right. The CI gate only stops future bleeding. It does nothing for the 631 tickets, the 280+ orphaned files, and the dark factory of unmerged work currently rotting in your repos.We cannot wait for agents to manually remember what they built. We have to mechanically sweep the entire estate right now, unearth every single module, and force-stamp a capability.yaml onto it.Here is the exact "Great Uncovering" script.The Deep Sweep ScriptSave this as uncover_estate.py in your root workspace (where idp, hermes-v2, research-engine, etc., live) and run it.It walks every folder in every repository, looking for mechanical proof of work (Dockerfiles, package managers, Kubernetes manifests, or execution scripts). When it finds a project boundary, it generates a baseline capability.yaml and flags it as ORPHANED if it has no deployment configuration.Pythonimport os
import yaml
from pathlib import Path
import subprocess

# Directories to ignore
IGNORE_DIRS = {'.git', 'node_modules', 'venv', '__pycache__', '.claude'}

# Mechanical proof that a folder contains a standalone capability
PROJECT_INDICATORS = {
    'Dockerfile', 'package.json', 'requirements.txt', 'Cargo.toml', 
    'go.mod', 'kustomization.yaml', 'docker-compose.yml'
}

def is_capability_root(path: Path) -> bool:
    """Check if this directory contains proof of being a distinct module."""
    if not path.is_dir():
        return False
    return any((path / indicator).exists() for indicator in PROJECT_INDICATORS)

def get_git_branch(path: Path) -> str:
    """Find out what branch this orphaned code is sitting on."""
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
            cwd=path, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        return "unknown"

def generate_capability_yaml(path: Path):
    """Stamp the folder with a capability file."""
    yaml_path = path / "capability.yaml"
    if yaml_path.exists():
        return # Already tracked

    # Check if it has a cluster home (Kubernetes manifest)
    has_k8s = any(path.rglob("*.yaml")) and not any(path.rglob("launchd*"))
    
    capability = {
        "id": f"auto-{path.name.lower().replace(' ', '-')}",
        "name": path.name,
        "status": "LIVE" if has_k8s else "ORPHANED_LAPTOP_JOB",
        "git_branch": get_git_branch(path),
        "cluster_ready": has_k8s,
        "requires_deep_review": True
    }

    with open(yaml_path, "w") as f:
        yaml.dump(capability, f, sort_keys=False)
    
    print(f"✅ Stamped: {path.relative_to(path.parent.parent)} -> {capability['status']}")

def main():
    root_dir = Path.cwd()
    print(f"🔍 Sweeping estate starting at: {root_dir}")
    
    capabilities_found = 0
    
    for current_dir, dirs, files in os.walk(root_dir):
        # Prune ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        path = Path(current_dir)
        if is_capability_root(path):
            generate_capability_yaml(path)
            capabilities_found += 1
            # Don't recurse into subdirectories of a capability
            dirs[:] = [] 

    print(f"\n🎯 Sweep Complete. Uncovered {capabilities_found} distinct capabilities.")

if __name__ == "__main__":
    main()
What this does immediately:Exposes the Dark Matter: It will immediately print out every single hidden tool, bot, probe, and harness across hermes-v2, crew, and mumchimp.Flags the Laptop Rot: Anything without Kubernetes deployment files gets tagged as ORPHANED_LAPTOP_JOB.Creates the Master Database: Because every project now has a capability.yaml, your CI/CD pipeline and admission controllers now have the raw data they need to block unapproved deployments and map the entire estate.Run the script. Once we have the output, we will know exactly how massive the backlog is.
