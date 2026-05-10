"""Orchestrator engine — tracks tasks across all running autonomous agents.

The full orchestrator spec is pending design. This module defines the stable
interface (OrchestratorEngine) that the runtime depends on, plus a lightweight
in-memory implementation (InMemoryOrchestratorEngine) suitable for development
and testing. The production implementation will replace InMemoryOrchestratorEngine
once the spec is finalised.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum
from uuid import UUID, uuid4


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentTask:
    id: UUID = field(default_factory=uuid4)
    agent_id: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict = field(default_factory=dict)


class OrchestratorEngine(ABC):
    """Interface for the orchestrator engine.

    The runtime owns exactly one engine instance and is the sole entry point
    for submitting and querying agent tasks. Concrete implementations must be
    thread-safe.
    """

    @abstractmethod
    def submit_task(self, agent_id: str, description: str, metadata: dict | None = None) -> AgentTask: ...

    @abstractmethod
    def get_task(self, task_id: UUID) -> AgentTask | None: ...

    @abstractmethod
    def update_task_status(self, task_id: UUID, status: TaskStatus) -> None: ...

    @abstractmethod
    def list_tasks(
        self,
        agent_id: str | None = None,
        status: TaskStatus | None = None,
    ) -> list[AgentTask]: ...

    @abstractmethod
    def cancel_task(self, task_id: UUID) -> None: ...


class InMemoryOrchestratorEngine(OrchestratorEngine):
    """Development stub — stores tasks in memory, not suitable for production."""

    def __init__(self) -> None:
        self._tasks: dict[UUID, AgentTask] = {}

    def submit_task(self, agent_id: str, description: str, metadata: dict | None = None) -> AgentTask:
        task = AgentTask(agent_id=agent_id, description=description, metadata=metadata or {})
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: UUID) -> AgentTask | None:
        return self._tasks.get(task_id)

    def update_task_status(self, task_id: UUID, status: TaskStatus) -> None:
        task = self._tasks.get(task_id)
        if task:
            task.status = status
            task.updated_at = datetime.now(UTC)

    def list_tasks(
        self,
        agent_id: str | None = None,
        status: TaskStatus | None = None,
    ) -> list[AgentTask]:
        tasks = list(self._tasks.values())
        if agent_id is not None:
            tasks = [t for t in tasks if t.agent_id == agent_id]
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        return tasks

    def cancel_task(self, task_id: UUID) -> None:
        self.update_task_status(task_id, TaskStatus.CANCELLED)
