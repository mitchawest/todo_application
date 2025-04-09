import pytest  # noqa: F401
from modules.todo import Todo


def test_todo_happy_path():
    my_todo = Todo(1, "Test todo")
    assert my_todo.get_is_done() is False
    assert my_todo.get_priority() == 1


def test_todo_negative_path():
    error = None
    try:
        Todo(1, None)
    except Exception as e:
        error = e

    assert error is not None
    assert isinstance(error, ValueError)
    assert str(error) == "Submitted name None is not a string"
