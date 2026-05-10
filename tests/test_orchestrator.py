from specorator_runtime.orchestrator.engine import InMemoryOrchestratorEngine, TaskStatus


def test_submit_task():
    engine = InMemoryOrchestratorEngine()
    task = engine.submit_task(agent_id="agent-1", description="do work")
    assert task.agent_id == "agent-1"
    assert task.status == TaskStatus.PENDING


def test_get_task():
    engine = InMemoryOrchestratorEngine()
    task = engine.submit_task(agent_id="agent-1", description="do work")
    fetched = engine.get_task(task.id)
    assert fetched is task


def test_get_task_returns_none_for_unknown():
    from uuid import uuid4
    engine = InMemoryOrchestratorEngine()
    assert engine.get_task(uuid4()) is None


def test_update_task_status():
    engine = InMemoryOrchestratorEngine()
    task = engine.submit_task(agent_id="agent-1", description="do work")
    engine.update_task_status(task.id, TaskStatus.RUNNING)
    assert engine.get_task(task.id).status == TaskStatus.RUNNING


def test_cancel_task():
    engine = InMemoryOrchestratorEngine()
    task = engine.submit_task(agent_id="agent-1", description="do work")
    engine.cancel_task(task.id)
    assert engine.get_task(task.id).status == TaskStatus.CANCELLED


def test_list_tasks_filter_by_agent():
    engine = InMemoryOrchestratorEngine()
    engine.submit_task(agent_id="a", description="task 1")
    engine.submit_task(agent_id="b", description="task 2")
    engine.submit_task(agent_id="a", description="task 3")

    tasks_a = engine.list_tasks(agent_id="a")
    assert len(tasks_a) == 2
    assert all(t.agent_id == "a" for t in tasks_a)


def test_list_tasks_filter_by_status():
    engine = InMemoryOrchestratorEngine()
    t1 = engine.submit_task(agent_id="a", description="task 1")
    engine.submit_task(agent_id="a", description="task 2")
    engine.update_task_status(t1.id, TaskStatus.RUNNING)

    running = engine.list_tasks(status=TaskStatus.RUNNING)
    assert len(running) == 1
    assert running[0].id == t1.id


def test_list_tasks_no_filter():
    engine = InMemoryOrchestratorEngine()
    engine.submit_task(agent_id="a", description="task 1")
    engine.submit_task(agent_id="b", description="task 2")
    assert len(engine.list_tasks()) == 2
