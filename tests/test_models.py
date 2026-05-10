from uuid import UUID
from specorator_runtime.models.request import Request
from specorator_runtime.models.response import Response, ResponseStatus
from specorator_runtime.models.prompt import Prompt, Message


def test_request_defaults():
    req = Request(content="hello")
    assert isinstance(req.id, UUID)
    assert req.content == "hello"
    assert req.context == []
    assert req.metadata == {}
    assert req.routing_key is None


def test_request_with_routing_key():
    req = Request(content="hello", routing_key="summarize")
    assert req.routing_key == "summarize"


def test_response_defaults():
    req = Request(content="hello")
    prompt = Prompt(request_id=req.id, messages=[])
    resp = Response(request_id=req.id, prompt_id=prompt.id, content="world")
    assert resp.status == ResponseStatus.SUCCESS
    assert resp.metadata == {}
    assert resp.request_id == req.id
    assert resp.prompt_id == prompt.id


def test_response_error_status():
    req = Request(content="hello")
    prompt = Prompt(request_id=req.id, messages=[])
    resp = Response(
        request_id=req.id,
        prompt_id=prompt.id,
        content="",
        status=ResponseStatus.ERROR,
        metadata={"error": "timeout"},
    )
    assert resp.status == ResponseStatus.ERROR


def test_prompt_with_messages():
    req = Request(content="hello")
    msgs = [Message(role="system", content="be helpful"), Message(role="user", content="hello")]
    prompt = Prompt(request_id=req.id, messages=msgs)
    assert len(prompt.messages) == 2
    assert prompt.messages[0].role == "system"
