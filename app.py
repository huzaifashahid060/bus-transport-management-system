"""
app.py - Streamlit UI only. All logic lives in backend.py.
Run with:  py -m streamlit run app.py
"""
import streamlit as st
import backend

st.set_page_config(page_title="Smart Bus Reservation", page_icon="🚌")
st.title("🚌 Smart Bus Reservation System")

menu = st.sidebar.radio("Menu", [
    "1. View Available Routes",
    "2. Search for a Route",
    "3. Book a Ticket",
    "4. View My Bookings",
    "5. Cancel a Booking",
    "6. View Seat Availability",
    "7. Generate Booking Report",
    "8. Route Schedule",
])

# ---------- 1. VIEW ROUTES ----------
if menu.startswith("1"):
    st.header("Available Bus Routes")
    only_available = st.checkbox("Show only routes with seats left")
    rows = backend.get_routes(only_available)
    if rows:
        st.table(rows)
    else:
        st.info("No routes to show.")

# ---------- 2. SEARCH ----------
elif menu.startswith("2"):
    st.header("Search for a Route")
    term = st.text_input("Route ID or city")
    if term.strip():
        rows = backend.search_routes(term)
        if rows:
            st.table(rows)
        else:
            st.warning("No matching route found.")

# ---------- 3. BOOK ----------
elif menu.startswith("3"):
    st.header("Book a Ticket")
    name = st.text_input("Passenger name")
    age = st.number_input("Passenger age", min_value=0, step=1, value=0)
    route_id = st.selectbox("Route", backend.get_route_ids())
    seats = st.number_input("Number of seats", min_value=0, step=1, value=0)

    if st.button("Confirm Booking"):
        ok, message, booking = backend.book_ticket(name, age, route_id, seats)
        if ok:
            details = backend.get_booking_details(booking)
            st.success(message)
            st.write("**Booking ID:**", booking["booking_id"])
            st.write("**Passenger:**", booking["passenger_name"])
            st.write("**Route:**", details["Route"])
            st.write("**Seats booked:**", booking["seats"])
            st.write("**Fare per seat:** Rs.", details["Fare per seat"])
            st.write("**Total fare:** Rs.", booking["total_fare"])
            st.write("**Status:**", booking["status"])
        else:
            st.error(message)

# ---------- 4. VIEW BOOKINGS ----------
elif menu.startswith("4"):
    st.header("My Bookings")
    all_bookings = backend.get_bookings()
    if all_bookings:
        st.table(all_bookings)
    else:
        st.info("No bookings found.")

# ---------- 5. CANCEL ----------
elif menu.startswith("5"):
    st.header("Cancel a Booking")
    cancel_id = st.text_input("Booking ID (example: B1001)")
    if st.button("Cancel Booking"):
        ok, message = backend.cancel_booking(cancel_id)
        if ok:
            st.success(message)
        else:
            st.error(message)

# ---------- 6. SEAT AVAILABILITY ----------
elif menu.startswith("6"):
    st.header("Seat Availability")
    for item in backend.get_seat_availability():
        st.write("**" + item["label"] + "** — " + item["status"])
        st.progress(item["available"] / item["total"],
                    text=str(item["available"]) + " of " + str(item["total"]) + " seats free")

# ---------- 7. REPORT ----------
elif menu.startswith("7"):
    st.header("Booking Report")
    report = backend.generate_report()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total bookings", report["total"])
    col2.metric("Confirmed", report["confirmed"])
    col3.metric("Cancelled", report["cancelled"])

    col4, col5, col6 = st.columns(3)
    col4.metric("Seats reserved", report["reserved_seats"])
    col5.metric("Confirmed revenue", "Rs. " + format(report["revenue"], ","))
    col6.metric("Fully booked routes", report["fully_booked"])

# ---------- 8. SCHEDULE ----------
elif menu.startswith("8"):
    st.header("Route Schedule by Departure City")
    for city, lines in backend.get_schedule():
        st.subheader(city)
        if lines:
            for line in lines:
                st.write(line)
        else:
            st.caption("No scheduled departures.")
