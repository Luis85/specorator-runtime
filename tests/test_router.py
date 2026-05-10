from specorator_runtime.models.request import Request
from specorator_runtime.router.router import DefaultRoutingStrategy, Route, Router, RoutingStrategy


def test_default_strategy_uses_default_pipeline():
    req = Request(content="hello")
    strategy = DefaultRoutingStrategy()
    route = strategy.resolve(req)
    assert route.pipeline == "default"


def test_default_strategy_uses_routing_key():
    req = Request(content="hello", routing_key="summarize")
    strategy = DefaultRoutingStrategy()
    route = strategy.resolve(req)
    assert route.pipeline == "summarize"


def test_router_delegates_to_strategy():
    class FixedStrategy(RoutingStrategy):
        def resolve(self, request: Request) -> Route:
            return Route(pipeline="fixed", parameters={"k": "v"})

    router = Router(FixedStrategy())
    route = router.route(Request(content="x"))
    assert route.pipeline == "fixed"
    assert route.parameters == {"k": "v"}


def test_router_uses_default_strategy_when_none_given():
    router = Router()
    route = router.route(Request(content="hello"))
    assert route.pipeline == "default"
