# specorator-runtime

The execution layer for the Specorator ecosystem — provides an agent habitat, loads typed workflow packages, and exposes a small request/response API that Specorator uses to start sessions, run commands, submit tasks, and stream events.

[![Phase 1 — Architecture & Design](https://img.shields.io/badge/phase-1%20architecture%20%26%20design-blue)](https://github.com/Luis85/specorator-runtime/issues/14)

---

## Where it fits

```
┌─────────────────────────────────────────────────────────────────┐
│  agentic-workflow — workflow package source                      │
│  Agent/skill/command definitions, TS scripts, templates, docs   │
└──────────────────────────────┬──────────────────────────────────┘
                               │ assembled into WorkflowPackage
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  specorator-runtime  (this package)                             │
│  Agent habitat · capability provider · event bus                │
│  Public API: startSession / stopSession / getSession            │
│              submitTask / runCommand / runScript                 │
│              spawnAgent / stopAgent / bus.subscribe             │
│  Orchestrator engine (SAO): automated agent dispatch            │
└──────┬──────────────────────────────────────────────────────────┘
       │  submits tasks/commands; subscribes to events
       ▼
┌──────────────────────────┐   ┌────────────────────────────────┐
│  Specorator              │   │  agentonomous                  │
│  Obsidian plugin         │   │  Autonomous agent library      │
│  Cockpit UI · vault I/O  │   │  Lives inside the runtime      │
│  HITL · WorkflowPackage  │   │  as ECS entities               │
│  assembly                │   │  instantiated from definitions │
└──────────────────────────┘   └────────────────────────────────┘
```

The runtime sits between workflow definitions and UI/agent consumers. It exposes a small, stable surface so consumers never see internal ECS, definition-parsing, permission enforcement, or orchestration complexity.

---

## Core concepts

**Session** — one isolated execution context for a workflow package. Created via `startSession(workflowPackage, capabilities)`. Query its state at any point via `getSession(id)`.

**Event bus** — the coordination spine. Every lifecycle change emits a typed `RuntimeEvent` with a monotonic `seq`, `traceId`, and `parentId`. Subscribe via `bus.subscribe`. Events are ordered and trace-correlated across the three buses (plugin, runtime, agent-internal).

**Task lifecycle** — tasks progress through `created → ready → running → completed | failed`. The runtime resolves dependencies and advances tasks when prerequisites are met.

**Agent habitat** — the runtime hosts `agentonomous` agents as ECS entities. It provisions capabilities (LLM, vault-read, workflow-reference), enforces per-agent permissions declared in the workflow package, and ticks the agent loop each simulation step.

**Orchestrator engine (SAO)** — the automated dispatch layer built into the runtime. Polls the vault for eligible features, dispatches Claude CLI agent processes into isolated git worktrees, evaluates artifact quality via a sensor hierarchy, and advances workflow stages upon confirmed success. Configurable via the `agentOrchestrator` settings namespace with human review gates.

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
| Phase 0 — Foundation | Product identity, knowledge architecture, design workshops, ADRs, solution proposal | In progress |
| Phase 1 — Architecture & Design | Runtime kernel, data model, orchestrator design, all design decisions | In progress |
| Phase 2 — Engineering Scaffold | Tooling, CI, test infrastructure, architecture fitness, entropy management | Planned |
| Hello World (v0.1.0) | First end-to-end runtime proof | Planned |
| Phase 3+ | Replay, sandboxing, MCP transport, semantic indexing | Deferred |

See the full roadmap in [issue #37](https://github.com/Luis85/specorator-runtime/issues/37).

---

## Related

- [ROADMAP — issue #37](https://github.com/Luis85/specorator-runtime/issues/37) — full phase-by-phase delivery plan
- [PRD — issue #1](https://github.com/Luis85/specorator-runtime/issues/1)
- [VISION.md](./VISION.md) — the decision filter for this project
- [Architecture proposal — issue #14](https://github.com/Luis85/specorator-runtime/issues/14)
- [Orchestrator engine — issue #43](https://github.com/Luis85/specorator-runtime/issues/43)
- [`agentic-workflow`](https://github.com/Luis85/agentic-workflow) — workflow definitions consumed by the runtime
- [`agentonomous`](https://github.com/Luis85/agentonomous) — agent implementations invoked by the runtime
- [Specorator](https://github.com/Luis85/specorator) — the Obsidian plugin that drives the runtime
