---
captured: 2026-09-02T02:36:53+00:00
session: 54539261-20a7-4289-a144-e9265f1b0c43
cwd: /Users/chidionyema/dev/code/idp/.wt-eye-breaker
chars: 1684
source: founder prompt, verbatim (founder-doc-capture.py)
---

I traded a 5-second password prompt for a 15-minute nightmare navigating the Google Cloud Console's labyrinth of OAuth consent screens and API credentials. That is a massive downgrade in the founder experience. You are right to call it out.

The root of the problem is that Metabase's free tier is actively fighting our architecture. They intentionally paywall the seamless header-based auth (JWT/SAML) to force companies into their enterprise tier.

If the Google Console UI is a dealbreaker (and for a B2B product, it absolutely is), we have two ways to achieve zero friction right now:

Option 1: The Client-ID Reuse (If Gateway = Google)
If your existing cluster gateway (OAuth2-Proxy) is already using Google to authenticate you at the front door, we don't need to touch the Google Console at all.
We can simply instruct the Kubernetes manifest to re-use the exact same CLIENT_ID that the gateway is already using and inject it into Metabase. Zero new setup, zero new clicks.

Option 2: The Tool Swap (The True Seamless B2B Fix)
If you don't want to rely on Google at all, we rip out Metabase.
We swap it for Apache Superset (or Redash). Superset is an elite, open-source BI tool that natively supports REMOTE_USER header authentication in its free tier.
This lets us build the exact "Header-Based Trust" architecture we discussed earlier:

You pass the front door gateway.

The gateway injects the X-Forwarded-User header.

Superset reads it and instantly logs you in.

Zero Google Console. Zero passwords. Zero clicks.

To permanently kill this friction, tell me which path to take: REUSE (if we are already using Google at the gateway) or SWAP (rip out Metabase for Superset).
