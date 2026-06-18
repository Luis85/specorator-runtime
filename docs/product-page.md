# Specorator Runtime — Product Page

```yaml
source: docs/product-page.md
feeds: docs/index.html (SPEC-HW-001)
issue: "#2"
stage: draft
created: 2026-05-04
updated: 2026-05-10
terminology: session, event bus, task, agent, artifact, workflow, orchestrator
```

---

## Hero Statement

Specorator Runtime is the execution layer that turns typed agentic workflow packages into running, observable, in-memory sessions — and provides the harness that lets the Specorator Agent Orchestrator dispatch automated agents reliably.

---

## Problem → Solution

Knowledge work teams using the Specorator ecosystem can define workflows and configure agents, but nothing runs them reliably. Workflows sit as static definitions. Agents are invoked manually, without shared context, structured output capture, or quality controls. There is no unified lifecycle, no session state to query, and no event stream for a UI to follow in real time.

Specorator Runtime closes that gap. It interprets typed workflow packages assembled from `agentic-workflow`, invokes agents from `agentonomous`, and coordinates execution through a typed event bus. The Specorator Agent Orchestrator (SAO) — built on the runtime's public API — dispatches isolated Claude CLI agents into per-feature git worktrees and advances stages upon confirmed artifact production. Every step emits a lifecycle event. The result is a stateful, observable session that any part of the ecosystem can subscribe to and query.

---

## Key Capabilities

- **Start and stop workflow sessions** — create a runtime session from a typed `WorkflowPackage`; query its state at any point via `getSession`
- **Dispatch commands and scripts** — `runCommand` orchestrates the full agent dispatch chain with permission enforcement; `runScript` invokes typed TS scripts with a narrow capability surface
- **Host agents in context** — `spawnAgent` instantiates an `agentonomous` agent as an ECS entity with provisioned capabilities (LLM, vault-read, workflow-reference); `submitTask` drives the agent loop with typed input
- **Enforce permissions** — a Permission Guard gates every dispatch against each agent's declared `allowedSkills`, `allowedCommands`, `allowedScripts`; denied calls emit `permission.denied` events for cockpit visibility
- **Stream trace-correlated events** — subscribe to any `RuntimeEvent` from any part of the system; events carry `traceId`/`parentId` correlated across the three buses (plugin, runtime, agent-internal)
- **Automated stage dispatch (SAO)** — the orchestrator engine polls the vault, dispatches Claude CLI agents into isolated worktrees, evaluates output via a feedforward/feedback sensor hierarchy, and advances stages — with human review gates configurable per stage

---

## Integration Map

```
agentic-workflow
  (definitions source)
       │ WorkflowPackage assembled by Specorator
       ▼
Specorator (Obsidian plugin)
  │  startSession(workflowPackage, capabilities)
  │  runCommand / submitTask / runScript
  │  subscribes to RuntimeEvents
  ▼
specorator-runtime  (this package)
  │  hosts agents (agentonomous)
  │  enforces permissions
  │  emits RuntimeEvents
  │  SAO: dispatches Claude CLI → worktrees → artifacts
  │
  └─► agentonomous  (agent library — lives inside runtime as ECS entities)
```

**Consuming the runtime:**

```ts
import { RuntimeKernel } from 'specorator-runtime';
import type { Session, RuntimeEvent, WorkflowPackage } from 'specorator-runtime';

const session = await kernel.startSession(workflowPackage, capabilities);
session.bus.subscribe(event => { /* handle RuntimeEvent */ });
await kernel.runCommand(session.id, '/spec:requirements', args);
```

All public types are re-exported from a single barrel entry point. No deep or path-based imports required.

---

## Current Status

**Phase 1 — Architecture & Design** *(in progress)*

Every design decision — runtime kernel, data model, orchestrator engine, failure taxonomy, trace propagation — is being ratified before implementation begins. The v0.1.0 Hello World release follows once the architecture is locked and the engineering scaffold is in place.

**Delivery plan:**

| Phase | Focus | Status |
|---|---|---|
| Phase 0 — Foundation | Product identity, knowledge architecture, design workshops, ADRs, solution proposal | In progress |
| Phase 1 — Architecture & Design | Runtime kernel, data model, orchestrator design, all design decisions | In progress |
| Phase 2 — Engineering Scaffold | Tooling, CI, test infrastructure, architecture fitness, entropy management | Planned |
| Hello World (v0.1.0) | First end-to-end runtime proof | Planned |
| Phase 3+ | Replay, sandboxing, MCP transport, semantic indexing | Deferred |

Non-Goals (V1): distributed execution, multi-user collaboration, cloud-native scaling, filesystem persistence, complex scheduling.

---

## Related

- [GitHub repository](https://github.com/Luis85/specorator-runtime)
- [ROADMAP — issue #37](https://github.com/Luis85/specorator-runtime/issues/37)
- [PRD — issue #1](https://github.com/Luis85/specorator-runtime/issues/1)
- [`agentic-workflow`](https://github.com/Luis85/agentic-workflow) — workflow definitions consumed by the runtime
- [`agentonomous`](https://github.com/Luis85/agentonomous) — agent implementations invoked by the runtime
- [Specorator](https://github.com/Luis85/specorator) — the Obsidian plugin that drives the runtime
