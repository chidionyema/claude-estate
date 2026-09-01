# Founder, 2026-09-02: estate DNA gets the email address — core company info that can change

Verbatim, in the crew#612 phone session (context: Diamond Standard DNA keys had just shipped —
ESTATE_ZONE, ESTATE_REGISTRY, ESTATE_STORAGE_PROVIDER):

> estate dna is nising enail address, basically core conpany inf that cn chage

Reading: the estate DNA (`clusters/oke/estate-config.yaml`) is missing the email address, and the
principle is broader — the DNA block is the one place for **core company info that can change**
(email, and whatever core identity values follow), not only infrastructure names.

Acted on same turn: `ESTATE_EMAIL` added to the DNA block on idp branch `fix/names-one-place`;
the intent compiler already reads every DNA value for the blindness check, so agents are refused
if they speak it, and surfaces reference `${ESTATE_EMAIL}`.
