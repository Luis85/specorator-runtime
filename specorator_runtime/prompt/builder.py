from abc import ABC, abstractmethod

from specorator_runtime.models.prompt import Message, Prompt
from specorator_runtime.models.request import Request
from specorator_runtime.router.router import Route


class PromptStrategy(ABC):
    @abstractmethod
    def build(self, request: Request, route: Route) -> Prompt: ...


class DefaultPromptStrategy(PromptStrategy):
    """Prepends a system message, replays context history, then appends the request content."""

    def __init__(self, system_prompt: str = "You are a helpful assistant.") -> None:
        self._system_prompt = system_prompt

    def build(self, request: Request, route: Route) -> Prompt:
        messages: list[Message] = [Message(role="system", content=self._system_prompt)]

        for entry in request.context:
            messages.append(Message(role=entry.get("role", "user"), content=entry.get("content", "")))

        messages.append(Message(role="user", content=request.content))

        return Prompt(
            request_id=request.id,
            messages=messages,
            parameters={"pipeline": route.pipeline, **route.parameters},
        )


class PromptEngineer:
    def __init__(self, strategy: PromptStrategy | None = None) -> None:
        self._strategy = strategy or DefaultPromptStrategy()

    def build(self, request: Request, route: Route) -> Prompt:
        return self._strategy.build(request, route)
