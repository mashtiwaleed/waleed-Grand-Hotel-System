import json
import os
import random
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "hotel_data.json")


class HotelAccount:
    def __init__(
        self,
        name,
        reservation_number,
        password,
        room_type,
        nights,
        breakfast,
        total_bill=0,
        history=None,
        checked_in=False,
        checked_out=False,
        rating=None,
        services=None
    ):
        self.name = name
        self.reservation_number = reservation_number
        self.password = password
        self.room_type = room_type
        self.nights = nights
        self.breakfast = breakfast
        self.total_bill = total_bill
        self.checked_in = checked_in
        self.checked_out = checked_out
        self.rating = rating
        self.services = services if services is not None else []
        self.history = history if history is not None else []

    def add_history(self, text):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{time} - {text}")

    def add_charge(self, amount, reason="Extra charge"):
        if amount <= 0:
            print("Invalid amount.")
        else:
            self.total_bill += amount
            self.add_history(f"{reason}: {amount} CZK")
            print(f"Charge added successfully. Total bill: {self.total_bill} CZK")

    def cancel_charge(self, amount):
        if amount <= 0:
            print("Invalid amount.")
        elif amount > self.total_bill:
            print("You cannot cancel more than the total bill.")
        else:
            self.total_bill -= amount
            self.add_history(f"Cancelled charge: {amount} CZK")
            print(f"Charge cancelled successfully. Total bill: {self.total_bill} CZK")

    def add_service(self, service_name, price):
        if service_name in self.services:
            print("This service is already booked.")
        else:
            self.services.append(service_name)
            self.total_bill += price
            self.add_history(f"Added service: {service_name} - {price} CZK")
            print(f"{service_name} added successfully. Total bill: {self.total_bill} CZK")

    def cancel_service(self, service_name, price):
        if service_name not in self.services:
            print("This service is not booked.")
        else:
            self.services.remove(service_name)
            self.total_bill -= price
            self.add_history(f"Cancelled service: {service_name} - {price} CZK")
            print(f"{service_name} cancelled successfully. Total bill: {self.total_bill} CZK")

    def show_info(self):
        print("\n----- Reservation Information -----")
        print(f"Name: {self.name}")
        print(f"Reservation Number: {self.reservation_number}")
        print(f"Room Type: {self.room_type}")
        print(f"Nights: {self.nights}")
        print(f"Breakfast: {self.breakfast}")
        print(f"Total Bill: {self.total_bill} CZK")
        print(f"Checked In: {self.checked_in}")
        print(f"Checked Out: {self.checked_out}")
        print(f"Rating: {self.rating if self.rating else 'Not rated yet'}")

        if self.services:
            print("Services:", ", ".join(self.services))
        else:
            print("Services: No services booked")

    def show_history(self):
        print("\n----- Transaction History -----")
        if not self.history:
            print("No transactions yet.")
        else:
            for item in self.history:
                print(item)

    def check_in(self):
        if self.checked_in:
            print("Guest is already checked in.")
        else:
            self.checked_in = True
            self.add_history("Guest checked in")
            print("Check-in successful.")

    def check_out(self):
        if not self.checked_in:
            print("Guest must check in first.")
        elif self.checked_out:
            print("Guest is already checked out.")
        else:
            self.checked_out = True
            self.add_history("Guest checked out")
            print("Check-out successful.")

    def add_rating(self, rating):
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
        else:
            self.rating = rating
            self.add_history(f"Hotel rated {rating}/5")
            print("Thank you for your rating.")


def load_rooms():
    rooms = {}

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

            for room_num, room_data in data.items():
                rooms[room_num] = HotelAccount(
                    room_data["name"],
                    room_data["reservation_number"],
                    room_data["password"],
                    room_data.get("room_type", "Standard Room"),
                    room_data.get("nights", 1),
                    room_data.get("breakfast", "No"),
                    room_data.get("total_bill", room_data.get("paid_amount", 0)),
                    room_data.get("history", []),
                    room_data.get("checked_in", False),
                    room_data.get("checked_out", False),
                    room_data.get("rating", None),
                    room_data.get("services", [])
                )

    return rooms


def save_rooms(rooms):
    data = {}

    for room_num, room in rooms.items():
        data[room_num] = {
            "name": room.name,
            "reservation_number": room.reservation_number,
            "password": room.password,
            "room_type": room.room_type,
            "nights": room.nights,
            "breakfast": room.breakfast,
            "total_bill": room.total_bill,
            "checked_in": room.checked_in,
            "checked_out": room.checked_out,
            "rating": room.rating,
            "services": room.services,
            "history": room.history
        }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def generate_room_number(rooms):
    while True:
        number = str(random.randint(10000, 99999))
        if number not in rooms:
            return number


def choose_room_type():
    print("\nChoose room type:")
    print("1. Standard Room - 800 CZK")
    print("2. Deluxe Room - 1200 CZK")
    print("3. Suite Room - 2000 CZK")

    choice = input("Choose room type: ")

    if choice == "1":
        return "Standard Room", 800
    elif choice == "2":
        return "Deluxe Room", 1200
    elif choice == "3":
        return "Suite Room", 2000
    else:
        print("Invalid room type.")
        return None, None


def create_reservation(rooms):
    name = input("Enter full name: ")
    password = input("Create password: ")

    room_type, room_price = choose_room_type()

    if room_type is None:
        return

    nights = int(input("How many nights? "))

    print("\nBreakfast option:")
    print("1. With breakfast - 150 CZK per night")
    print("2. Without breakfast")

    breakfast_choice = input("Choose option: ")

    if breakfast_choice == "1":
        breakfast = "Yes"
        breakfast_price = 150 * nights
    else:
        breakfast = "No"
        breakfast_price = 0

    total_bill = (room_price * nights) + breakfast_price
    room_number = generate_room_number(rooms)

    rooms[room_number] = HotelAccount(
        name,
        room_number,
        password,
        room_type,
        nights,
        breakfast,
        total_bill
    )

    rooms[room_number].add_history(
        f"Booked {room_type} for {nights} nights - {room_price * nights} CZK"
    )

    if breakfast == "Yes":
        rooms[room_number].add_history(f"Breakfast added - {breakfast_price} CZK")

    save_rooms(rooms)

    print("\nReservation created successfully.")
    print(f"Your room number is: {room_number}")
    print(f"Room type: {room_type}")
    print(f"Nights: {nights}")
    print(f"Breakfast: {breakfast}")
    print(f"Total bill: {total_bill} CZK")


def login(rooms):
    room_number = input("Enter room number: ")
    password = input("Enter password: ")

    if room_number not in rooms:
        print("Room not found.")
        return None

    room = rooms[room_number]

    if room.password != password:
        print("Wrong password.")
        return None

    print(f"\nWelcome, {room.name}!")
    return room


def change_room(rooms, guest):
    new_room_number = input("Enter new room number: ")

    if new_room_number in rooms:
        print("This room is already reserved.")
        return

    old_room_number = guest.reservation_number

    del rooms[old_room_number]

    guest.reservation_number = new_room_number
    rooms[new_room_number] = guest

    guest.add_history(f"Room changed from {old_room_number} to {new_room_number}")
    save_rooms(rooms)

    print("Room changed successfully.")


def restaurant_menu(room, rooms):
    while True:
        print("\n----- Hotel Restaurant Menu -----")
        print("1. Asian Food")
        print("2. Italian Food")
        print("3. French Food")
        print("4. Back")

        choice = input("Choose food section: ")

        if choice == "1":
            print("\nAsian Food:")
            print("1. Sushi - 250 CZK")
            print("2. Noodles - 180 CZK")
            print("3. Fried Rice - 160 CZK")

            food = input("Choose item: ")

            if food == "1":
                room.add_charge(250, "Ordered Sushi")
            elif food == "2":
                room.add_charge(180, "Ordered Noodles")
            elif food == "3":
                room.add_charge(160, "Ordered Fried Rice")
            else:
                print("Invalid food choice.")

            save_rooms(rooms)

        elif choice == "2":
            print("\nItalian Food:")
            print("1. Pizza - 220 CZK")
            print("2. Pasta - 190 CZK")
            print("3. Lasagna - 240 CZK")

            food = input("Choose item: ")

            if food == "1":
                room.add_charge(220, "Ordered Pizza")
            elif food == "2":
                room.add_charge(190, "Ordered Pasta")
            elif food == "3":
                room.add_charge(240, "Ordered Lasagna")
            else:
                print("Invalid food choice.")

            save_rooms(rooms)

        elif choice == "3":
            print("\nFrench Food:")
            print("1. Croissant - 80 CZK")
            print("2. French Onion Soup - 150 CZK")
            print("3. Steak Frites - 320 CZK")

            food = input("Choose item: ")

            if food == "1":
                room.add_charge(80, "Ordered Croissant")
            elif food == "2":
                room.add_charge(150, "Ordered French Onion Soup")
            elif food == "3":
                room.add_charge(320, "Ordered Steak Frites")
            else:
                print("Invalid food choice.")

            save_rooms(rooms)

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


def cancel_service_menu(room, rooms):
    while True:
        print("\n----- Cancel Hotel Service -----")
        print("1. Cancel Swimming Pool - 300 CZK")
        print("2. Cancel Gym Membership - 250 CZK")
        print("3. Cancel Spa Service - 600 CZK")
        print("4. Back")

        choice = input("Choose service to cancel: ")

        if choice == "1":
            room.cancel_service("Swimming Pool Service", 300)
            save_rooms(rooms)

        elif choice == "2":
            room.cancel_service("Gym Membership", 250)
            save_rooms(rooms)

        elif choice == "3":
            room.cancel_service("Spa Service", 600)
            save_rooms(rooms)

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


def hotel_services(room, rooms):
    while True:
        print("\n----- Hotel Services -----")
        print("1. Swimming Pool - 300 CZK")
        print("2. Gym Membership - 250 CZK")
        print("3. Spa Service - 600 CZK")
        print("4. Cancel service")
        print("5. Back")

        choice = input("Choose service: ")

        if choice == "1":
            room.add_service("Swimming Pool Service", 300)
            save_rooms(rooms)

        elif choice == "2":
            room.add_service("Gym Membership", 250)
            save_rooms(rooms)

        elif choice == "3":
            room.add_service("Spa Service", 600)
            save_rooms(rooms)

        elif choice == "4":
            cancel_service_menu(room, rooms)

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


def reservation_menu(rooms, room):
    while True:
        print(f"\n----- Reservation Menu: {room.name} -----")
        print("1. Add extra charge")
        print("2. Cancel charge")
        print("3. Check total bill")
        print("4. Show reservation information")
        print("5. Show transaction history")
        print("6. Change room")
        print("7. Change guest name")
        print("8. Restaurant menu")
        print("9. Hotel services")
        print("10. Check-in")
        print("11. Check-out")
        print("12. Rate hotel")
        print("13. Back to main menu")

        choice = input("Choose an option: ")

        if choice == "1":
            amount = float(input("Enter charge amount: "))
            room.add_charge(amount)
            save_rooms(rooms)

        elif choice == "2":
            amount = float(input("Enter amount to cancel: "))
            room.cancel_charge(amount)
            save_rooms(rooms)

        elif choice == "3":
            print(f"Total bill: {room.total_bill} CZK")

        elif choice == "4":
            room.show_info()

        elif choice == "5":
            room.show_history()

        elif choice == "6":
            change_room(rooms, room)

        elif choice == "7":
            new_name = input("Enter new guest name: ")
            room.name = new_name
            room.add_history(f"Guest name changed to {new_name}")
            save_rooms(rooms)
            print("Guest name updated successfully.")

        elif choice == "8":
            restaurant_menu(room, rooms)

        elif choice == "9":
            hotel_services(room, rooms)

        elif choice == "10":
            room.check_in()
            save_rooms(rooms)

        elif choice == "11":
            room.check_out()
            save_rooms(rooms)

        elif choice == "12":
            try:
                rating = float(input("Rate hotel from 1 to 5: "))
                room.add_rating(rating)
                save_rooms(rooms)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "13":
            break

        else:
            print("Invalid choice.")


def admin_panel(rooms):
    admin_password = input("Enter admin password: ")

    if admin_password != "admin4u":
        print("Wrong admin password.")
        return

    while True:
        print("\n----- Admin Panel -----")
        print("1. Show all reservations")
        print("2. Search reservation")
        print("3. Delete reservation")
        print("4. Show total hotel bills")
        print("5. Back to main menu")

        choice = input("Choose an option: ")

        if choice == "1":
            if not rooms:
                print("No reservations found.")
            else:
                for room_num, room in rooms.items():
                    print(
                        f"{room_num} - {room.name} - {room.room_type} - Total Bill: {room.total_bill} CZK"
                    )

        elif choice == "2":
            room_num = input("Enter room number: ")

            if room_num in rooms:
                rooms[room_num].show_info()
            else:
                print("Reservation not found.")

        elif choice == "3":
            room_num = input("Enter room number to delete: ")

            if room_num in rooms:
                del rooms[room_num]
                save_rooms(rooms)
                print("Reservation deleted successfully.")
            else:
                print("Reservation not found.")

        elif choice == "4":
            total = 0
            for room in rooms.values():
                total += room.total_bill

            print(f"Total hotel bills: {total} CZK")

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


def main():
    rooms = load_rooms()

    print("===================================")
    print("Welcome to Waleed Grand Hotel")
    print("Your trusted Python hotel system")
    print("===================================")

    while True:
        print("\n----- Main Menu -----")
        print("1. Create new reservation")
        print("2. Login to reservation")
        print("3. Admin panel")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_reservation(rooms)

        elif choice == "2":
            room = login(rooms)
            if room:
                reservation_menu(rooms, room)

        elif choice == "3":
            admin_panel(rooms)

        elif choice == "4":
            save_rooms(rooms)
            print("Thank you for using Waleed Grand Hotel.")
            break

        else:
            print("Invalid choice.")


main()