# Vision — Specorator Runtime

```yaml
document: VISION.md
issue: "#2"
stage: draft
created: 2026-05-04
```

---

## Why does this exist?

Workflows and agents exist throughout the Specorator ecosystem, but nothing orchestrates them. A workflow definition describes what should happen. An agent implementation knows how to do a task. Without a runtime, neither runs automatically, and no shared state connects them. The gap is an execution layer — something that reads a workflow, invokes the right agents in the right order, captures what they produce, and makes the whole thing observable. That is the only job of this library.

---

## Who benefits?

The human in the loop: a practitioner who designs knowledge work as a workflow and needs to see it execute, inspect what each agent produced, and intervene when something goes wrong. Not a developer wiring up plumbing — someone doing actual work, watching it run, and trusting the output.

---

## What does success look like in 12 months?

- A practitioner can define a multi-task workflow in `agentic-workflow`, install `specorator-runtime` from npm, start a session with three lines of TypeScript, and watch every task progress through the lifecycle without writing orchestration logic
- Specorator UI renders live session state — task graph, agent outputs, event log — directly from the runtime's event stream, with no polling
- `agentonomous` agents are invoked by the runtime with typed context and return typed artifacts; no manual wiring needed between workflow steps
- Breaking changes to the public API are rare because the session model, event catalog, and agent interface are stable enough that ecosystem consumers trust them across minor releases

---

## What is this explicitly NOT?

- Not a general-purpose workflow engine — it executes knowledge-work workflows, not arbitrary automation pipelines
- Not a distributed system — V1 is single-process, in-memory, single-user; no cloud, no multi-tenancy, no persistence layer
- Not a UI — it has no frontend; it emits events that a UI subscribes to
- Not an agent framework — it invokes agents from `agentonomous`; it does not define what agents are or how they reason
- Not a scheduler — sequential task execution in V1; complex scheduling strategies are explicitly deferred
- Not a replacement for `agentic-workflow` or `agentonomous` — it depends on both and does not absorb their responsibilities

When a decision would push the runtime toward any of the above, that is the signal to stop and record it in the Follow-Up Register.

---

## North Star

> Does this help humans understand, control, and evolve knowledge work?

Every architectural decision, API shape, and scoping choice is tested against this question. If the answer is not clearly yes, the decision is deferred or rejected.
