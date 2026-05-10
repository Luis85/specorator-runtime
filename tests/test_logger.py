import json
from pathlib import Path

import pytest

from specorator_runtime.log.logger import JsonlLogger
from specorator_runtime.models.prompt import Prompt
from specorator_runtime.models.request import Request
from specorator_runtime.models.response import Response, ResponseStatus


@pytest.fixture
def log_file(tmp_path: Path) -> Path:
    return tmp_path / "test.log.jsonl"


def test_logs_request(log_file: Path):
    logger = JsonlLogger(log_file)
    req = Request(content="hello")
    logger.log_request(req)

    lines = log_file.read_text().strip().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["type"] == "request"
    assert record["data"]["content"] == "hello"


def test_logs_response(log_file: Path):
    logger = JsonlLogger(log_file)
    req = Request(content="hello")
    prompt = Prompt(request_id=req.id, messages=[])
    resp = Response(request_id=req.id, prompt_id=prompt.id, content="world")
    logger.log_response(resp)

    record = json.loads(log_file.read_text().strip())
    assert record["type"] == "response"
    assert record["data"]["content"] == "world"
    assert record["data"]["status"] == ResponseStatus.SUCCESS


def test_appends_multiple_records(log_file: Path):
    logger = JsonlLogger(log_file)
    req = Request(content="a")
    prompt = Prompt(request_id=req.id, messages=[])
    resp = Response(request_id=req.id, prompt_id=prompt.id, content="b")

    logger.log_request(req)
    logger.log_response(resp)

    lines = log_file.read_text().strip().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["type"] == "request"
    assert json.loads(lines[1])["type"] == "response"
