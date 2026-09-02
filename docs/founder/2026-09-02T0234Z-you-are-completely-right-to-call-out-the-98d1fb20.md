---
captured: 2026-09-02T02:34:09+00:00
session: 54539261-20a7-4289-a144-e9265f1b0c43
cwd: /Users/chidionyema/dev/code/idp/.wt-eye-breaker
chars: 1526
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are completely right to call out the friction. I am replacing one prompt (Metabase's setup) with two prompts (the gateway login plus a Google SSO login). That is terrible architecture and a violation of extreme asymmetry.Here is exactly what went wrong and how we fix it.The Stupidity: Double LoginRight now, you have a front door (the cluster gateway) that uses OAuth2-Proxy to check your identity. But because Metabase (the free version) doesn't natively speak to OAuth2-Proxy, my previous solution forced you to log in again via Google once you got through the front door.That is friction. That is a bespoke hack.The Fix: Header-Based Trust (The Seamless SSO)We can eliminate the second login entirely using the gateway we already have.When you log into the cluster gateway (OAuth2-Proxy), it verifies you. Once verified, it passes the traffic downstream to Metabase.We can configure the gateway to inject a secure HTTP header (e.g., X-Forwarded-Email: founder@company.com) into that downstream traffic.We then tell Metabase to trust the gateway. We configure Metabase to read that header and automatically log you in, instantly.The Zero-Friction OutcomeYou hit the Metabase URL.If you aren't logged into the cluster, you see one Google login screen (the front door).Once through, you are instantly inside the Metabase dashboard. No second login. No manual setup wizard.This works for Metabase, SigNoz, Backstage, and any other internal tool. You authenticate once at the edge, and the cluster physics handles the rest.
