---
captured: 2026-09-05T12:05:11+00:00
session: a38e9120-94ce-4652-b630-dee1b236e40d
cwd: /Users/chidionyema/dev/code/idp
chars: 2746
source: founder prompt, verbatim (founder-doc-capture.py)
---

sotto-answer-probe-29810160-znh68
Namespace
otto-gateway
Creation
05/09/2026, 13:00:21 BST
Labels
batch.kubernetes.io/controller-uid: 4004f2b3-00da-…

batch.kubernetes.io/job-name: otto-answer-probe-29…

controller-uid: 4004f2b3-00da-44bf-95ba-e58d9e7c3b…

job-name: otto-answer-probe-29810160

topology.kubernetes.io/region: uk-london-1

topology.kubernetes.io/zone: UK-LONDON-1-AD-1

Controlled by
Job: otto-answer-probe-29810160
State
Error
Node
10.0.159.197
Service Account
default
Host IPs
10.0.159.197
Pod IPs
10.244.1.151
QoS Class
Burstable
Priority
1000
Priority Class
platform-batch
Start Time
05/09/2026, 13:00:21 BST
Termination Grace Period
30s
Diagnostics
Critical
Pod status: Error

Review the container logs and the warning events below to find the cause.

Phase: Failed
Ready containers: 0/1
Critical
Condition PodReadyToStartContainers is False

Tolerations
Key
Value
Operator
Effect
Seconds
node.kubernetes.io/not-ready
Exists
NoExecute
300
node.kubernetes.io/unreachable
Exists
NoExecute
300
Conditions
Condition
Status
Last Transition
Last Update
Reason
PodReadyToStartContainers
False
4m
-
-
Initialized
True
4m
-
-
Ready
False
4m
-
PodFailed
ContainersReady
False
4m
-
PodFailed
PodScheduled
True
4m
-
-
Containers
probe
Status
Error (Error)
Exit Code
1
Started
05/09/2026, 13:00:23 BST
Finished
05/09/2026, 13:00:29 BST
Restart Count
0
Container ID
cri-o://d42caf73394e0c419ef49f7bd6942ce09dd14ab0875ac400bce9e02ca7d978dd
Image Pull Policy
IfNotPresent
Image
docker.io/library/python:3.11-slim

ID: docker.io/library/python@sha256:6c5ae9d998f4cc06f892f428d7af53a566c24ad0dc29fa572696b647cf2762a7

Command
python3 /scripts/probe.py
Environment
Name
Value
From
LITELLM_BASE_URL
http://litellm.llm.svc.cluster.local:4000/v1

manifest
OTEL_EXPORTER_OTLP_ENDPOINT
http://signoz-otel-collector.observability.svc:4318

manifest
OTTO_ROUTER_LANE_BULK_MODEL
deepseek

manifest
OTTO_ROUTER_LANE_JUDGMENT_MODEL
minimax

manifest
OTTO_ROUTER_LANE_VERIFY_MODEL
deepseek

manifest
OTTO_TENANT_ID
estate

manifest
Volume Mounts
Mount Path
from
I/O
/scripts
scripts
ReadOnly
/run/secrets/otto-gateway-router
router
ReadOnly
/tmp
tmp
ReadWrite
Volumes
scripts
Kind
configMap
Source
scripts
name
otto-answer-probe-script
defaultMode
365
router
Kind
secret
Source
router
secretName
otto-gateway-router
defaultMode
420
tmp
Kind
emptyDir
Source
tmp

Events
Type
Reason
From
Message
Age
Normal
Scheduled
default-scheduler
Successfully assigned otto-gateway/otto-answer-probe-29810160-znh68 to 10.0.159.197
4m24s
Normal
Pulled
kubelet
Container image "docker.io/library/python:3.11-slim" already present on machine and can be accessed by the pod
4m24s
Normal
Created
kubelet
Container created
4m22s
Normal
Started
kubelet
Container started
4m22s
