import datetime

class Vehicle:
    def __init__(self, reg_number, vehicle_type):
        self.reg_number = reg_number
        self.vehicle_type = vehicle_type  # 'two_wheeler' or 'four_wheeler'

class TollPass:
    def __init__(self, vehicle_reg_number, toll_id, pass_type, purchase_date, times_used=0):
        self.vehicle_reg_number = vehicle_reg_number
        self.toll_id = toll_id
        self.pass_type = pass_type  # 'single', 'return', '7_day'
        self.times_used = times_used
        self.purchase_date = purchase_date
        self.valid_until = self.calculate_validity()
        # keep history of the direction. mostly just for return. so only one variable called passed_direction.

    def calculate_validity(self):
        if self.pass_type == 'single':
            return self.purchase_date
        elif self.pass_type == 'return':
            return (self.purchase_date + datetime.timedelta(days=1)) 
        elif self.pass_type == '7_day':
            return self.purchase_date + datetime.timedelta(days=7)

    def is_valid(self, date):
        if self.pass_type == 'single':
            return date <= self.valid_until and self.times_used == 0
        elif self.pass_type == 'return':
            return date <= self.valid_until and self.times_used < 2
        elif self.pass_type == '7_day':
            return date <= self.valid_until
        
    def increment_times_used(self):
        self.times_used += 1


class TollBooth:
    def __init__(self, toll_id, booth_id):
        self.toll_id = toll_id
        self.booth_id = booth_id
        self.vehicle_count = 0
        self.total_collection = 0
        # have my_direction

    def process_vehicle(self, vehicle, toll_pass):
        self.vehicle_count += 1
        charge = self.calculate_charge(vehicle, toll_pass.pass_type)
        self.total_collection += charge
        toll_pass.increment_times_used()

    

    @staticmethod
    def calculate_charge(vehicle, pass_type):
        charges = {'two_wheeler': {'single': 50, 'return': 75, '7_day': 200},
                   'four_wheeler': {'single': 100, 'return': 150, '7_day': 400}}
        return charges[vehicle.vehicle_type][pass_type]

class Toll:
    def __init__(self, toll_id):
        self.toll_id = toll_id


# Sample usage
def main():

    # Initialize some data
    vehicles = [Vehicle('AB1234', 'two_wheeler'), Vehicle('CD5678', 'four_wheeler')]
    tolls = [Toll(1), Toll(2)]
    toll_booths = [TollBooth(1, 101), TollBooth(1, 102), TollBooth(2, 201), TollBooth(2, 202)]
    toll_passes = [TollPass('AB1234', 1, '7_day', datetime.date.today())]

    # CLI interactions (simplified)
    while True:
        print("\n1. Process Vehicle\n2. Show Leaderboard\n3. Print")
        choice = input("Enter your choice: ")

        if choice == '1':
            reg_number = input("Enter vehicle registration number: ")
            vehicle = next((v for v in vehicles if v.reg_number == reg_number), None)
            if not vehicle:
                print("Vehicle not found.")
                continue

            toll_booth_number = input("Enter toll booth number: ")
            toll_booth = None
            for t in toll_booths:
                if t.booth_id == int(toll_booth_number):
                    toll_booth = t
                    break

            # Check if vehicle has a valid pass
            valid_pass = next((p for p in toll_passes if p.vehicle_reg_number == reg_number and p.toll_id == toll_booth.toll_id and p.is_valid(datetime.date.today())), None)
            if valid_pass:
                print(f"Valid pass found: {valid_pass.pass_type}")
                toll_booth.process_vehicle(vehicle, valid_pass)

            else:
                print("No valid pass. Purchase a new pass.")
                # Logic for purchasing a new pass
                pass_choice = input("Enter choice type: 1 for single, 2 for return, 3 for 7-day: ")
                pass_type = ''
                if int(pass_choice) == 1:
                    pass_type = 'single'
                elif int(pass_choice) == 2:
                    pass_type = 'return'
                elif int(pass_choice) == 3:
                    pass_type = '7_day'

                if not pass_type:
                    print("invalid choice")

                new_pass = TollPass(vehicle.reg_number, toll_booth.toll_id, pass_type, datetime.date.today())
                toll_passes.append(new_pass)
                print("New pass purchased")
        elif choice == '2':
            # Show leaderboard logic
            for booth in toll_booths:
                print(f"Toll Booth {booth.booth_id}: Vehicles Processed: {booth.vehicle_count}, Total Collection: {booth.total_collection}")

        elif choice == '3':
            for v in vehicles:
                print(vars(v))
            for p in toll_passes:
                print(vars(p))
            for t in toll_booths:
                print(vars(t))

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()