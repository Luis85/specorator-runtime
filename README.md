# specorator-runtime

The execution layer for the Specorator ecosystem — runs agentic workflows, orchestrates agents, and exposes session state and events to the rest of the system.

[![Phase 1 — Core Skeleton](https://img.shields.io/badge/phase-1%20core%20skeleton-blue)](https://github.com/Luis85/specorator-runtime/issues/8)

---

## Where it fits

```
Specorator UI  ──►  specorator-runtime  ◄──  agentic-workflow (definitions)
                           │
                           └──────────────◄──  agentonomous (agents)
```

The runtime sits between workflow definitions and agent implementations. It is the piece that makes the system execute.

---

## Core concepts

**Session** — one execution instance of a workflow. Contains the workflow reference, execution state, task graph, agent interactions, produced artifacts, and the full event log. Query it at any point during or after a run.

**Event bus** — the coordination spine. Every lifecycle change emits a typed event (`workflow.started`, `task.ready`, `agent.invoked`, `artifact.created`, …). Components subscribe; the runtime guarantees event ordering within a session.

**Task lifecycle** — each task in a workflow progresses through states: `created → ready → running → completed | failed`. The runtime resolves dependencies and advances tasks when their prerequisites are met.

---

## Getting started

> Not yet available — see the delivery plan below.
>
> The first installable release is `v0.1.0` (Hello World milestone, issue [#8](https://github.com/Luis85/specorator-runtime/issues/8)).
> Once published: `npm install specorator-runtime`

---

## Delivery plan

| Phase | Focus | Status |
|---|---|---|
| Phase 1 — Core Skeleton | Runtime kernel, event bus, session model | In progress → v0.1.0 |
| Phase 2 — Execution | Full workflow interpreter, agent executor | Planned |
| Phase 3 — Observability | Runtime API, logging, state store | Planned |
| Phase 4 — Integration | Connect to Specorator UI | Planned |

---

## Related

- [PRD — Specorator Runtime](https://github.com/Luis85/specorator-runtime/issues/1)
- [VISION.md](./VISION.md) — the decision filter for this project
- [`agentic-workflow`](https://github.com/Luis85/agentic-workflow) — workflow definitions consumed by the runtime
- [`agentonomous`](https://github.com/Luis85/agentonomous) — agent implementations invoked by the runtime
- [Specorator](https://github.com/Luis85/specorator) — the UI that subscribes to runtime events
