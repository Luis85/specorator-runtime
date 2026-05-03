# Spec: GitHub Pages — product page and product demo

```yaml
id: SPEC-HW-001
feature: hello-world
issue: "#8"
stage: specification
status: draft
created: 2026-05-03
```

---

## Context

The Hello World milestone (issue #8) includes a runnable example that demonstrates the full end-to-end execution scenario. Two public-facing artefacts must accompany that example:

- a **product page** — the human-readable introduction to Specorator Runtime
- a **product demo** — a static, self-contained rendering of a Hello World run

Both files are static HTML. They require no build step, no server, and no JavaScript framework. They are hosted on **GitHub Pages** served from the `docs/` directory of the `main` branch.

---

## Deliverables

### 1. `docs/index.html` — product page

A single static HTML file. No external dependencies that require a build step. Inline styles are acceptable; a single linked stylesheet (`docs/style.css`) is also acceptable.

Must include:

- Hero statement — one sentence, jargon-free, that explains what Specorator Runtime is
- Problem → Solution narrative — 3–5 sentences
- Key capabilities — outcome-oriented bullet list (not feature names)
- Integration map — how the runtime connects to Specorator UI, `agentic-workflow`, and `agentonomous`
- Current status — clearly states this is `v0.1.0`, the Hello World release
- Link to the GitHub repository
- Link to the product demo (`demo.html`)

Must NOT include:

- API documentation
- Marketing language disconnected from the PRD
- Anything that requires a server, CMS, or build pipeline to render

---

### 2. `docs/demo.html` — product demo

A single static HTML file that presents a rendered execution trace of the Hello World scenario.

Must include:

- A brief intro (2–3 sentences) explaining what the viewer is looking at
- The full ordered event log from a Hello World run, rendered as a visual timeline or structured list:
  1. `workflow.started`
  2. `task.created`
  3. `task.ready`
  4. `agent.invoked`
  5. `agent.completed`
  6. `artifact.created`
  7. `task.completed`
  8. `workflow.completed`
- For each event: event name, a one-sentence description of what it means, and the key payload fields
- The artifact produced by the stub agent, displayed inline
- Session state snapshot after completion (id, state: `completed`, task count, artifact count)
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
- A CI workflow `pages.yml` must be added under `.github/workflows/` that validates the pages are reachable after every push to `main`

#### `pages.yml` requirements

Trigger: `push` to `main` (paths: `docs/**`)

Steps:
1. Checkout
2. Verify `docs/index.html` exists
3. Verify `docs/demo.html` exists
4. (Optional) Run an HTML validator (e.g. `html-validate` or `tidy`) if one is available in the CI environment

---

## Acceptance Criteria

- [ ] `docs/index.html` committed and renders correctly in a browser opened via `file://`
- [ ] `docs/demo.html` committed and renders correctly in a browser opened via `file://`
- [ ] All 8 Hello World events are present and correctly ordered in `docs/demo.html`
- [ ] The stub agent artifact is visible in `docs/demo.html`
- [ ] GitHub Pages is configured to serve from `docs/` on `main`
- [ ] `https://luis85.github.io/specorator-runtime/` resolves to the product page after merge to `main`
- [ ] `https://luis85.github.io/specorator-runtime/demo.html` resolves to the product demo
- [ ] `.github/workflows/pages.yml` exists and passes on `main`
- [ ] Both HTML files pass the cold-reader test: a newcomer can understand the project within 60 seconds

---

## Constraints

- No build step — both files must be valid HTML as committed; no transpilation or bundling
- No external runtime dependencies — CSS from a CDN (e.g. a single font or reset) is acceptable, but the pages must degrade gracefully if offline
- Terminology must be consistent with the PRD and `docs/product-page.md`: _session_, _event bus_, _task_, _agent_, _artifact_, _workflow_
- The product demo content must match the actual output of `examples/hello-world/index.ts` — it is not a fictional example

---

## Related

- Issue #8 — Milestone: Hello World
- Issue #2 — Product presence (`docs/product-page.md` is the source document for `docs/index.html`)
- `examples/hello-world/` — the runnable source that the demo page renders statically
- PRD §11 — UX Entry Points
