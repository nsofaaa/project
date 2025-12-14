from __future__ import annotations
from enum import Enum
import re
from tracemalloc import take_snapshot


class Type(Enum):
    SPORTSCAR = 'SPORTSCAR'
    CONVERTIBLE = 'CONVERTIBLE'
    VAN = 'VAN'
    OTHER = 'OTHER'

def get_price(vehicle) -> int:
    if isinstance(vehicle, Motorcycle):
        return 100
    elif hasattr(vehicle, 'type_of_car'):
        if vehicle.type_of_car == Type.OTHER:
            return 50
        elif vehicle.type_of_car == Type.VAN:
            return 100
        elif vehicle.type_of_car == Type.CONVERTIBLE:
            return 150
        elif vehicle.type_of_car == Type.SPORTSCAR:
            return 200
    return 0

def date_checker(date: str) -> bool:
    if not isinstance(date, str):
        return False

    pattern = re.compile(
        r"^((0[1-9])|([12][0-9])|(3[01]))\.((0[1-9])|(1[0-2]))\.(19[0-9]{2}|[2-9][0-9]{3})$"
    )
    return pattern.fullmatch(date) is not None


class Car:
    def __init__(self, make: str, model: str, year: int, type_of_car: Type) -> None:
        self.make = make
        self.model = model
        self.year = year
        self.type_of_car = type_of_car
        self.price = get_price(self)

        if not isinstance(type_of_car, Type):
            raise ValueError("Error")

    def __repr__(self) -> str:
        return f"Car({self.make}, {self.model}, {self.year}, {self.type_of_car})"

    def __hash__(self) -> int:
        return hash((self.make, self.model, self.year, self.type_of_car))

    def get_make(self) -> str:
        return self.make
    def get_model(self) -> str:
        return self.model
    def get_year(self) -> int:
        return self.year
    def get_type(self) -> Type:
        return self.type_of_car
    def get_price(self) -> int:
        return self.price


class Motorcycle:
    def __init__(self, make: str, model: str, year: int) -> None:
        self.make = make
        self.model = model
        self.year = year
        self.price = get_price(self)

    def __repr__(self) -> str:
        return f"Motorcycle({self.make}, {self.model}, {self.year})"

    def __hash__(self) -> int:
        return hash((self.make, self.model, self.year))

    def get_make(self) -> str:
        return self.make

    def get_model(self) -> str:
        return self.model

    def get_year(self) -> int:
        return self.year

from __future__ import annotations

class Client:
    def __init__(self, name: str, budget: int) -> None:
        self._name = name
        self._budget = budget
        self._bookings: list [Car | Motorcycle] = []

    def __repr__(self) -> str:
        return f"Client('{self._name}', {self._budget})"

    def book_vehicle(self, vehicle: Car | Motorcycle, date: str, vehicle_rental) -> bool:
        uspeh = vehicle_rental.rent_vehicle(self, vehicle, date)
        if uspeh:
            self._bookings.append(vehicle)
            return True
        return False

    def total_spent(self) -> int:
        return self.start_budget - self.budget

    def get_name(self) -> str:
        return self.name

    def get_budget(self) -> int:
        return self.budget

    def get_bookings(self) -> list[Car | Motorcycle]:
        return self.bookings

class VehicleRental:
    def __init__(self) -> None:
        self.earnings = 0
        self.motorcycles = []
        self.cars = []
        self.taken = False
        self.clients = []
        self.vehicle_availability = {}

    def get_money(self) -> int:
        pass

    def get_motorcycles(self) -> list[Motorcycle]:
        pass

    def get_cars(self) -> list[Car]:
        pass

    def get_vehicle_bookings_dict(self) -> dict[Car | Motorcycle, list[str]]:
        pass

    def get_clients(self) -> list[Client]:
        pass

    def add_vehicle(self, vehicle: Car | Motorcycle) -> bool:
        if isinstance(vehicle, Car) and not self.cars:
            self.cars.append(vehicle)
            return True
        elif isinstance(vehicle, Motorcycle) and not self.motorcycles:
            self.motorcycles.append(vehicle)
            return True
        return False

    def is_vehicle_available(self, vehicle: Car | Motorcycle, date: str) -> bool:
        if not date_checker(date):
            return False

        if vehicle in self.vehicle_availability and date in self.vehicle_availability[vehicle]:
            return False

        return True

    def rent_vehicle(self, vehicle: Car | Motorcycle, date: str, client: Client) -> bool:
        pass

    def get_most_rented_vehicle(self) -> list[Motorcycle | Car]:
        most_rented_vehicles = []

        if not self.vehicle_availability:
            return []

        max_rentals = 0

        for vehicle, dates in self.vehicle_availability.items():
            rental_count = len(dates)
            if rental_count > max_rentals:
                max_rentals = rental_count
                most_rented_vehicles = [vehicle]
            elif rental_count == max_rentals:
                most_rented_vehicles.append(vehicle)

        return most_rented_vehicles

    def find_vehicle_by_make(self, make: str) -> list[Car | Motorcycle]:
        return [v for v in self.cars + self.motorcycles if v.get_make() == make]

    def find_car_by_type(self, type_of_car: Type) -> list[Car]:
        return [car for car in self.cars if car.type_of_car == type_of_car]

    def get_best_client(self) -> Client | None:
        pass

    def get_sorted_vehicles_list(self) -> list[Car | Motorcycle]:
        return sorted(self.cars + self.motorcycles, key=lambda vehicle: len(self.vehicle_availability.get(vehicle, [])))

    def get_vehicles_by_year_range(self, start_year: int, end_year: int) -> list[Car | Motorcycle] | ValueError:
        if isinstance(start_year, float) or isinstance(end_year, float):
            raise ValueError(f"Start year and end year must be integers.")
        if end_year < start_year:
            raise ValueError(f"End year must be greater than start year.")
        return [vehicle for vehicle in self.cars + self.motorcycles if start_year <= vehicle.get_year() <= end_year]


if __name__ == '__main__':
    rental = VehicleRental()
    car1 = Car('Hyundai', 'Solaris', 2022, Type.OTHER)
    motorcycle1 = Motorcycle('Kawasaki', 'Ninja', 2019)
    client1 = Client('Kaspar', 200)

    print('def get_price(vehicle) -> int:')
    print('-' * 30)
    print(str(get_price(Motorcycle('Kawasaki', 'Ninja', 2019))) + '  # ' + '100')  # 100
    print(str(get_price(Car('Hyundai', 'Solaris', 2022, Type.OTHER))) + '  # ' + '50')  # 50
    print('')

    print('def date_checker(date: str) -> bool:')
    print('-' * 36)
    print(str(date_checker('02.12.2025')) + '  # ' + 'True')  # True
    print(str(date_checker('32.13.1899')) + '  # ' + 'False')  # False
    print(str(date_checker('02/12/2025')) + '  # ' + 'False')  # False
    print(str(date_checker('2.12.2025')) + '  # ' + 'False')  # False
    print(str(date_checker(' 02.12.2025 ')) + '  # ' + 'False')  # False
    print(str(date_checker(' ')) + '  # ' + 'False')  # False
    print(str(date_checker('')) + '  # ' + 'False')  # False
    print('')

    print('Car')
    print('===')
    print('')

    print('def __repr__(self) -> str:')
    print('-' * 26)
    print(car1.__repr__() + '  # ' + 'Car(Hyundai, Solaris, 2022, Type.OTHER)')
    # 'Car(Hyundai, Solaris, 2022, Type.OTHER)'
    print('')

    print('def get_make(self) -> str:')
    print('-' * 26)
    print(str(car1.get_make()) + '  # ' + 'Hyundai')  # Hyundai
    print('')

    print('def get_model(self) -> str:')
    print('-' * 27)
    print(str(car1.get_model()) + '  # ' + 'Solaris')  # Solaris
    print('')

    print('def get_type(self) -> Type:')
    print('-' * 27)
    print(str(car1.get_type()) + '  # ' + 'Type.OTHER')  # Type.OTHER
    print('')

    print('def get_year(self) -> int:')
    print('-' * 26)
    print(str(car1.get_year()) + '  # ' + '2022')  # 2022
    print('')

    print('def get_price(self) -> int:')
    print('-' * 27)
    print(str(car1.get_price()) + '  # ' + '50')  # 50
    print('')

    print('Motorcycle')
    print('==========')
    print('')

    print('def __repr__(self) -> str:')
    print('-' * 26)
    print(motorcycle1.__repr__() + '  # ' + 'Motorcycle(Kawasaki, Ninja, 2019)')
    # 'Motorcycle(Kawasaki, Ninja, 2019)'
    print('')

    print('def get_make(self) -> str:')
    print('-' * 26)
    print(str(motorcycle1.get_make()) + '  # ' + 'Kawasaki')  # Kawasaki
    print('')

    print('def get_model(self) -> str:')
    print('-' * 27)
    print(str(motorcycle1.get_model()) + '  # ' + 'Ninja')  # Ninja
    print('')

    print('def get_year(self) -> int:')
    print('-' * 26)
    print(str(motorcycle1.get_year()) + '  # ' + '2019')  # 2019
    print('')

    print('def get_price(self) -> int:')
    print('-' * 27)
    print(str(motorcycle1.get_price()) + '  # ' + '100')  # 100
    print('')

    print('VehicleRental')
    print('=============')
    print('')

    print('def add_vehicle(self, vehicle: Car | Motorcycle) -> bool:')
    print('-' * 57)
    print(str(rental.add_vehicle(car1)) + '  # ' + 'True')  # True
    print(str(rental.add_vehicle(motorcycle1)) + '  # ' + 'True')  # True
    print(str(rental.add_vehicle(motorcycle1)) + '  # ' + 'False')  # False
    print('')

    print('Client')
    print('======')
    print('')

    print('def __repr__(self) -> str:')
    print('-' * 27)
    print(client1.__repr__() + '  # ' + 'Client(Kaspar, 200)')
    # 'Client(Kaspar, 200)'
    print('')

    print('def book_vehicle(self, vehicle: Car|Motorcycle, date: str, vehicle_rental) -> bool:')
    print('-' * 83)
    print(str(client1.book_vehicle(car1, '31.12.2025', rental)) + '  # ' + 'True')  # True
    print(str(client1.book_vehicle(motorcycle1, '01.01.2026', rental)) + '  # ' + 'True')  # True
    print('')

    print('def total_spent(self) -> int:')
    print('-' * 29)
    print(str(client1.total_spent()) + '  # ' + '150')  # 150
    print('')

    print('def get_name(self) -> str:')
    print('-' * 26)
    print(str(client1.get_name()) + '  # ' + 'Kaspar')  # Kaspar
    print('')

    print('def get_budget(self) -> int:')
    print('-' * 28)
    print(str(client1.get_budget()) + '  # ' + '50')  # 50
    print('')

    print('def get_bookings(self) -> list[Car | Motorcycle]:')
    print('-' * 49)
    print(str(client1.get_bookings()) + '  # ' + '\n'
          + '[Car(Hyundai, Solaris, 2022, Type.OTHER), Motorcycle(Kawasaki, Ninja, 2019)]')
    # [Car(Hyundai, Solaris, 2022, Type.OTHER), Motorcycle(Kawasaki, Ninja, 2019)]
    print('')

    print('VehicleRental')
    print('=============')
    print('')

    print('def get_money(self) -> int:')
    print('-' * 27)
    print(str(rental.get_money()) + '  # ' + '150')  # 150
    print('')

    print('def get_motorcycles(self) -> list[Motorcycle]:')
    print('-' * 46)
    print(str(rental.get_motorcycles()) + '  # ' + '[Motorcycle(Kawasaki, Ninja, 2019)]')
    # [Motorcycle(Kawasaki, Ninja, 2019)]
    print('')

    print('def get_cars(self) -> list[Car]:')
    print('-' * 32)
    print(str(rental.get_cars()) + '  # ' + '[Car(Hyundai, Solaris, 2022, Type.OTHER)]')
    # [Car(Hyundai, Solaris, 2022, Type.OTHER)]
    print('')

    print('def get_vehicle_bookings_dict(self) -> dict[Car | Motorcycle, list[str]]:')
    print('-' * 73)
    print(str(rental.get_vehicle_bookings_dict()) + '  # ')
    print("{Car(Hyundai, Solaris, 2022, Type.OTHER): ['31.12.2025'], "
          + "Motorcycle(Kawasaki, Ninja, 2019): ['01.01.2026']}")
    # {Car(Hyundai, Solaris, 2022, Type.OTHER): ['31.12.2025'], Motorcycle(Kawasaki, Ninja, 2019): ['01.01.2026']}
    print('')

    print('get_clients(self) -> list[Client]:')
    print('-' * 34)
    print(str(rental.get_clients()) + '  # ' + '[Client(Kaspar, 50)]')  # [Client(Kaspar, 50)]
    print('')

    print('def is_vehicle_available(self, vehicle: Car | Motorcycle, date: str) -> bool:')
    print('-' * 77)
    print(str(rental.is_vehicle_available(car1, '31.12.2025')) + '  # ' + 'False')  # False
    print(str(rental.is_vehicle_available(car1, '02.01.2026')) + '  # ' + 'True')  # True
    print('')

    print('def rent_vehicle(self, vehicle: Car | Motorcycle, date: str, client: Client) -> bool:')
    print('-' * 85)
    print(str(rental.rent_vehicle(car1, '02.01.2026', client1)) + '  # ' + 'True')  # True
    print(str(rental.rent_vehicle(car1, '31.12.2025', client1)) + '  # ' + 'False')  # False
    print('')

    print('def get_most_rented_vehicle(self) -> list[Motorcycle | Car]:')
    print('-' * 60)
    print(str(rental.get_most_rented_vehicle()) + '  # ' + '[Car(Hyundai, Solaris, 2022, Type.OTHER)]')
    # [Car(Hyundai, Solaris, 2022, Type.OTHER)]
    print('')

    print('def find_vehicle_by_make(self, make: str) -> list[Car|Motorcycle]:')
    print('-' * 66)
    print(str(rental.find_vehicle_by_make('Hyundai')) + '  # ' + '[Car(Hyundai, Solaris, 2022, Type.OTHER)]')
    # [Car(Hyundai, Solaris, 2022, Type.OTHER)]
    print('')

    print('def find_car_by_type(self, type_of_car: Type) -> list[Car]:')
    print('-' * 59)
    print(str(rental.find_car_by_type(Type.OTHER)) + '  # ' + '[Car(Hyundai, Solaris, 2022, Type.OTHER)]')
    # [Car(Hyundai, Solaris, 2022, Type.OTHER)]
    print('')

    print('def get_best_client(self) -> Client | None:')
    print('-' * 43)
    print(str(rental.get_best_client()) + '  # ' + 'Client(Kaspar, 50)')  # Client(Kaspar, 50)
    print('')

    print('def get_sorted_vehicles_list(self) -> list[Car | Motorcycle]:')
    print('-' * 61)
    print(str(rental.get_sorted_vehicles_list()) + '  # ' + '\n'
          + '[Car(Hyundai, Solaris, 2022, Type.OTHER), Motorcycle(Kawasaki, Ninja, 2019)]')
    # [Car(Hyundai, Solaris, 2022, Type.OTHER), Motorcycle(Kawasaki, Ninja, 2019)]
    print('')

    print('def get_vehicles_by_year_range(self, start_year: int, end_year: int) -> '
          + 'list[Car | Motorcycle] | ValueError:')
    print('-' * 108)
    print(str(rental.get_vehicles_by_year_range(2018, 2020)) + '  # '
          + '[Motorcycle(Kawasaki, Ninja, 2019)]')
    # [Motorcycle(Kawasaki, Ninja, 2019)]
    print('')
