# Smart Bus Ticket Booking & Reservation System

A beginner-friendly Python 3 console application for a small bus service.
You can browse routes, search, book seats, cancel bookings, check seat
availability and view a report - all from a text menu.

## Requirements
- Python 3.8 or newer
- Built-in Python only (no packages to install)

## How to run
Open a terminal in this folder and run:

    py main.py          (Windows)
    python3 main.py     (Mac / Linux)

## Menu guide
| Option | What it does |
|--------|--------------|
| 1. View Available Routes | Lists all routes with fare and seats. You can hide fully booked routes. |
| 2. Search for a Route | Search by route ID (e.g. R101) or by city. Not case-sensitive. |
| 3. Book a Ticket | Asks for name, age, route ID and seats. Checks everything, then shows the booking. |
| 4. View My Bookings | Lists every booking, including cancelled ones. |
| 5. Cancel a Booking | Cancels a Confirmed booking by ID and gives its seats back (only once). |
| 6. View Seat Availability | Shows seats left vs. total, with Available / Partially Booked / Fully Booked. |
| 7. Generate Booking Report | Shows totals and confirmed revenue, then the route schedule by departure city. |
| 8. Exit | Ends the program. |

## Sample workflow
1. Choose **1** to see the five routes.
2. Choose **3**, enter `Ahmed`, `24`, `R101`, `2` -> booking B1001 for Rs. 2400. R101 drops to 38 seats.
3. Choose **5**, enter `B1001` -> booking cancelled, R101 goes back to 40 seats.
4. Choose **5** and `B1001` again -> rejected, seats are not restored twice.
5. Choose **7** -> report shows 1 total, 0 confirmed, 1 cancelled, Rs. 0 revenue.

A full example run is saved in `sample_output.txt`.

## Business rules
- Name must not be empty; age and seats must be whole numbers above zero.
- Route must exist; requested seats must not be more than the seats available.
- Total fare = ticket price x seats.
- Booking IDs are unique (tracked in a set).
- Seats change only after every check passes.
- Only Confirmed bookings can be cancelled, and seats are restored once.
- Cancelled bookings stay in the history but are not counted in seats reserved or revenue.

## Storage limitation
All data is kept **in memory**. When you close the program, every booking is
lost and the routes return to their starting values. There is no database or
file saving in `main.py`.

## Constraints
- Python 3 console app, built-in features only.
- No GUI, database, payment, or external library in `main.py`.

## Python concepts used in main.py
`print()`/`input()`, variables, lists, dictionaries, a tuple (`CITIES`), a set
(`booking_ids`), `if/elif/else`, nested conditions, `for` loops, nested loops
(report and schedule), `for-else` (search and cancel), `break`, `continue`
(skip full routes, restart after bad menu input), `enumerate()`, `while`, and
input validation with `try/except`.

## Files
| File | Purpose |
|------|---------|
| `main.py` | The complete console application (main deliverable). |
| `README.md` | This guide. |
| `test_cases.txt` | 15 test scenarios with expected and actual results. |
| `sample_output.txt` | A real run of the program (use it as a guide for your screenshots). |

### Optional extra: Streamlit web interface
These files are an extra and are not needed for `main.py`:
`app.py` (screens), `backend.py` (logic), `data.py` (file loading/saving),
`route.json` and `booking.json` (saved data).

    py -m pip install streamlit
    py -m streamlit run app.py

Unlike `main.py`, the Streamlit version **saves** routes and bookings in the
JSON files, so data is kept after you close it.
