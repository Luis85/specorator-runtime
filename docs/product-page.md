# Specorator Runtime — Product Page

```yaml
source: docs/product-page.md
feeds: docs/index.html (SPEC-HW-001)
issue: "#2"
stage: draft
created: 2026-05-04
terminology: session, event bus, task, agent, artifact, workflow
```

---

## Hero Statement

Specorator Runtime is the execution layer that turns defined agentic workflows into running, observable, in-memory sessions — bridging workflow definitions and agent implementations into a single coordinated system.

---

## Problem → Solution

Knowledge work teams using the Specorator ecosystem can define workflows and configure agents, but nothing runs them. Workflows sit as static definitions. Agents exist but are invoked manually, without shared context or structured output capture. There is no unified lifecycle, no session state to query, and no event stream for a UI to follow in real time.

Specorator Runtime closes that gap. It interprets workflow definitions from `agentic-workflow`, invokes agents from `agentonomous`, and coordinates execution through a typed event bus. Every step in a workflow — from session start to artifact capture — emits a lifecycle event. The result is a stateful, observable session that any part of the ecosystem can subscribe to and query.

---

## Key Capabilities

- **Start and stop workflow sessions** — create a runtime session from any workflow definition; query its state at any point during or after execution
- **Coordinate task execution** — resolve task dependencies, advance tasks from `created` through `ready` to `completed` or `failed`, and emit lifecycle events at each transition
- **Invoke agents in context** — pass typed context to each agent, capture its structured output as an artifact, and log the interaction in the session event log
- **Stream execution events** — subscribe to any event type (`workflow.started`, `agent.invoked`, `artifact.created`, etc.) from any part of the system, in guaranteed order within a session
- **Query runtime state** — inspect sessions, task graphs, event logs, and produced artifacts via a clean TypeScript API, without filesystem or network I/O

---

## Integration Map

```
Specorator UI ──────────── subscribes to events, visualises sessions, triggers execution
       │
       ▼
Specorator Runtime  ◄──── interprets workflows from: agentic-workflow
  (this package)    ◄──── invokes agents from:       agentonomous
       │
       ▼
  npm registry ─────────── install with: npm install specorator-runtime
```

**Consuming the runtime:**

```ts
import { RuntimeKernel, EventBus } from 'specorator-runtime';
import type { Session, RuntimeEvent, Artifact } from 'specorator-runtime';
```

All public types are re-exported from a single entry point. No deep or path-based imports required.

---

## Current Status

**Phase 1 — Core Skeleton** *(in progress toward v0.1.0 — Hello World)*

The v0.1.0 release is the first proof that the system runs end-to-end. It delivers:

- `RuntimeKernel` — session lifecycle management
- `EventBus` — typed pub/sub, ordered within a session
- Session, Task, Artifact, and RuntimeEvent types
- A stub workflow interpreter and agent executor
- A runnable Hello World example (`examples/hello-world/`)
- This product page and a static demo at `docs/demo.html`, hosted on GitHub Pages

**Roadmap:**

| Phase | Focus | Status |
|---|---|---|
| Phase 1 — Core Skeleton | Runtime kernel, event bus, session model | In progress |
| Phase 2 — Execution | Full workflow interpreter, agent executor | Planned |
| Phase 3 — Observability | Runtime API, logging, state store | Planned |
| Phase 4 — Integration | Connect to Specorator UI | Planned |

Non-Goals (V1): distributed execution, multi-user collaboration, cloud-native scaling, filesystem persistence, complex scheduling.

---

## Related

- [GitHub repository](https://github.com/Luis85/specorator-runtime)
- PRD — issue #1 in this repository
- [`agentic-workflow`](https://github.com/Luis85/agentic-workflow) — workflow definitions consumed by the runtime
- [`agentonomous`](https://github.com/Luis85/agentonomous) — agent implementations invoked by the runtime
- [Specorator UI](https://github.com/Luis85/specorator) — the interface that subscribes to runtime events
