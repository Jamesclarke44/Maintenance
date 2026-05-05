import json
from datetime import datetime

FILE = "4runner_maintenance.json"

# Default maintenance schedule (km intervals)
SCHEDULE = {
    "Engine Oil": 8000,
    "Transmission (Drain & Fill)": 60000,
    "Front Differential": 80000,
    "Rear Differential": 80000,
    "Transfer Case": 80000,
    "Brake Fluid": 40000,
    "Coolant": 160000
}

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {"logs": [], "last_service": {}}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_service():
    data = load_data()

    service = input("Service type: ")
    km = int(input("Current KM: "))
    notes = input("Notes (fluid, parts, etc): ")

    entry = {
        "service": service,
        "km": km,
        "date": str(datetime.now()),
        "notes": notes
    }

    data["logs"].append(entry)
    data["last_service"][service] = km

    save_data(data)
    print("✅ Service logged.")

def check_due():
    data = load_data()
    current_km = int(input("Enter current KM: "))

    print("\n🔧 Maintenance Status:\n")

    for service, interval in SCHEDULE.items():
        last_km = data["last_service"].get(service, 0)
        due_km = last_km + interval

        if current_km >= due_km:
            print(f"⚠️ {service} is DUE (Last: {last_km} km)")
        else:
            remaining = due_km - current_km
            print(f"✅ {service} OK ({remaining} km remaining)")

def show_logs():
    data = load_data()
    print("\n📒 Service History:\n")

    for log in data["logs"]:
        print(f"{log['date']} | {log['service']} @ {log['km']} km")
        print(f"   Notes: {log['notes']}\n")

def main():
    while True:
        print("\n--- 4Runner Maintenance Tracker ---")
        print("1. Log Service")
        print("2. Check Maintenance Due")
        print("3. Show History")
        print("4. Exit")

        choice = input("Select: ")

        if choice == "1":
            log_service()
        elif choice == "2":
            check_due()
        elif choice == "3":
            show_logs()
        elif choice == "4":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()