from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


@app.route('/')
def welcome():
    """Serves a JSON welcome message at the root route."""
    return jsonify({"message": "Welcome to the Event Management API"}), 200


@app.route('/events', methods=['GET'])
def get_events():
    """Returns a JSON array of all events."""
    return jsonify([event.to_dict() for event in events]), 200


@app.route('/events', methods=['POST'])
def add_event():
    """Create a new event from JSON input."""
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Missing 'title' in request body"}), 400

    new_id = events[-1].id + 1 if events else 1
    new_event = Event(new_id, data['title'])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201


@app.route('/events/<int:id>', methods=['PATCH'])
def update_event(id):
    """Update the title of an event."""
    event = next((e for e in events if e.id == id), None)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Missing 'title' in request body"}), 400

    event.title = data['title']
    return jsonify(event.to_dict()), 200


@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    """Remove an event from the list."""
    global events
    event = next((e for e in events if e.id == id), None)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events = [e for e in events if e.id != id]
    return jsonify({"message": "Event deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)