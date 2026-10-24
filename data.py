import json


def load_json(filename):

    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json(filename, data):
    """Write a list to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_route():
    return load_json("route.json")


def load_booking():
    return load_json("booking.json")


def save_route_data(routes):
    save_json("route.json", routes)


def save_booking_data(bookings):
    save_json("booking.json", bookings)
