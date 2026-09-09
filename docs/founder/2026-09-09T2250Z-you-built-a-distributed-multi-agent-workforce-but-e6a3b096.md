---
captured: 2026-09-09T22:50:23+00:00
session: a941270d-843c-40b9-9481-9f198a8612f1
cwd: /Users/chidionyema/dev/code/idp
chars: 3061
source: founder prompt, verbatim (founder-doc-capture.py)
---

You built a distributed, multi-agent workforce, but you accidentally gave them a single brain stem. Because every agent relies on litellm.llm.svc:4000 for credential surrogation (so they don't hold raw API keys), the moment that one pod choked on a tracing error, your entire company was paralyzed.A single configuration error in one telemetry tool took down 90% of your workforce for hours. That is unacceptable for an elite estate.To make sure your crew never goes completely dark again, you have to eliminate LiteLLM as a Single Point of Failure (SPOF). Here is how you build an "Unkillable Crew" architecture.The "Lifeboat" Architecture (Dual-Gateway Failover)Right now, your agents have one hardcoded route to the models. If that route dies, they throw an exception and crash. You must give them a Lifeboat—a secondary gateway that lives in a completely different failure domain.1. The Primary Route (The Oracle Cluster)Target: [http://litellm.llm.svc:4000](http://litellm.llm.svc:4000)Role: The fast, internal, primary router. It handles 99% of traffic, logs to your local database, and uses the internal cluster network.2. The Lifeboat Route (The Serverless Edge)Target: A hyper-lightweight secondary gateway hosted outside your Oracle cluster entirely (e.g., Cloudflare AI Gateway, Google Cloud Run, or Vercel).Role: It holds a duplicate set of read-only fallback keys. It has no database, no SigNoz tracing, and no complex configuration. It is a dumb, bulletproof proxy.3. The Agent Brain (Client-Side Failover)You update the base class that every agent in your crew uses to communicate. You wrap their LLM calls in an automatic, invisible failover loop.If the agent gets a 504 Timeout or Connection Refused from the primary cluster router, it does not crash. It automatically silently retries against the external Lifeboat.Python# The logic injected into every agent's base client
try:
    # Try the primary internal router first (Fast, logged, internal)
    response = call_llm(base_url="http://litellm.llm.svc:4000", prompt=task)
except (TimeoutError, ConnectionError, HTTP504Error):
    logging.warning("⚠️ Primary router down. Failing over to external Lifeboat.")
    # The cluster is on fire, route out to the serverless fallback
    response = call_llm(base_url="https://lifeboat-llm.mumchimp.com", prompt=task)
Why This is Exponentially BetterSurvives Network Partitions: If Oracle OKE breaks pod-to-pod routing again, the agents will just use public egress to hit the Cloudflare Lifeboat and keep working.Survives Bad Configs: If a rogue PR introduces a broken callback into your main LiteLLM config, it only breaks the primary router. The Lifeboat is immutable and stays up.Zero-Trust Maintained: The agents still do not hold raw Anthropic or DeepSeek keys. They just hold a single internal JWT that authenticates them to both gateways.You protect the Medic (Otto) with the Mac Silicon backdoor, and you protect the Crew with the Serverless Lifeboat. That guarantees your workforce survives even if the entire Oracle control plane melts down.
