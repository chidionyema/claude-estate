# Founder, 2026-09-01 ~15:0xZ: activate the Dagster migration, do not fix the Mac Dagster

Verbatim: "also need to activate dagster migration plan soon, higher priority than fixing broken dagster, no point doing work twice"

Ruling id: R67-activate-dagster-migration-before-fixing-mac-dagster. Plan it activates: crew#716 (Dagster stays; control plane in the cluster; one clock; hybrid Mac compute), founder ruling 2026-08-30 17:31Z.

What changes now
- No session repairs the Mac Dagster (`ai.estate.scheduler`, code location not loading since 2026-08-28 01:14Z).
- Nothing new is scheduled on the Mac. crew#786 part 3 no longer adds a launchd job; the feed page is pushed by the handoff itself and the render becomes a cluster Dagster schedule under crew#716 CP3.
- Order: crew#716 CP2 (generated inventory of every clock) and CP1 (control plane in `platform/dagster/`) first, then CP3 (cluster rows), then CP4 (Mac-only rows over the tailnet).

Captured on arrival by session a2aed3c9.
