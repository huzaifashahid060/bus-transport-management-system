from data import (load_route, load_booking,
                  save_route_data, save_booking_data)

CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")

routes = load_route()        # list of dictionaries
bookings = load_booking()    # list of dictionaries
booking_ids = set()
for booking in bookings:
    booking_ids.add(booking["booking_id"])


def save_all():
    save_route_data(routes)
    save_booking_data(bookings)


def find_route(route_id):
    for route in routes:
        if route["route_id"] == route_id:
            return route
    return None


def seat_status(route):
    if route["available_seats"] == 0:
        return "Fully Booked"
    if route["available_seats"] == route["total_seats"]:
        return "Available"
    return "Partially Booked"


def new_booking_id():
    number = 1001
    while "B" + str(number) in booking_ids:
        number += 1
    return "B" + str(number)


def route_row(route):
    return {
        "Route": route["route_id"],
        "Journey": route["departure_city"] + " -> " + route["destination_city"],
        "Depart": route["departure_time"],
        "Fare (Rs.)": route["ticket_price"],
        "Seats": str(route["available_seats"]) + "/" + str(route["total_seats"]),
        "Status": seat_status(route),
    }


def get_routes(only_available=False):
    rows = []
    for route in routes:
        if only_available and route["available_seats"] == 0:
            continue
        rows.append(route_row(route))
    return rows


def search_routes(term):
    term = term.strip().lower()
    rows = []
    if term == "":
        return rows
    for route in routes:
        if (term == route["route_id"].lower()
                or term == route["departure_city"].lower()
                or term == route["destination_city"].lower()):
            rows.append(route_row(route))
    return rows


def get_route_ids():
    return [route["route_id"] for route in routes]


def book_ticket(name, age, route_id, seats):
    name = name.strip()
    if name == "":
        return False, "Name cannot be empty.", None

    try:
        age = int(age)
    except (TypeError, ValueError):
        return False, "Age must be a whole number.", None
    if age <= 0:
        return False, "Age must be a positive number.", None

    route = find_route(route_id)
    if route is None:
        return False, "Route not found.", None

    try:
        seats = int(seats)
    except (TypeError, ValueError):
        return False, "Seats must be a whole number.", None
    if seats <= 0:
        return False, "Seats must be greater than zero.", None
    if seats > route["available_seats"]:
        return False, "Only " + str(route["available_seats"]) + " seats available on this route.", None

    booking_id = new_booking_id()
    booking_ids.add(booking_id)
    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route_id,
        "seats": seats,
        "total_fare": route["ticket_price"] * seats,
        "status": "Confirmed",
    }
    bookings.append(booking)
    route["available_seats"] -= seats
    save_all()
    return True, "Booking confirmed!", booking


def get_booking_details(booking):
    route = find_route(booking["route_id"])
    return {
        "Route": route["route_id"] + " (" + route["departure_city"] + " -> " + route["destination_city"] + ")",
        "Fare per seat": route["ticket_price"],
    }


def get_bookings():
    return list(bookings)


def cancel_booking(booking_id):
    booking_id = booking_id.strip().upper()
    found = None
    for booking in bookings:
        if booking["booking_id"] == booking_id:
            found = booking
            break

    if found is None:
        return False, "Booking ID not found."
    if found["status"] != "Confirmed":
        return False, "This booking is already cancelled."

    route = find_route(found["route_id"])
    route["available_seats"] += found["seats"]
    found["status"] = "Cancelled"
    save_all()
    return True, ("Booking " + booking_id + " has been cancelled. Seats restored: "
                  + str(found["seats"]) + ". Route " + route["route_id"]
                  + " now has " + str(route["available_seats"]) + " available seats.")


def get_seat_availability():
    rows = []
    for route in routes:
        rows.append({
            "label": route["route_id"] + " " + route["departure_city"] + " -> " + route["destination_city"],
            "status": seat_status(route),
            "available": route["available_seats"],
            "total": route["total_seats"],
        })
    return rows


def generate_report():
    confirmed = 0
    cancelled = 0
    reserved_seats = 0
    revenue = 0
    fully_booked = 0

    for booking in bookings:
        if booking["status"] == "Confirmed":
            confirmed += 1
            reserved_seats += booking["seats"]
            revenue += booking["total_fare"]
        else:
            cancelled += 1

    for route in routes:
        if route["available_seats"] == 0:
            fully_booked += 1

    return {
        "total": len(bookings),
        "confirmed": confirmed,
        "cancelled": cancelled,
        "reserved_seats": reserved_seats,
        "revenue": revenue,
        "fully_booked": fully_booked,
    }


def get_schedule():
    schedule = []
    for city in CITIES:
        lines = []
        for route in routes:
            if route["departure_city"] == city:
                lines.append(route["route_id"] + " -> " + route["destination_city"]
                             + " | " + route["departure_time"])
        schedule.append((city, lines))
    return schedule
