import json
from abc import ABC, abstractmethod
from pathlib import Path

from specorator_runtime.models.request import Request
from specorator_runtime.models.response import Response


class RuntimeLogger(ABC):
    @abstractmethod
    def log_request(self, request: Request) -> None: ...

    @abstractmethod
    def log_response(self, response: Response) -> None: ...


class JsonlLogger(RuntimeLogger):
    """Appends newline-delimited JSON records to a file.

    Each line is a JSON object with a "type" field ("request" or "response")
    and a "data" field containing the serialized model.
    """

    def __init__(self, path: Path | str = "runtime.log.jsonl") -> None:
        self._path = Path(path)

    def log_request(self, request: Request) -> None:
        self._append({"type": "request", "data": request.model_dump(mode="json")})

    def log_response(self, response: Response) -> None:
        self._append({"type": "response", "data": response.model_dump(mode="json")})

    def _append(self, record: dict) -> None:
        with self._path.open("a") as fh:
            fh.write(json.dumps(record, default=str) + "\n")
