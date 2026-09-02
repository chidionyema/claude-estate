---
captured: 2026-09-02T17:47:44+00:00
session: 54539261-20a7-4289-a144-e9265f1b0c43
cwd: /Users/chidionyema/dev/code
chars: 3427
source: founder prompt, verbatim (founder-doc-capture.py)
---

e reason this keeps happening is a structural flaw in how your image automation bot interacts with your deployment manifests (likely Flux Image Update Automation or a custom script).

When an automation bot is configured to bump an image tag inside a large Kubernetes manifest or a HelmRelease, it often uses a naive text-replacement regex or rewrites the entire file based on an outdated template. In doing so, it treats your hand-crafted replicas, anti-affinity rules, and telemetry blocks as "extraneous" and wipes them out.

To solve this permanently and stop the bleeding, you have to decouple the image tag from the rest of your infrastructure configuration. There are two ways to do this:

Solution 1: Use Precise Marker Comments (The Native Flux Way)
If you are using Flux Image Automation, you must stop the bot from rewriting whole files by using strict marker comments.

Instead of letting the bot guess what to change, restrict it to a single-line inline marker. The bot will parse the file, find the comment key, and rewrite only the string immediately preceding it, leaving your HA settings, replicas, and telemetry untouched.

Inside your HelmRelease or Deployment manifest:
YAML
spec:
  values:
    image:
      repository: my-registry/my-app
      tag: 1.0.0 # {"$imagepolicy": "flux-system:my-app-policy"}
    # --- EVERYTHING BELOW THIS REMAINS UNTOUCHED BY THE BOT ---
    replicaCount: 2
    affinity:
      podAntiAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
                - key: app
                  operator: In
                  values: ["my-app"]
            topologyKey: kubernetes.io/hostname
    telemetry:
      enabled: true
Because the automation controller is bound exclusively to that single line marked by {"$imagepolicy": ...}, it physically cannot overwrite your replicas or telemetry blocks on commit.

Solution 2: Separate State via Kustomize Overlays (The Enterprise Way)
If your automation bot is too aggressive and keeps rewriting files it shouldn't, stop letting it touch Helm charts or base templates altogether. Split your repository into a strict base-and-overlay pattern using Kustomize:

base/ directory (Immutable): Contains your stable HelmRelease or Deployment with all your HA settings, replicas, and telemetry blocks. Image automation has zero permissions to touch this folder.

overlays/staging/ or overlays/prod/ (Mutable): Contains a lightweight kustomization.yaml where the image automation bot is allowed to run.

The Kustomize Overlay Patch (kustomization.yaml):
Instead of modifying the core deployment file, the automation bot targets a tiny patch file:

YAML
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- ../../base
images:
  - name: my-registry/my-app
    newTag: 1.0.3  # <--- The bot ONLY updates this single line in this isolated file
The Immediate Action
Check your image automation configuration (e.g., ImageUpdateAutomation resource or custom GitHub Action bot).

If it is pointing to raw, monolithic configuration files, restrict its target path to a dedicated file containing only image tags, or implement the inline # {"$imagepolicy": ...} comment markers shown in Solution 1.

Once constrained, the bot will change the tag, your HA/telemetry settings will remain safe, and your agents will never have to waste another minute restoring them.
