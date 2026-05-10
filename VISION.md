# Vision — Specorator Runtime

```yaml
document: VISION.md
issue: "#2"
stage: draft
created: 2026-05-04
updated: 2026-05-10
```

---

## Why does this exist?

Workflows and agents exist throughout the Specorator ecosystem, but nothing orchestrates them reliably. A workflow definition describes what should happen. An agent implementation knows how to do a task. Without a runtime, neither runs automatically, no shared state connects them, and no harness keeps quality consistent across automated runs.

The gap is an execution layer — something that reads a typed workflow package, instantiates the right agents in a controlled habitat, dispatches the right commands, captures what they produce, and makes the whole thing observable. It must also provide the harness that lets automated agent dispatch (the SAO) produce reliable, auditable output without requiring human attention at every step. That is the only job of this library.

---

## Who benefits?

The human in the loop: a practitioner who designs knowledge work as a workflow and needs to see it execute, inspect what each agent produced, and intervene when something goes wrong. Not a developer wiring up plumbing — someone doing actual work, watching it run, and trusting the output.

Teams running the Specorator Agent Orchestrator also benefit: the runtime's harness — prompt templates, structured feedback sensors, trace-correlated event bus, permission enforcement — ensures automated agent runs produce consistent, auditable output without requiring manual review at every stage.

---

## What does success look like in 12 months?

- A practitioner can define a multi-stage workflow in `agentic-workflow`, install `specorator-runtime` from npm, start a session with three lines of TypeScript, and watch every stage progress through the lifecycle without writing orchestration logic
- Specorator renders live session state — agent activity, produced artifacts, event log — directly from the runtime's event stream, with no polling
- `agentonomous` agents are invoked by the runtime with typed context and return typed artifacts; no manual wiring needed between workflow stages
- The Specorator Agent Orchestrator (SAO) advances features through workflow stages automatically — dispatching isolated Claude CLI processes into per-feature worktrees, evaluating artifact quality, and merging confirmed output — with human review gates at configurable stages
- Breaking changes to the public API are rare because the session model, event catalog, and agent interface are stable enough that ecosystem consumers trust them across minor releases

---

## What is this explicitly NOT?

- Not a general-purpose workflow engine — it executes knowledge-work workflows, not arbitrary automation pipelines
- Not a distributed system — V1 is single-process, in-memory, single-user; no cloud, no multi-tenancy, no persistence layer
- Not a UI — it has no frontend; it emits events that a UI subscribes to
- Not an agent framework — it invokes agents from `agentonomous`; it does not define what agents are or how they reason
- Not a standalone orchestrator — automated agent dispatch belongs to the Specorator Agent Orchestrator (SAO), a separate layer built on the runtime's public API. The runtime provides the habitat, harness, and event bus; the SAO provides the dispatch loop, worktree isolation, prompt template system, and quality sensors
- Not a scheduler — sequential task execution in V1; complex scheduling strategies are explicitly deferred
- Not a replacement for `agentic-workflow` or `agentonomous` — it depends on both and does not absorb their responsibilities
- Not a methodology owner — the runtime loads and enforces definitions; it never authors them, writes to the vault, or models the 11-stage methodology in runtime types

When a decision would push the runtime toward any of the above, that is the signal to stop and record it in the Follow-Up Register.

---

## North Star

> Does this help humans understand, control, and evolve knowledge work?

Every architectural decision, API shape, and scoping choice is tested against this question. If the answer is not clearly yes, the decision is deferred or rejected.
