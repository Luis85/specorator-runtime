from pathlib import Path

import pytest

from specorator_runtime.models.prompt import Prompt
from specorator_runtime.models.request import Request
from specorator_runtime.models.response import ResponseStatus
from specorator_runtime.orchestrator.engine import InMemoryOrchestratorEngine
from specorator_runtime.runtime import LLMConnector, Runtime


class EchoConnector(LLMConnector):
    """Returns the last user message content as-is."""

    def send(self, prompt: Prompt) -> str:
        user_messages = [m for m in prompt.messages if m.role == "user"]
        return user_messages[-1].content if user_messages else ""


class FailingConnector(LLMConnector):
    def send(self, prompt: Prompt) -> str:
        raise RuntimeError("LLM unavailable")


@pytest.fixture
def runtime(tmp_path: Path) -> Runtime:
    return Runtime(llm_connector=EchoConnector(), log_path=tmp_path / "test.log.jsonl")


def test_process_returns_response(runtime: Runtime):
    req = Request(content="ping")
    resp = runtime.process(req)
    assert resp.request_id == req.id
    assert resp.content == "ping"
    assert resp.status == ResponseStatus.SUCCESS


def test_process_links_prompt_id(runtime: Runtime):
    req = Request(content="hello")
    resp = runtime.process(req)
    assert resp.prompt_id is not None


def test_process_logs_request_and_response(tmp_path: Path):
    import json
    log_path = tmp_path / "test.log.jsonl"
    rt = Runtime(llm_connector=EchoConnector(), log_path=log_path)
    req = Request(content="logged?")
    rt.process(req)

    lines = log_path.read_text().strip().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["type"] == "request"
    assert json.loads(lines[1])["type"] == "response"


def test_process_returns_error_response_on_llm_failure(tmp_path: Path):
    rt = Runtime(llm_connector=FailingConnector(), log_path=tmp_path / "test.log.jsonl")
    resp = rt.process(Request(content="fail me"))
    assert resp.status == ResponseStatus.ERROR
    assert "LLM unavailable" in resp.metadata["error"]


def test_runtime_exposes_orchestrator(runtime: Runtime):
    assert isinstance(runtime.orchestrator, InMemoryOrchestratorEngine)


def test_runtime_orchestrator_tracks_tasks(runtime: Runtime):
    task = runtime.orchestrator.submit_task(agent_id="agent-42", description="background job")
    assert runtime.orchestrator.get_task(task.id) is task


def test_routing_key_flows_into_prompt(tmp_path: Path):
    rt = Runtime(llm_connector=EchoConnector(), log_path=tmp_path / "test.log.jsonl")
    req = Request(content="summarize this", routing_key="summarize")
    resp = rt.process(req)
    assert resp.status == ResponseStatus.SUCCESS
