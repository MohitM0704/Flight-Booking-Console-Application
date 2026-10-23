from abc import ABC, abstractmethod


class Passenger(ABC):

    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    @abstractmethod
    def get_discount(self):
        pass

    def get_passenger_type(self):
        pass


class RegularPassenger(Passenger):

    def get_discount(self):
        return 0.0

    def get_passenger_type(self):
        return "Regular"


class StudentPassenger(Passenger):

    def get_discount(self):
        return 0.10

    def get_passenger_type(self):
        return "Student"


class Flight:

    def __init__(self, code, airline, source, destination,
                 seats, base_fare):
        self.__code = code
        self.__airline = airline
        self.__source = source
        self.__destination = destination
        self.__seats = seats
        self.__base_fare = base_fare

    def get_code(self):
        return self.__code

    def get_airline(self):
        return self.__airline

    def get_source(self):
        return self.__source

    def get_destination(self):
        return self.__destination

    def get_seats(self):
        return self.__seats

    def get_base_fare(self):
        return self.__base_fare

    def book_seats(self, count):
        if count <= self.__seats:
            self.__seats -= count
            return True
        return False

    def display_flight(self):
        print(
            self.__code, "|", self.__airline, "|",
            self.__source, "to", self.__destination,
            "| Seats:", self.__seats,
            "| Base Fare: Rs.", self.__base_fare
        )


class Booking:

    def __init__(self, booking_id, flight, passenger,
                 tickets, subtotal, discount, total):
        self.booking_id = booking_id
        self.flight = flight
        self.passenger = passenger
        self.tickets = tickets
        self.subtotal = subtotal
        self.discount = discount
        self.total = total

    def display_summary(self):
        print("\n========== BOOKING SUMMARY ==========")
        print("Booking ID:", self.booking_id)
        print("Flight Code:", self.flight.get_code())
        print("Airline:", self.flight.get_airline())
        print(
            "Route:", self.flight.get_source(),
            "to", self.flight.get_destination()
        )
        print("Passenger:", self.passenger.get_name())
        print("Age:", self.passenger.get_age())
        print("Passenger Type:", self.passenger.get_passenger_type())
        print("Number of Tickets:", self.tickets)
        print("Base Fare per Ticket: Rs.", self.flight.get_base_fare())
        print("Subtotal: Rs.", self.subtotal)
        print(
            "Discount (",
            int(self.passenger.get_discount() * 100),
            "%): Rs.", self.discount
        )
        print("Final Amount: Rs.", self.total)
        print("======================================")


class FlightBookingSystem:

    def __init__(self):
        self.flights = [
            Flight("PN101", "Air India", "Pune", "Delhi", 20, 4000),
            Flight("MB202", "IndiGo", "Mumbai", "Bengaluru", 30, 3500),
            Flight("PN303", "Akasa Air", "Pune", "Hyderabad", 25, 3000)
        ]

        self.bookings = []
        self.booking_counter = 1001

    def display_flights(self):
        print("\n========== AVAILABLE FLIGHTS ==========")
        for flight in self.flights:
            flight.display_flight()

    def find_flight(self, code):
        for flight in self.flights:
            if flight.get_code().upper() == code.upper():
                return flight
        return None

    def validate_booking(self, flight, name, age, tickets):
        if flight is None:
            print("Booking failed: Invalid flight code.")
            return False

        if not name.strip():
            print("Booking failed: Passenger name cannot be blank.")
            return False

        if age <= 0:
            print("Booking failed: Age must be greater than zero.")
            return False

        if tickets <= 0:
            print("Booking failed: Tickets must be greater than zero.")
            return False

        if tickets > flight.get_seats():
            print("Booking failed: Not enough seats available.")
            print("No booking was created. Available seats remain unchanged.")
            return False

        return True

    def calculate_fare(self, flight, passenger, tickets):
        subtotal = flight.get_base_fare() * tickets
        discount = subtotal * passenger.get_discount()
        total = subtotal - discount

        return subtotal, discount, total

    def book_flight(self):
        self.display_flights()

        code = input("\nEnter flight code: ").strip()
        flight = self.find_flight(code)

        name = input("Enter passenger name: ").strip()

        try:
            age = int(input("Enter age: "))
            if age <= 0:
                print("Booking failed: Age must be greater than zero.")
                return

            passenger_type = input(
                "Passenger type (Regular/Student): "
            ).strip().lower()

            if passenger_type == "regular":
                passenger = RegularPassenger(name, age)
            elif passenger_type == "student":
                passenger = StudentPassenger(name, age)
            else:
                print("Invalid passenger type! Enter Regular or Student.")
                return

            tickets = int(input("Enter number of tickets: "))

        except ValueError:
            print("Invalid input! Please enter valid numeric values.")
            return

        if not self.validate_booking(flight, name, age, tickets):
            return

        subtotal, discount, total = self.calculate_fare(
            flight, passenger, tickets
        )

        if flight.book_seats(tickets):
            booking_id = "BK" + str(self.booking_counter)
            self.booking_counter += 1

            booking = Booking(
                booking_id, flight, passenger,
                tickets, subtotal, discount, total
            )

            self.bookings.append(booking)

            print("\nBooking confirmed!")
            booking.display_summary()

    def view_booking(self):
        if not self.bookings:
            print("\nNo confirmed bookings found.")
        else:
            self.bookings[-1].display_summary()

    def run(self):
        print("Welcome to Kiran Air Booking")

        while True:
            print("\n========== MAIN MENU ==========")
            print("1. View Flights")
            print("2. Book Flight")
            print("3. View Booking")
            print("4. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.display_flights()

            elif choice == "2":
                self.book_flight()

            elif choice == "3":
                self.view_booking()

            elif choice == "4":
                print("Thank you for using Kiran Air Booking!")
                break

            else:
                print("Invalid choice! Please select from 1 to 4.")


system = FlightBookingSystem()
system.run()
