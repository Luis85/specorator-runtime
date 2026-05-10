from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from specorator_runtime.models.request import Request


@dataclass
class Route:
    pipeline: str
    parameters: dict[str, Any] = field(default_factory=dict)


class RoutingStrategy(ABC):
    @abstractmethod
    def resolve(self, request: Request) -> Route: ...


class DefaultRoutingStrategy(RoutingStrategy):
    """Routes by routing_key when present, falls back to 'default' pipeline."""

    def resolve(self, request: Request) -> Route:
        pipeline = request.routing_key or "default"
        return Route(pipeline=pipeline)


class Router:
    def __init__(self, strategy: RoutingStrategy | None = None) -> None:
        self._strategy = strategy or DefaultRoutingStrategy()

    def route(self, request: Request) -> Route:
        return self._strategy.resolve(request)
