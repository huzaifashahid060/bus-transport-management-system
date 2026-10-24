from data import (load_route, load_booking)
CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")
routes = load_route() 
bookings = load_booking()
booking_ids = {booking["booking_id"] for booking in bookings}

def find_route(route_id):
    for route in routes:
        if route["route_id"] == route_id:
            return route
    return None


def seat_status(route):
    """Return Available, Partially Booked or Fully Booked for one route."""
    if route["available_seats"] == 0:
        return "Fully Booked"
    elif route["available_seats"] == route["total_seats"]:
        return "Available"
    else:
        return "Partially Booked"


def read_positive_int(prompt):
    """Ask for a whole number greater than zero. Return None if input is invalid."""
    text = input(prompt).strip()
    try:
        number = int(text)
    except ValueError:
        return None
    if number <= 0:
        return None
    return number


def yes_no(prompt):
    """Ask a y/n question and return True for yes."""
    return input(prompt).strip().lower() == "y"


def new_booking_id():
    """Create a booking ID that is not already in the booking_ids set."""
    number = 1001
    while "B" + str(number) in booking_ids:
        number += 1
    return "B" + str(number)



def show_menu():
    print()
    print("SMART BUS RESERVATION SYSTEM")
    print("================================")
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. Exit")
    print("================================")


def view_routes():
    """Option 1 - list all routes, optionally only those with seats left."""
    only_available = yes_no("Show only routes with seats available? (y/n): ")

    print("\nAVAILABLE BUS ROUTES")
    print("No.  Route  Journey                       Depart     Fare      Seats")
    shown = 0
    for number, route in enumerate(routes, start=1):
        if only_available and route["available_seats"] == 0:
            continue  

        journey = route["departure_city"] + " -> " + route["destination_city"]
        seats = str(route["available_seats"]) + "/" + str(route["total_seats"])
        if route["available_seats"] == 0:
            seats = seats + "  Fully Booked"
        print(f"{number:<4} {route['route_id']:<6} {journey:<29} "
              f"{route['departure_time']:<10} Rs.{route['ticket_price']:<6} {seats}")
        shown += 1

    if shown == 0:
        print("No routes to show.")


def search_route():
    """Option 2 - search by route ID or by city (case-insensitive)."""
    term = input("Search by route ID or city: ").strip().lower()
    if term == "":
        print("Please type a route ID or a city name.")
        return

    for route in routes:
        if route["route_id"].lower() == term:
            print_route_line(route)
            break
    else:
        matches = 0
        for route in routes:
            if term == route["departure_city"].lower() or term == route["destination_city"].lower():
                print_route_line(route)
                matches += 1
        if matches == 0:
            print("No matching route found.")


def print_route_line(route):
    print(route["route_id"], "|", route["departure_city"], "->", route["destination_city"],
          "| Rs.", route["ticket_price"], "|", route["available_seats"], "seats available")


def book_ticket():
    """Option 3 - validate everything first, then create the booking."""
    print("\nBOOK A TICKET")
    name = input("Passenger name: ").strip()
    age = read_positive_int("Passenger age: ")
    route_id = input("Route ID (example R101): ").strip().upper()
    seats_text = input("Number of seats: ").strip()

    if name == "":
        print("Error: passenger name cannot be empty.")
        return
    if age is None:
        print("Error: age must be a whole number greater than zero.")
        return

    route = find_route(route_id)
    if route is None:
        print("Error: route", route_id, "does not exist.")
        return

    try:
        seats = int(seats_text)
    except ValueError:
        seats = 0
    if seats <= 0:
        print("Error: number of seats must be a whole number greater than zero.")
        return
    if seats > route["available_seats"]:
        print("Error: only", route["available_seats"], "seats are available on", route_id + ".")
        return

    # --- all checks passed: create the record, then update seats ---
    booking_id = new_booking_id()
    booking_ids.add(booking_id)
    total_fare = route["ticket_price"] * seats

    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route_id,
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed",
    }
    bookings.append(booking)
    route["available_seats"] -= seats

    print("\nBooking confirmed!")
    print("Booking ID:", booking_id)
    print("Passenger:", name)
    print("Route:", route_id, "(" + route["departure_city"] + " -> " + route["destination_city"] + ")")
    print("Seats booked:", seats)
    print("Fare per seat: Rs.", route["ticket_price"])
    print("Total fare: Rs.", total_fare)
    print("Status: Confirmed")


def view_bookings():
    """Option 4 - show every booking, including cancelled ones."""
    if len(bookings) == 0:
        print("No bookings found.")
        return

    print("\nMY BOOKINGS")
    for number, booking in enumerate(bookings, start=1):
        print(number, "|", booking["booking_id"], "|", booking["passenger_name"],
              "| Route", booking["route_id"], "| Seats:", booking["seats"],
              "| Rs.", booking["total_fare"], "|", booking["status"])


def cancel_booking():
    """Option 5 - cancel a Confirmed booking and restore its seats once."""
    booking_id = input("Enter booking ID to cancel: ").strip().upper()

    for booking in bookings:
        if booking["booking_id"] == booking_id:
            found = booking
            break
    else:
        print("Booking", booking_id, "was not found.")
        return

    if found["status"] != "Confirmed":
        print("Booking", booking_id, "is already cancelled. No seats were restored.")
    else:
        route = find_route(found["route_id"])
        route["available_seats"] += found["seats"]  
        found["status"] = "Cancelled"               

        print("Booking", booking_id, "has been cancelled.")
        print("Seats restored:", found["seats"])
        print("Route", route["route_id"], "available seats:", route["available_seats"])


def view_seat_availability():
    """Option 6 - available seats versus total capacity for each route."""
    only_available = yes_no("Show only routes with seats available? (y/n): ")

    print("\nSEAT AVAILABILITY")
    shown = 0
    for route in routes:
        if only_available and route["available_seats"] == 0:
            continue
        print(route["route_id"], "|", route["departure_city"], "->", route["destination_city"],
              "|", route["available_seats"], "of", route["total_seats"], "seats |", seat_status(route))
        shown += 1

    if shown == 0:
        print("No routes with seats available.")


def generate_report():
    """Option 7 - totals for bookings, seats, revenue and full routes."""
    total_bookings = len(bookings)
    confirmed_count = 0
    cancelled_count = 0
    reserved_seats = 0
    confirmed_revenue = 0
    fully_booked_routes = 0

    for booking in bookings:
        if booking["status"] == "Confirmed":
            confirmed_count += 1
        else:
            cancelled_count += 1

    print("\nCONFIRMED BOOKINGS BY ROUTE")
    any_confirmed = False
    for route in routes:
        route_seats = 0
        route_revenue = 0
        for booking in bookings:
            if booking["route_id"] == route["route_id"] and booking["status"] == "Confirmed":
                route_seats += booking["seats"]
                route_revenue += booking["total_fare"]
        if route_seats > 0:
            print(route["route_id"], "|", route_seats, "seats | Rs.", format(route_revenue, ","))
            any_confirmed = True
        reserved_seats += route_seats
        confirmed_revenue += route_revenue

        if route["available_seats"] == 0:
            fully_booked_routes += 1

    if not any_confirmed:
        print("No confirmed bookings.")

    print("\nBOOKING REPORT")
    print("Total bookings created:", total_bookings)
    print("Confirmed bookings:", confirmed_count)
    print("Cancelled bookings:", cancelled_count)
    print("Seats currently reserved:", reserved_seats)
    print("Confirmed revenue: Rs.", format(confirmed_revenue, ","))
    print("Fully booked routes:", fully_booked_routes)

    show_schedule()


def show_schedule():
    """Route schedule grouped by departure city (nested loops)."""
    print("\nROUTE SCHEDULE BY DEPARTURE CITY")
    for city in CITIES:
        print(city)
        has_departures = False
        for route in routes:
            if route["departure_city"] == city:
                print("  ", route["route_id"], "->", route["destination_city"],
                      "|", route["departure_time"])
                has_departures = True
        if not has_departures:
            print("   No scheduled departures.")



def main():
    print("Welcome to the Smart Bus Reservation System!")

    while True:
        show_menu()
        choice_text = input("Enter your choice: ").strip()

        try:
            choice = int(choice_text)
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 8.")
            continue

        if choice == 1:
            view_routes()
        elif choice == 2:
            search_route()
        elif choice == 3:
            book_ticket()
        elif choice == 4:
            view_bookings()
        elif choice == 5:
            cancel_booking()
        elif choice == 6:
            view_seat_availability()
        elif choice == 7:
            generate_report()
        elif choice == 8:
            print("Thank you for using Smart Bus. Goodbye!")
            break
        else:
            print("Unsupported choice. Please enter a number from 1 to 8.")


main()
