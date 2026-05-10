# Spec: GitHub Pages — product page and product demo

```yaml
id: SPEC-HW-001
feature: hello-world
issue: "#8"
stage: specification
status: draft
created: 2026-05-03
updated: 2026-05-10
inputs:
  - "#14 — architecture proposal (public API surface)"
  - "#15 — data model (RuntimeEvent union — authoritative event names)"
  - "#21 — failure-event taxonomy"
  - "#29 — CI workflow (hard vs. soft gate policy)"
```

---

## Context

The Hello World milestone (issue #8) includes a runnable example that demonstrates the first end-to-end execution scenario. Two public-facing artefacts must accompany that example:

- a **product page** — the human-readable introduction to Specorator Runtime
- a **product demo** — a static, self-contained rendering of a Hello World run

Both files are static HTML. They require no build step, no server, and no JavaScript framework. They are hosted on **GitHub Pages** served from the `docs/` directory of the `main` branch.

> **Living spec notice:** The event names, payload shapes, and API surface shown in this spec are preliminary. Authoritative definitions are resolved in #14 (architecture), #15 (data model), and #21 (failure-event taxonomy). The demo page content (`docs/demo.html`) must be verified against the actual output of `examples/hello-world/index.ts` before this spec is considered complete. Update the event table below when #15 §7 closes.

---

## Deliverables

### 1. `docs/index.html` — product page

A single static HTML file. No external dependencies that require a build step. Inline styles are acceptable; a single linked stylesheet (`docs/style.css`) is also acceptable.

Source document: `docs/product-page.md` (issue #2) is the canonical content source for this file. The HTML is a rendered version of that document.

Must include:

- Hero statement — one sentence, jargon-free, that explains what Specorator Runtime is
- Problem → Solution narrative — 3–5 sentences
- Key capabilities — outcome-oriented bullet list (not feature names)
- Integration map — how the runtime connects to Specorator, `agentic-workflow`, `agentonomous`, and the SAO orchestrator engine
- Current status — clearly states this is `v0.1.0`, the Hello World release
- Link to the GitHub repository
- Link to the product demo (`demo.html`)

Must NOT include:

- API documentation
- Marketing language disconnected from the PRD
- Anything that requires a server, CMS, or build pipeline to render

---

### 2. `docs/demo.html` — product demo

A single static HTML file that presents a rendered execution trace of the Hello World scenario. This is a **static snapshot of a real run** — not a fictional example. The content must match the actual output of `examples/hello-world/index.ts`.

Must include:

- A brief intro (2–3 sentences) explaining what the viewer is looking at and that this is a static snapshot
- The full ordered event log from a Hello World run, rendered as a visual timeline or structured list

  **Event names must match the ratified `RuntimeEvent` union from #15 §7 and #21.** Preliminary expected sequence:

  | # | Event | What it means |
  |---|---|---|
  | 1 | `session.started` | A new runtime session was created and the workflow package loaded |
  | 2 | `agent.spawned` | An agentonomous agent was instantiated as an ECS entity in the session |
  | 3 | `task.created` | A task was registered in the session task graph |
  | 4 | `task.ready` | Task prerequisites met; the agent may claim it |
  | 5 | `command.dispatched` | A command was dispatched to the agent for execution |
  | 6 | `artifact.created` | The agent produced a typed artifact output |
  | 7 | `task.completed` | The task transitioned to `completed` state |
  | 8 | `session.stopped` | The session was cleanly stopped and the lifecycle concluded |

  > Verify and update this table against `examples/hello-world/index.ts` output and #15 §7 before merging to `main`. Do not ship fictional event names.

- For each event: event name, a one-sentence description of what it means, and the key payload fields — at minimum: `eventId`, `traceId`, `seq`, `type`
- The artifact produced by the stub agent, displayed inline
- Session state snapshot after completion (`id`, `state: 'stopped'`, task count, artifact count)
- Link back to the product page (`index.html`)

Must NOT include:

- A live runtime — this is a static snapshot, not an interactive executor
- External API calls
- Any dependency that prevents the file from opening directly in a browser via `file://`

---

### 3. GitHub Pages configuration

- Source: `docs/` directory on the `main` branch
- No custom domain required for `v0.1.0`
- Expected URL: `https://luis85.github.io/specorator-runtime/`
- The repository's **GitHub Pages** setting must be configured to serve from `docs/` on `main`
- A CI workflow `pages.yml` must be added under `.github/workflows/`

#### `pages.yml` requirements

Per the CI gate philosophy in #29 — hard gates block merge; soft gates retry once and report without blocking:

Trigger: `push` to `main` (paths: `docs/**`)

**Hard gates** (fail the job immediately if violated):
1. Checkout
2. Verify `docs/index.html` exists
3. Verify `docs/demo.html` exists
4. Run HTML validator (e.g. `html-validate`) on both files — both must be valid HTML5
5. Verify neither file contains `<script src>` pointing to an external host that is not a CDN allowlist entry

**Soft gate** (retry once; report failure as a warning without blocking merge — network-dependent):
6. Reachability check: `curl -f https://luis85.github.io/specorator-runtime/` — GitHub Pages propagation may lag behind the push; a single retry after 30 s is acceptable before marking the step as advisory-failed

Each failing step must emit a clear, agent-readable error message per the lint message policy in #28:
```
[pages-check] docs/index.html missing
  ✗ The product page HTML file was not found at docs/index.html
  ✓ Fix: ensure docs/index.html is committed on the main branch
  Docs: specs/hello-world/github-pages.md#deliverables
```

---

## Acceptance Criteria

- [ ] `docs/index.html` committed and renders correctly in a browser opened via `file://`
- [ ] `docs/demo.html` committed and renders correctly in a browser opened via `file://`
- [ ] All events in `docs/demo.html` use names from the ratified `RuntimeEvent` union (#15 §7, #21) — verified against `examples/hello-world/index.ts` actual output
- [ ] Each event entry in `docs/demo.html` shows `eventId`, `traceId`, `seq`, `type`, and key payload fields
- [ ] The stub agent artifact is visible in `docs/demo.html`
- [ ] Integration map in `docs/index.html` includes Specorator, agentonomous, agentic-workflow, and SAO orchestrator engine
- [ ] GitHub Pages is configured to serve from `docs/` on `main`
- [ ] `https://luis85.github.io/specorator-runtime/` resolves to the product page after merge to `main`
- [ ] `https://luis85.github.io/specorator-runtime/demo.html` resolves to the product demo
- [ ] `.github/workflows/pages.yml` exists with hard/soft gate split per #29
- [ ] Each `pages.yml` error message follows the agent-readable format from #28
- [ ] Both HTML files pass the cold-reader test: a newcomer can understand the project within 60 seconds

---

## Constraints

- No build step — both files must be valid HTML as committed; no transpilation or bundling
- No external runtime dependencies — CSS from a CDN (e.g. a single font or reset) is acceptable, but the pages must degrade gracefully if offline
- Terminology must be consistent with the PRD and `docs/product-page.md`: _session_, _event bus_, _task_, _agent_, _artifact_, _workflow_, _orchestrator_
- Event names in `docs/demo.html` are authoritative in #15 and #21 — do not use assumed or fictional names; verify against the actual Hello World run before merging
- The product demo content must match the actual output of `examples/hello-world/index.ts` — it is a rendered snapshot, not invented content

---

## Related

- Issue #8 — Milestone: Hello World
- Issue #2 — Product presence (`docs/product-page.md` is the source document for `docs/index.html`)
- Issue #14 — Architecture proposal v1 (public API surface — authoritative)
- Issue #15 — Data model (RuntimeEvent union — authoritative event names and payload shapes)
- Issue #21 — Failure-event taxonomy (which `*.failed` and orchestration events ship in V1)
- Issue #29 — CI workflow (hard vs. soft gate policy)
- Issue #28 — Lint conventions (agent-readable error message format for `pages.yml`)
- Issue #43 — Orchestrator engine (SAO — referenced in integration map)
- `examples/hello-world/` — the runnable source that the demo page renders statically
- PRD §11 — UX Entry Points
