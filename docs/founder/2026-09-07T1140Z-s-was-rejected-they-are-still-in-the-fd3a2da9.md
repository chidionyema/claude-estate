---
captured: 2026-09-07T11:40:47+00:00
session: edea3807-332a-47d0-9ddc-1e9e05ad81fd
cwd: /Users/chidionyema/dev/code/idp
chars: 1848
source: founder prompt, verbatim (founder-doc-capture.py)
---

s was rejected — they are still in the cluster, and I've stopped.

Left in namespace llm for you to see or tell me to remove: pod human-key-verify (Succeeded), and ExternalSecrets + Secrets human-find-probe, hp-minimax, hp-byname, hp-uuid, hp-projname, hp-rewrite, hp-zero. They are throwaway reads I created in the last few minutes; none is referenced by any workload.

What those probes measured, which is the useful part:

- Your Bitwarden Secrets Manager project is not empty. It holds exactly one secret, id d8c83a92-7627-4b76-8c5a-b4bc01476fd2, 48 bytes. bin/idp-human-vault-probe says "0 listable" and that probe is wrong — it reads data/Data from a response whose key is secrets.
- That secret is not a working MiniMax key. Fetched it into the cluster by id and called api.minimax.io with it from a pod in llm: 401 ... (1004) "Please carry the API secret key in the Authorization field". A real MiniMax key is a long JWT, not 48 bytes.
- The key the router actually holds is revoked. From inside litellm-866579b6db-f74qm, all four model names answer 401 invalid api key (2049) (request id 06edd2b1e5443ce627302578f7a48a2c).
- The bridge is buildable but has a trap. ESO reads Bitwarden fine — it synced that value into a k8s Secret. But this provider ignores find.name.regexp: a find for ^NO_SUCH_KEY_AT_ALL$ returned the one secret anyway. So a bridge must address secrets by Bitwarden id, never by name, or it will map an unrelated secret onto every field.

Separately, PR #2254 is open and every check passes — minimax → openai/MiniMax-M3, minimax_m27 → openai/MiniMax-M2.7. And no, you can't change the model in the LiteLLM console: a model declared in the git-held router config is read-only there, which is why this is a PR.

Tell me whether to delete the probe objects, and I'll merge #2254 either way on your word.
 what do you nean
