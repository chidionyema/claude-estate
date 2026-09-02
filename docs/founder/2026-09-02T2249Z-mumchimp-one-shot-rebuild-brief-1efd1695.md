---
captured: 2026-09-02T22:49:37+00:00
session: b4b812cb-c900-48a5-a58b-d4f76e4000a1
cwd: /Users/chidionyema/.claude
chars: 17968
source: founder prompt, verbatim (founder-doc-capture.py)
---

Mumchimp — one-shot rebuild brief

Target: mumchimp.com, every public page. Date: 2 Sept 2026.
Basis: the live homepage and a live pack page (/pack/7ba29bd2956e7e04) as they render today.
Scope is everything below and nothing outside it. Branch, one PR, before/after screenshots.

---

## 0. Read first — the five things that matter most

1. **The homepage sample shows the engine reading cookie banners.** The featured "Can the payer pay?" check cites ONS pages that returned only consent screens, plus an Australian loan site and a US hardship-loan page — for a UK check. That is the showcase. Fix the source gate (§4.1) before touching a pixel.
2. **Cards say "8× payback"; the same pack's page says "Payback 8.1 months."** One number, two units. Cards are currently showing months with a multiplier sign (§4.2).
3. **Kill / die / destroy / survive is banned sitewide.** Decided in August, not shipped. Nav still says "Kill log"; the hero still says "built to kill the idea first." Replacement table in §2.1.
4. **Every page repeats itself.** The pack page has three buy boxes, two lists of the six checks with different names, two "what's inside" models (14 documents vs. a legacy 4-document block). One of each (§7).
5. **The homepage is a front page, not the whole newspaper.** It currently carries five catalogues (What passed, main, US, US-GA, and show-more), two stat blocks, two document lists. Structure in §5.

---

## 1. Product truth — do not change

- Sourced, checked business opportunity packs. £19.99–£99.99, one payment, instant download, 14 documents in 6 files, 14-day refund. Priced by opportunity size.
- Theme: digital newsroom meets e-commerce. Light. White / near-black / teal primary, blue for links and info. No dark theme. No red except errors.
- Tone: Monzo. Fewest words. Peer to peer. No hype, no doom.
- Keep: accounts, /sample, the rejection ledger (renamed), per-pack OG images, the "Researched by Chidi" byline, the "£372/day to have this researched for you" anchor.
- Logo: wordmark only, existing "**Mum**chimp" lockup. Do not invent an icon.

---

## 2. Vocabulary

### 2.1 Banned → replacement

| Banned | Use instead |
|---|---|
| kill, killed, kills, kill log | reject, rejected, didn't pass · **Rejected** (nav) · `/rejected` |
| die, died, dead, death | rejected, didn't pass |
| survive, survived, survivor | pass, passed |
| destroy, sink, landmine, doom, graveyard | rewrite the sentence |
| "put through an AI built to kill the idea first" | "checked against sourced evidence before it goes on sale" |
| "Every idea walks into a room built to destroy it." | "Six checks. Sourced evidence. Only what passes goes on sale." |
| "6 in 100 or fewer survive the checks" | "6 in 100 pass" |
| "Killed on cited evidence" (stat tile) | "Rejected, with the source" |
| Document 05 "What would sink this" | "The case against" |
| Document 06 "…what would kill this" | "…what would stop this" |
| Title suffix "A business idea that survived our filter" | "Checked against sourced evidence" |
| Footer "Killed 1,364" | "Rejected 1,364" |

Grep the app, the pack templates, titles, metas, OG alt text and the email templates for `kill|die|dead|surviv|destroy|sink|landmine|doom`. Zero hits in public output when done. `/kill-log` 301s to `/rejected`.

### 2.2 The six checks — one name set, everywhere

Cards, pack page, sample, /how-it-works, /rejected. Question form; short form in brackets.

1. Is the pain real? (Pain)
2. Does the value last? (Value)
3. Is there room in the market? (Room)
4. Can the buyer pay? (Payer)
5. Can you reach the buyer? (Reach)
6. Is it legal to sell? (Legal)

Delete both other label sets currently live ("Real pain / Lasting value / Room past the competition…" and "Whether the pain is imagined / Whether the value decays…").

### 2.3 Copy rules — site and pack

- Fewest words that carry the meaning. Cut each sentence by a third, then read it aloud.
- No sentence opens with "Not".
- No bracketed expansions in titles or card summaries. Expand an acronym once, in the pack body.
- Category labels in sentence case everywhere. "Professional services", never "PROFESSIONAL SERVICES". Currently mixed on the same page.
- Skill filter labels: **Build it · Sell it · Run it · Grow an audience.** Never "Suits …". Drop "I don't code" (one result) into "Run it".
- Numbers: tabular figures, thousands separators, decimals only on money.
- "We" is fine. "You" is better. "Our engine" is not a character; the sources are the authority.

---

## 3. Card summary formula and lint

Every pack summary on a card: **[what it is] for [who], so [outcome].** One sentence, 8–22 words.

Live summaries that fail and must be regenerated:

- "HMRC can refuse a building subcontractor the right to be paid in full, so the contractor must withhold part of every invoice" — a problem, not an offer.
- "A carer who uses a direct payment to employ a personal assistant is legally the employer" — same.
- "A dataset of tribunal outcomes and DWP recalculation rules, built from freedom of information requests" — no buyer, no outcome.
- "…under British Standard British Standard (BS) 4142…" — expansion ran twice.
- Anything containing "(IP)", "(ICO)'s", "(BS)", "(OSHA)".

Lint (runs over all 77 now, then in CI on every new pack):
- title ≤ 70 chars, no bracket, no banned word
- summary 8–22 words, one sentence, contains a named buyer, no bracket, no leading "Not", no banned word, no repeated bigram
- category present, market present, published date present

Regenerate failures. A pack that fails lint does not go on the shelf.

---

## 4. Data hygiene — this is most of the upgrade

### 4.1 Source gate

Nothing is displayed on a public page — card, verdict, sample, /rejected — unless it passes all four:

1. Has a human-readable title. Not a URL slug ("3139annualsurveyofhoursandearningsashe…" is live today).
2. The fetched text is content. Reject anything matching consent / cookie / "enable JavaScript" / login / 404 patterns.
3. Jurisdiction matches the pack's market, or the domain is on an allowlist (ISO, WHO, OECD, IEEE, W3C, RFCs, etc.). A UK affordability check does not cite latitudefinancial.com.au or consumeraffairs.com.
4. It is cited against a specific claim, not a topic.

A check with fewer than 3 gated sources displays **"Evidence thin · n sources"** (amber) rather than junk. The verdict stays what it is; the display is honest.

Re-run the gate over all 77 packs and the sample. Any pack whose gated source count falls below 15 comes off the shelf until re-researched. Report the list in the PR.

### 4.2 Payback metric

- Find the field behind "8× payback" (card) and "Payback 8.1 months" (pack page). Same number, two renderings. Decide the unit from the model, not the UI.
- If months: **"Pays back in 8 months."** If a multiple: **"8× first-year return."** One label sitewide, including the sort option and the numbers preview.
- Suppress on cards when it isn't a selling point: ≤ 1× or > 18 months. "1× payback" is live today on two cards. Never again.

### 4.3 Completeness

Every pack has: category · market (UK / US, with optional state tag) · published date · verified date · payback or null · ≥ 15 gated sources.

Every card renders the same meta line in the same order: **payback · sources · verified.** Nulls drop out; nothing shifts.

### 4.4 The sample

The homepage sample is a **passed** check with impeccable evidence, hand-picked from the best pack in the catalogue. The current failed-check example moves to /how-it-works, or is deleted. Sample quality is the product's first impression; it is currently its worst.

---

## 5. Homepage — a front page

This order. Nothing else.

1. **Masthead.** Wordmark · today's date · nav: Catalogue · How it works · Rejected · Sample · Account. Strip beneath: "77 packs · 1,444 checked · last published [today / yesterday / 28 Aug]". "Updated 17 days ago" never appears anywhere on the site; if nothing shipped, show the date, not the age.
2. **Lead.** H1 "Business ideas with the research already done." Line: "The buyer, the price and the plan, checked against sourced evidence before it goes on sale." CTAs: **Browse the packs** (primary) · **Read a pack free** (secondary). One lead card (largest, with image): the newest pack.
3. **Numbers strip.** Passed 77 · Checked 1,444 · Sources 2,640. One row. Replaces the two stat tiles and the standalone "2,640" block.
4. **Catalogue.** One filter bar (§6). First 12 packs, then **Show more**. Market is a filter, not a section: delete "Built for the US market", "US (GA)", "US (FL)", "US (CA)", "US (TX)" sections. Delete the "What passed" three-pack row; it duplicates the catalogue.
5. **Band — Today's rejection.** One idea from the 1,364: title · the check it failed · one-line reason · one source · link to /rejected. Rotates daily. This is free daily content and the newsroom hook.
6. **Band — Why ideas get rejected.** Keep the six-bar chart. Heading: "What 1,364 ideas didn't pass, and why". The 624 number stays; it is the proof of rigour. Copy loses "kill".
7. **Sample.** One passed check (§4.4): question · Passed · one evidence line · source. CTA "Read the whole sample free · no email".
8. **What you get.** 14 documents as a compact two-column list; 6 files as one row. Once.
9. **Email.** One field, one button, two toggles: "Only when a new pack ships" · "Weekly: new packs and rejections".
10. **Trust strip.** 14-day refund · every claim sourced · one payment · Researched by Chidi (photo or initials).
11. **Footer.** As now, vocabulary fixed.

Delete: "Every idea walks into a room built to destroy it" block · second 14-document list · standalone "2,640" block · all per-market sections · "Show the other 45 UK packs".

---

## 6. Filters — one system, live

- One bar: Search · Market · Category · Skill · Price · Sort. Mobile: one "Filter" sheet with the same fields and a live count on the apply button.
- Live apply. No "Filter packs" button.
- URL-synced: `/?market=uk&cat=trades&skill=build&price=50&sort=newest`. Back button works. Links are shareable. Category pages are this URL with a header.
- Active filters as chips above the grid, each with ×, plus **Clear all**.
- Options with 0 results hidden. Options with 1 result shown as "(1)".
- Price: four chips — ≤ £20 · ≤ £30 · ≤ £50 · ≤ £100.
- Sort: Newest · Payback · Most sources · Price ↑ · Price ↓ · A–Z. Newest requires the date on the card.
- One result count, once: "23 of 77". Not "77/77" and "77 of 77" both.
- Result count region is `aria-live="polite"`. Bar is fully keyboard-operable.

---

## 7. Pack page — the money page

This order. One buy box.

1. **Breadcrumb.** Catalogue / [Category] / [Pack].
2. **Header.** Category · market tag (UK / US · GA) · H1 · one-sentence offer · "Who buys it: …" one line · stat row: 34 sources · 6/6 passed · verified 15 Aug 2026 · UK. The two tags from "Could you run this?" (Mostly automated · Vertical tool) become pills here; delete that section.
3. **Buy box.** Right rail on desktop, sticky bottom bar on mobile. Price · **Buy** · "Read a pack free first" · 14-day refund · "£372/day to have this researched for you (YunoJuno)" · "Researched by Chidi". The only buy box on the page. Delete the other two.
4. **Verdicts.** Six cards. Each: the question (§2.2) · **Passed** · one evidence line · source domain as a live link. This is the proof, and it is currently missing: the page lists six check names with nothing under them.
5. **Inside the pack.** 14 documents as an accordion, collapsed; 6 files as a row. Delete the legacy "The table of contents" block with its 4-document model (Blueprint / Go-to-market / Operations / Financial model). It contradicts the 14.
6. **Numbers preview.** Month-1 revenue · payback (with unit) · assumption count, blurred, "in document 04".
7. **Related.** Three packs from the same category or same buyer. Delete "Same mechanics, different world": the live picks (clinical coding, code-theft workspace) do not share mechanics with a scaffolding permit app.
8. **Share.** Icons, not raw intent URLs.
9. **Footer.**

"6 in 100" appears once, in the header stat row. "1,444 / 94.5%" does not appear on the pack page; it is a homepage fact.

---

## 8. /rejected — was /kill-log

- H1 "1,364 ideas that didn't pass." Sub: "Each with the check it failed and the source that decided it."
- Same filter system as the catalogue: check failed (six) · category · market.
- Row: title · check failed · one-line reason · source · date.
- Frame: the audit trail, not a graveyard. This page is why the 77 are worth paying for.
- The newest row feeds the homepage band.

---

## 9. Other pages

- **/how-it-works.** The six questions, one paragraph each, one real passed and one real failed example each, drawn from gated sources. Ends with the source gate in plain English. This is the only place a thin-evidence verdict is shown, and it is labelled as one.
- **/sample.** The full pack, reading exactly like the product. Sticky "Buy this pack" bar pointing at the real pack.
- **/ideas and category pages.** Each: 40-word intro · lead card · filtered catalogue. These are the SEO landing pages.
- **/pricing.** The ladder: four rows, one sentence each. Nothing else.
- **/about.** Chidi, photo, three sentences. The engine in one paragraph. The company line.
- **/faq.** Ten questions max. Refund, what's inside, US vs UK, re-verification, "is this advice" (no).

---

## 10. Design system

Tokens — light only:

- bg `#FAFAF7` · surface `#FFFFFF` · ink `#141412` · muted `#5C5B56` · rule `#E7E5DE` · teal (primary CTA, active chips) · blue (links, info badges) · amber ("evidence thin") · red (errors only).
- Type: one display face for H1/H2/pack titles — a serif or a high-contrast sans with newsroom weight; one text face for everything else. Scale 13 / 15 / 17 / 22 / 28 / 40 / 56. Body 17 / 1.5. Measure ≤ 68ch. Tabular numerals on every figure and price.
- Space: 8px base. Section gap 96 desktop / 64 mobile. Card padding 20. Radius 8 everywhere.
- Grid: 12 columns ≥ 1200 · 6 ≥ 768 · 4 at 390. Cards 3-up / 2-up / 1-up.

Three card components. No more.

- **Lead card.** Image · category · title (28) · summary · meta · price · CTA. Homepage lead and category-page lead only.
- **Row card.** No image. Category · market | title (22) | summary | meta · price · View. The catalogue. (The list-row format already approved.)
- **Tile card.** Title (17) · meta · price. Related, Today's rejection.

Same meta line, same order, same alignment on all three. Price is ink on surface, never coloured, never a badge.

Images: either every pack has an image in one consistent editorial style, or only lead cards carry images. No mixed state. Mixed is what reads as shabby.

Buttons: primary (teal) · secondary (outline) · text link. Nothing else. One primary per screen.

Polish checklist — fail any and the page is not done:
baselines align across columns · gutters equal · no orphan stats · no duplicate CTAs on one screen · no ALL CAPS · no line wider than 68ch · no layout shift on filter or load-more · every number tabular · one type family pair · one radius.

---

## 11. Newsroom rhythm

- Something ships every weekday: a new pack, a re-verified pack, or the day's rejection. The masthead strip always reads "last published today" or "yesterday".
- Packs older than 60 days are re-verified; badge "Re-checked [date]". Re-verification is a differentiator no competitor has; surface it.
- Cards carry dates. "Newest" is real.
- Weekly email: six lines — new packs, one notable rejection, one re-check. Plain text, one link each.

---

## 12. Conversion

- Social proof only if true: purchase count once it passes 25; sample-read count; Chidi byline with photo. Nothing invented.
- Stripe checkout with Apple Pay / Google Pay / Link on; one tap from the mobile buy bar.
- Post-purchase: download page with the six files, email with the same, "read index.html first".
- Refund and "every claim sourced" sit next to the price, not in the footer.
- Sample-to-pack: every sample page ends on the real pack's buy bar.

---

## 13. Tech, SEO, performance

- schema.org `Product` + `Offer` on every pack page; `ItemList` on catalogue and category pages; `BreadcrumbList` everywhere.
- Title pattern: "[Pack title] · £X · Mumchimp". No §2.1 vocabulary in any title, meta, or OG alt.
- 301 `/kill-log` → `/rejected`. Sitemap regenerated on publish.
- Budgets on 4G mobile: LCP < 2.0 s · CLS < 0.05 · first paint with 12 cards, rest lazy. AVIF/WebP. Fonts subset and preloaded.
- a11y: AA contrast, visible focus, keyboard-operable filters, `aria-live` counts, alt text on lead images (the pack title).

---

## 14. Process and definition of done

- Branch. One PR. No direct production edits.
- Before/after screenshots at 390 and 1440 for every public page, in the PR.
- `DECISIONS.md` at repo root: every choice made under this brief, one line, dated. Append only.
- Do not: add sections not listed here · change colours beyond §10 · go dark · collapse to one card component · restyle without also completing §2–§4.

Done when every box is ticked:

- [ ] grep for banned words: zero hits in public copy, titles, metas, OG, pack templates, emails
- [ ] all 77 summaries pass the §3 lint; lint runs in CI
- [ ] source gate re-run; no slug titles, off-jurisdiction sources, or consent pages visible anywhere; off-shelf list reported
- [ ] payback: one unit, one label, sitewide; suppressed where ≤ 1× / > 18 months
- [ ] one buy box per pack page · one "what's inside" per page · one set of six check names
- [ ] homepage sections match §5 exactly; per-market sections gone
- [ ] filters live, URL-synced, no button, chips, clear-all
- [ ] /rejected live; /kill-log redirects
- [ ] masthead never shows an age, only a date
- [ ] Lighthouse mobile ≥ 90 performance, 100 accessibility on home, one pack page, /rejected
- [ ] screenshots reviewed side by side; §10 polish checklist passed on every page
- [ ] `DECISIONS.md` committed
