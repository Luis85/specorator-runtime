from abc import ABC, abstractmethod
from pathlib import Path

from specorator_runtime.log.logger import JsonlLogger, RuntimeLogger
from specorator_runtime.models.prompt import Prompt
from specorator_runtime.models.request import Request
from specorator_runtime.models.response import Response, ResponseStatus
from specorator_runtime.orchestrator.engine import InMemoryOrchestratorEngine, OrchestratorEngine
from specorator_runtime.prompt.builder import PromptEngineer, PromptStrategy
from specorator_runtime.router.router import Router, RoutingStrategy


class LLMConnector(ABC):
    """Sends a fully-formed Prompt to an LLM and returns raw text content.

    Implement this interface to connect any LLM provider to the runtime.
    The runtime calls send() after prompt engineering is complete and before
    building the final Response.
    """

    @abstractmethod
    def send(self, prompt: Prompt) -> str: ...


class Runtime:
    """Central gatekeeper and orchestrator for all LLM-bound requests.

    Responsibilities:
    - Receive a Request and return a Response.
    - Analyze and route the request via the Router.
    - Drive prompt engineering to produce a Prompt from the routed request.
    - Gate every outbound call through the LLMConnector.
    - Persist every Request and Response via the RuntimeLogger.
    - Own and expose the OrchestratorEngine for autonomous agent task tracking.
    """

    def __init__(
        self,
        llm_connector: LLMConnector,
        routing_strategy: RoutingStrategy | None = None,
        prompt_strategy: PromptStrategy | None = None,
        logger: RuntimeLogger | None = None,
        log_path: Path | str = "runtime.log.jsonl",
        orchestrator: OrchestratorEngine | None = None,
    ) -> None:
        self._llm = llm_connector
        self._router = Router(routing_strategy)
        self._prompt_engineer = PromptEngineer(prompt_strategy)
        self._logger = logger or JsonlLogger(log_path)
        self._orchestrator = orchestrator or InMemoryOrchestratorEngine()

    @property
    def orchestrator(self) -> OrchestratorEngine:
        return self._orchestrator

    def process(self, request: Request) -> Response:
        """Process a request end-to-end and return the response.

        Flow: log request → route → build prompt → send to LLM → build response → log response.
        Errors from the LLM connector are caught and surfaced as an ERROR-status Response
        so callers always receive a typed Response, never a raw exception.
        """
        self._logger.log_request(request)

        route = self._router.route(request)
        prompt = self._prompt_engineer.build(request, route)

        try:
            raw_content = self._llm.send(prompt)
            response = Response(
                request_id=request.id,
                prompt_id=prompt.id,
                content=raw_content,
                status=ResponseStatus.SUCCESS,
            )
        except Exception as exc:
            response = Response(
                request_id=request.id,
                prompt_id=prompt.id,
                content="",
                status=ResponseStatus.ERROR,
                metadata={"error": str(exc)},
            )

        self._logger.log_response(response)
        return response
