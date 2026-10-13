
import pytest
from app import app, tasks


@pytest.fixture
def client():
    tasks.clear()

    with app.test_client() as test_client:
        yield test_client

    tasks.clear()


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TaskFlow" in response.data


def test_add_task(client):
    response = client.post(
        "/tasks/add",
        data={
            "title": "Learn Docker",
            "description": "Understand containers"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Learn Docker"


def test_complete_task(client):
    client.post(
        "/tasks/add",
        data={"title": "Learn Jenkins"}
    )

    task_id = tasks[0]["id"]

    response = client.post(
        f"/tasks/{task_id}/toggle",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert tasks[0]["completed"] is True


def test_edit_task(client):
    client.post(
        "/tasks/add",
        data={"title": "Old title"}
    )

    task_id = tasks[0]["id"]

    response = client.post(
        f"/tasks/{task_id}/edit",
        data={
            "title": "Updated title",
            "description": "Updated description"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert tasks[0]["title"] == "Updated title"


def test_delete_task(client):
    client.post(
        "/tasks/add",
        data={"title": "Delete me"}
    )

    task_id = tasks[0]["id"]

    response = client.post(
        f"/tasks/{task_id}/delete",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert len(tasks) == 0
