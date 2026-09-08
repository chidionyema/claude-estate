---
captured: 2026-09-08T10:41:05+00:00
session: aafd9b47-da6f-44b6-a51a-b005607c8507
cwd: /Users/chidionyema/dev/code/idp
chars: 5887
source: founder prompt, verbatim (founder-doc-capture.py)
---

The irony. The single biggest investment of the week was the fences themselves. That work broke the estate.

Second blocker. Freeze ticket crew#739 is open and says nothing may be released. Seven of its eight barred workflows are back on. Nobody enforces it and nobody closes it.

---

Snapshot

┌───────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│         Area          │                                                             Measured                                                              │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Main, 5 days          │ 1,086 commits: 673 image bumps, 400 real, 13 merges                                                                               │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Real commits by theme │ fences/CNI 34, gates/rules/tests 66, docs/reports 64, product/store/portal 25, Otto 19                                            │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Files touched most    │ platform/ns-fences 288, backstage/packages 113, tests/fixtures 79                                                                 │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Cluster               │ 2 nodes Ready. Flux 0/80. HelmReleases 31/32. Pods 30 of 193 not ready. 11 deployments short                                      │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Calico drop counter   │ 3,639 and 3,636 per node, was 12 at 10:20                                                                                         │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Open PRs idp          │ 4, all today                                                                                                                      │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Open issues           │ crew 383 (49 opened vs 31 closed in 5 days). idp 51, of which 24 are auto-filed P0 "Flux cannot reconcile" copies of the one fire │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Product tickets       │ Store CP1 to CP4 and agents CP1 to CP6, P1 ready-for-agent, untouched since 5 Sep                                                 │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Worktrees             │ 78, 55 in dead session scratchpads                                                                                                │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Branches              │ 625 local, 508 unmerged, 308 touched this week                                                                                    │
├───────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Sessions now          │ 13 session dirs, 34 claude processes on one repo                                                                                  │
└───────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

Root cause evidence
kustomize-controller: Get "http://source-controller.flux-system.svc.cluster.local./gitrepository/flux-system/flux-system/9c8aaf0f….tar.gz": dial tcp 10.96.202.29:80: i/o timeout
wget from inside kustomize-controller pod: download timed out

How to accelerate, in order

1. Put the fire out, one change. Take the default-deny fences off until each has a measured allow list. The estate ran 11 days with them unenforced, so this is a return to the last known-good state, not a regression. Then re-enable one namespace at a time against the drop counter. The previous session in this checkout was mid-way through this.
2. One word on crew#739. "Stands" and five workflows go off today, or "closed". Until then every session is either violating it or waiting on it.
3. Cut sessions from 13 to 2. One on the fire, one on the Store checkpoints. Parallel sessions on one repo are what produced 308 branches and 288 fence edits in a week. Volume without a throat is the pattern here.
4. Silence the robots. Batch image bumps to one pull request per day, and have the Flux incident filer open one issue per fire, not one per Kustomization. That removes about 60 percent of commit and ticket noise at once.
5. Prune in one pass. Prune the 55 dead worktrees and delete merged local branches. I can run this now, it is reversible.
6. Move product to the front. The Store checkpoints are the only tickets a buyer would call delivery. They are specified, labelled ready-for-agent, and nobody has picked one up.

Say "prune" and "fences off" and I do 1 and 5 now. I can also publish this as a one-page artifact if you want to share it.
