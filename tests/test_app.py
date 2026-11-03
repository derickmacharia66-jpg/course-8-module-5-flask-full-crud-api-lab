import pytest
from app import app, events, Event


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_welcome_message(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data


def test_get_events(client):
    response = client.get('/events')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all('id' in e and 'title' in e for e in data)


def test_post_event_created(client):
    response = client.post('/events', json={"title": "Hackathon"})
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == "Hackathon"
    assert 'id' in data


def test_post_event_missing_title(client):
    response = client.post('/events', json={})
    assert response.status_code == 400


def test_patch_event(client):
    post_res = client.post('/events', json={"title": "Draft Title"})
    event_id = post_res.get_json()['id']

    response = client.patch(f'/events/{event_id}', json={"title": "Hackathon 2025"})
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == "Hackathon 2025"


def test_patch_event_not_found(client):
    response = client.patch('/events/9999', json={"title": "Doesn't matter"})
    assert response.status_code == 404


def test_delete_event(client):
    post_res = client.post('/events', json={"title": "To Delete"})
    event_id = post_res.get_json()['id']

    response = client.delete(f'/events/{event_id}')
    assert response.status_code == 200

    get_res = client.get('/events')
    ids = [e['id'] for e in get_res.get_json()]
    assert event_id not in ids


def test_delete_event_not_found(client):
    response = client.delete('/events/9999')
    assert response.status_code == 404