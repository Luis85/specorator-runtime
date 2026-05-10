# specorator-runtime

The central gatekeeper and request/response orchestrator for LLM-backed autonomous agents.

## Responsibilities

| Responsibility | Module |
|---|---|
| Receive a `Request`, return a `Response` | `runtime.Runtime` |
| Analyze and route requests | `router.Router` |
| Orchestrate prompt engineering → produce a `Prompt` | `prompt.PromptEngineer` |
| Gate all outbound calls through an `LLMConnector` | `runtime.LLMConnector` |
| Persist every `Request` and `Response` to a log | `log.RuntimeLogger` |
| Own and manage the orchestrator engine for autonomous agent tasks | `orchestrator.OrchestratorEngine` |

## Architecture

```
Request
  │
  ▼
Runtime.process()
  ├─ Router          → resolves a Route (pipeline name + parameters)
  ├─ PromptEngineer  → builds a Prompt from Request + Route
  ├─ LLMConnector    → sends Prompt to the LLM, returns raw text
  ├─ RuntimeLogger   → persists Request and Response (JSONL by default)
  └─ Response        ← returned to caller
```

The `Runtime` also owns an `OrchestratorEngine` instance, which tracks tasks
across all running autonomous agents. The full orchestrator spec is in design;
the current `InMemoryOrchestratorEngine` is a well-defined stub.

## Package layout

```
specorator_runtime/
├── runtime.py            # Runtime, LLMConnector
├── models/
│   ├── request.py        # Request
│   ├── response.py       # Response, ResponseStatus
│   └── prompt.py         # Prompt, Message
├── router/
│   └── router.py         # Router, RoutingStrategy, DefaultRoutingStrategy, Route
├── prompt/
│   └── builder.py        # PromptEngineer, PromptStrategy, DefaultPromptStrategy
├── log/
│   └── logger.py         # RuntimeLogger (ABC), JsonlLogger
└── orchestrator/
    └── engine.py         # OrchestratorEngine (ABC), InMemoryOrchestratorEngine, AgentTask, TaskStatus
```

## Quick start

```python
from specorator_runtime import Runtime, LLMConnector, Request
from specorator_runtime.models.prompt import Prompt

class MyLLM(LLMConnector):
    def send(self, prompt: Prompt) -> str:
        # call your LLM provider here
        ...

runtime = Runtime(llm_connector=MyLLM())

response = runtime.process(Request(content="What is the capital of France?"))
print(response.content)   # "Paris"
print(response.status)    # ResponseStatus.SUCCESS
```

## Extending the runtime

### Custom routing

```python
from specorator_runtime import Runtime, RoutingStrategy, Route
from specorator_runtime.models.request import Request

class KeywordRouter(RoutingStrategy):
    def resolve(self, request: Request) -> Route:
        if "summarize" in request.content:
            return Route(pipeline="summarize", parameters={"max_tokens": 200})
        return Route(pipeline="default")

runtime = Runtime(llm_connector=MyLLM(), routing_strategy=KeywordRouter())
```

### Custom prompt engineering

```python
from specorator_runtime import Runtime, PromptStrategy
from specorator_runtime.models.prompt import Prompt, Message
from specorator_runtime.models.request import Request
from specorator_runtime.router.router import Route

class RAGPromptStrategy(PromptStrategy):
    def build(self, request: Request, route: Route) -> Prompt:
        context = fetch_relevant_docs(request.content)
        return Prompt(
            request_id=request.id,
            messages=[
                Message(role="system", content=f"Context:\n{context}"),
                Message(role="user", content=request.content),
            ],
        )

runtime = Runtime(llm_connector=MyLLM(), prompt_strategy=RAGPromptStrategy())
```

### Custom logger

```python
from specorator_runtime import Runtime, RuntimeLogger
from specorator_runtime.models.request import Request
from specorator_runtime.models.response import Response

class DatabaseLogger(RuntimeLogger):
    def log_request(self, request: Request) -> None: ...
    def log_response(self, response: Response) -> None: ...

runtime = Runtime(llm_connector=MyLLM(), logger=DatabaseLogger())
```

### Orchestrator engine

The `Runtime` owns the orchestrator and exposes it via `runtime.orchestrator`.

```python
task = runtime.orchestrator.submit_task(agent_id="agent-1", description="background analysis")
runtime.orchestrator.update_task_status(task.id, TaskStatus.RUNNING)
tasks = runtime.orchestrator.list_tasks(agent_id="agent-1")
```

The `OrchestratorEngine` interface will be backed by a production implementation
once the orchestrator spec is finalised. Swap it in via the `orchestrator=` parameter on `Runtime`.

## Requirements

- Python 3.11+
- pydantic >= 2.0

## Development

```bash
pip install -e ".[dev]"
pytest
```