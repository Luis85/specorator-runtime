from specorator_runtime.models.request import Request
from specorator_runtime.prompt.builder import DefaultPromptStrategy, PromptEngineer
from specorator_runtime.router.router import Route


def test_default_strategy_structure():
    req = Request(content="What is the capital of France?")
    route = Route(pipeline="default")
    strategy = DefaultPromptStrategy()
    prompt = strategy.build(req, route)

    assert prompt.request_id == req.id
    assert prompt.messages[0].role == "system"
    assert prompt.messages[-1].role == "user"
    assert prompt.messages[-1].content == req.content
    assert prompt.parameters["pipeline"] == "default"


def test_default_strategy_includes_context():
    req = Request(
        content="Follow-up question",
        context=[
            {"role": "user", "content": "First message"},
            {"role": "assistant", "content": "First reply"},
        ],
    )
    route = Route(pipeline="default")
    prompt = DefaultPromptStrategy().build(req, route)

    roles = [m.role for m in prompt.messages]
    assert roles == ["system", "user", "assistant", "user"]


def test_custom_system_prompt():
    req = Request(content="hi")
    route = Route(pipeline="default")
    strategy = DefaultPromptStrategy(system_prompt="You are a pirate.")
    prompt = strategy.build(req, route)
    assert prompt.messages[0].content == "You are a pirate."


def test_prompt_engineer_uses_default_strategy_when_none():
    engineer = PromptEngineer()
    prompt = engineer.build(Request(content="hello"), Route(pipeline="default"))
    assert prompt.messages[0].role == "system"
