---
captured: 2026-09-06T03:10:09+00:00
session: 8d04d4f4-9226-4a98-ac41-37c887c03441
cwd: /Users/chidionyema/dev/code/idp
chars: 4341
source: founder prompt, verbatim (founder-doc-capture.py)
---

To ensure PR #1954 fully resolves these failure modes without introducing silent regressions or secret leaks, verify the implementation against the three specific mechanics before merging:

---

### 1. Credential Variable Injection vs. Upstream Limitation

Because `0.2.71` hardcodes `process.env.GITHUB_TOKEN` and lacks native `*_FILE` resolution, mounting secrets as files will fail unless an entrypoint wrapper bridges them.

* **Trap to avoid:** Mapping secrets directly to pod `env` in the manifest exposes raw credentials in `kubectl describe pod` and container metadata.
* **Correct pattern:** Keep the tmpfs secret volume projection, and wrap the container entrypoint to read the files into environment memory immediately before starting the Node process:
```sh
#!/bin/sh
set -eu
[ -f /var/run/secrets/github/token ] && export GITHUB_TOKEN="$(cat /var/run/secrets/github/token)"
[ -f /var/run/secrets/linear/api_token ] && export LINEAR_API_TOKEN="$(cat /var/run/secrets/linear/api_token)"
[ -f /var/run/secrets/linear/webhook_secret ] && export LINEAR_WEBHOOK_SECRET="$(cat /var/run/secrets/linear/webhook_secret)"
[ -f /var/run/secrets/github/webhook_secret ] && export GITHUB_WEBHOOK_SECRET="$(cat /var/run/secrets/github/webhook_secret)"
exec node dist/index.js "$@"

```


* **Verification:** Check container startup logs for `transport: proxy` warnings. When secrets are recognized, Cyrus logs signature verification initialization instead of falling back to unauthenticated proxy mode.

---

### 2. Seeding `/repo` Ahead of GitService

`emptyDir` creates a bare filesystem. Because Cyrus's `GitService.js` expects initialized repositories upon startup rather than cloning them on the fly, `/repo` must be hydrated beforehand.

* **Implementation check:** Ensure an `initContainer` handles repo initialization or cloning using the mounted credentials:
```yaml
initContainers:
  - name: seed-repos
    image: alpine/git:latest
    volumeMounts:
      - name: repos
        mountPath: /repo
      - name: github-token
        mountPath: /var/run/secrets/github
        readOnly: true
    command: ["/bin/sh", "-c"]
    args:
      - |
        set -eu
        TOKEN=$(cat /var/run/secrets/github/token)
        # Clone or initialize each required repository into /repo/<name>

```


* **Verification:** Exec into the running pod and run `git -C /repo/<name> status`. It must return clean working trees rather than `fatal: not a git repository`.

---

### 3. Resolving the `subPath` Mount Permission Trap

When a `subPath` directory does not exist on the underlying volume, the Kubelet creates it on the host as `root:root (0755)`. A non-root container user (`UID 1000`) will immediately crash with `EACCES` when attempting to write subdirectories like `.cyrus/mcp-configs`.

* **Option A (Cleanest):** Avoid `subPath` for the home directory and mount a dedicated PVC or `emptyDir` directly at `/var/lib/cyrus`.
* **Option B (If sharing the volume):** Add an `initContainer` running as root (`runAsUser: 0`) to pre-create the directory structure and hand over ownership:
```yaml
initContainers:
  - name: fix-permissions
    image: busybox:musl
    securityContext:
      runAsUser: 0
    volumeMounts:
      - name: cyrus-data
        mountPath: /var/lib/cyrus
    command: ["sh", "-c", "mkdir -p /var/lib/cyrus/.cyrus/mcp-configs && chown -R 1000:1000 /var/lib/cyrus"]

```


* **Option C:** Set `pod.spec.securityContext.fsGroup = 1000` so mounted volume permissions default to the container's group.
* **Verification:** Run `kubectl get pod -l app=cyrus -o jsonpath='{.items[*].status.containerStatuses[*].state}'`. The container status must read `running` with zero restart counts.

---

### Live Proof Protocol

Once #1954 merges and deploys:

1. **Test signature rejection:** Send an unsigned POST request to the Linear/GitHub webhook endpoint. It must return `401 Unauthorized` / `Signature mismatch` rather than `200 OK` (which was the proxy-mode defect).
2. **Inspect filesystem write capability:** Verify Cyrus generated its MCP configs by inspecting the directory:
```bash
kubectl exec deploy/cyrus -- ls -la /var/lib/cyrus/.cyrus/mcp-configs

```


3. **Capture real webhook receipt:** Tail the pod logs during a test Linear webhook dispatch to confirm full end-to-end receipt without permission or git context errors.
