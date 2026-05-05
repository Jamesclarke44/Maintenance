import streamlit as st
import json
from datetime import datetime

FILE = "4runner_maintenance.json"

# ------------------ WORKSHOP DATABASE ------------------
WORKSHOP = {
    "Engine Oil": {
        "fluid": "0W-20 Synthetic Oil",
        "capacity": "5.7 L",
        "interval_km": 8000,
        "notes": "Oil + filter change",
        "sockets": {
            "drain_plug": "14 mm",
            "filter": "Toyota cartridge wrench"
        },
        "workflow": [
            "Warm engine slightly",
            "Lift vehicle safely",
            "Remove skid plate (if equipped)",
            "Remove drain plug (14 mm)",
            "Drain oil completely",
            "Replace crush washer",
            "Reinstall drain plug",
            "Replace oil filter",
            "Refill with 5.7 L oil",
            "Start engine and check for leaks"
        ]
    },

    "Transmission (Drain & Fill)": {
        "fluid": "Toyota ATF WS",
        "capacity": "3.0–4.3 L",
        "interval_km": 80000,
        "temp": "40–45°C",
        "torque": "20 Nm (check plug)",
        "sockets": {
            "fill_plug": "24 mm",
            "drain_plug": "14 mm",
            "level_check": "5 mm Allen"
        },
        "workflow": [
            "Warm transmission to operating temp",
            "Level vehicle on flat ground",
            "Remove fill plug FIRST (24 mm)",
            "Place drain pan",
            "Remove drain plug (14 mm)",
            "Let fluid fully drain",
            "Reinstall drain plug with new washer",
            "Fill with ATF WS until overflow",
            "Check fluid temp (40–45°C)",
            "Install level plug",
            "Verify no leaks"
        ]
    },

    "Front Differential": {
        "fluid": "75W-85 GL-5",
        "capacity": "1.3 L",
        "interval_km": 48000,
        "torque": "65 Nm",
        "sockets": {
            "fill_plug": "24 mm",
            "drain_plug": "24 mm"
        },
        "workflow": [
            "Ensure vehicle is level",
            "Remove fill plug FIRST (24 mm)",
            "Place drain pan under diff",
            "Remove drain plug",
            "Allow full drain",
            "Reinstall drain plug with crush washer",
            "Torque to 65 Nm",
            "Fill until fluid reaches bottom of fill hole",
            "Reinstall fill plug",
            "Torque to 65 Nm",
            "Check for leaks"
        ]
    },

    "Rear Differential": {
        "fluid": "75W-85 GL-5",
        "capacity": "2.7 L",
        "interval_km": 48000,
        "torque": "65 Nm",
        "sockets": {
            "fill_plug": "24 mm",
            "drain_plug": "24 mm"
        },
        "workflow": [
            "Park vehicle level",
            "Remove fill plug FIRST (24 mm)",
            "Place drain pan",
            "Remove drain plug",
            "Drain completely",
            "Install new crush washer",
            "Reinstall drain plug",
            "Torque to 65 Nm",
            "Fill until fluid seeps from fill hole",
            "Reinstall fill plug",
            "Torque to 65 Nm",
            "Clean area and inspect"
        ]
    },

    "Transfer Case": {
        "fluid": "75W-90 GL-4/GL-5",
        "capacity": "1.0 L",
        "interval_km": 48000,
        "torque": "65 Nm",
        "sockets": {
            "fill_plug": "24 mm",
            "drain_plug": "24 mm"
        },
        "workflow": [
            "Level vehicle",
            "Remove fill plug FIRST",
            "Remove drain plug",
            "Drain fully",
            "Reinstall drain plug with washer",
            "Torque to 65 Nm",
            "Fill with 1.0 L gear oil",
            "Reinstall fill plug",
            "Torque to 65 Nm"
        ]
    },

    "Brake Fluid": {
        "fluid": "DOT 3",
        "capacity": "0.8–1.0 L flush",
        "interval_km": 0,
        "interval_years": 2,
        "workflow": [
            "Start at passenger rear wheel",
            "Bleed brakes in sequence",
            "Keep reservoir full at all times",
            "Continue until clear fluid",
            "Check pedal feel",
            "Top off reservoir"
        ]
    },

    "Coolant": {
        "fluid": "Toyota SLLC (Pink)",
        "capacity": "11–12 L",
        "interval_km": 160000,
        "interval_after": 80000,
        "workflow": [
            "Ensure engine is cold",
            "Open radiator drain",
            "Drain coolant fully",
            "Close drain",
            "Refill with pre-mix SLLC",
            "Bleed air from system",
            "Run engine and check level",
            "Top off reservoir"
        ]
    }
}

# ------------------ DATA ------------------
def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {"logs": [], "last_service": {}}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ------------------ UI ------------------
st.set_page_config(page_title="4Runner Workshop Mode", layout="centered")

st.title("🔧 4Runner Workshop Mode")

menu = st.radio("", ["📊 Dashboard", "🛠 Service Mode", "📘 Workshop Specs", "📒 History"])

# ------------------ DASHBOARD ------------------
if menu == "📊 Dashboard":
    st.subheader("Maintenance Status")

    km = st.number_input("Current KM", min_value=0, step=100)

    if km:
        for item, spec in WORKSHOP.items():
            interval = spec.get("interval_km", 0)
            last = data["last_service"].get(item, 0)

            if interval > 0:
                due = last + interval

                if km >= due:
                    st.error(f"⚠️ {item} DUE")
                else:
                    st.success(f"{item}: {due - km} km remaining")

# ------------------ SERVICE MODE ------------------
elif menu == "🛠 Service Mode":
    st.subheader("Step-by-Step Service")

    service = st.selectbox("Select System", list(WORKSHOP.keys()))
    km = st.number_input("Current KM", min_value=0, step=100)
    notes = st.text_area("Notes")

    spec = WORKSHOP[service]

    st.markdown("## 🔧 Factory Specs")
    st.write(f"Fluid: {spec.get('fluid','-')}")
    st.write(f"Capacity: {spec.get('capacity','-')}")
    st.write(f"Interval: {spec.get('interval_km','Time-based')}")
    if "torque" in spec:
        st.write(f"Torque: {spec['torque']}")
    if "temp" in spec:
        st.write(f"Temp: {spec['temp']}")

    if "sockets" in spec:
        st.markdown("### 🔩 Socket Sizes")
        for part, size in spec["sockets"].items():
            st.write(f"{part}: {size}")

    if "workflow" in spec:
        st.markdown("### 📋 Step-by-Step Workflow")
        for i, step in enumerate(spec["workflow"], 1):
            st.write(f"{i}. {step}")

    if st.button("✔ Save Service"):
        entry = {
            "service": service,
            "km": km,
            "date": str(datetime.now()),
            "notes": notes
        }

        data["logs"].append(entry)
        data["last_service"][service] = km
        save_data(data)

        st.success("Service logged successfully")

# ------------------ WORKSHOP SPECS ------------------
elif menu == "📘 Workshop Specs":
    st.subheader("Reference Manual")

    for name, spec in WORKSHOP.items():
        st.markdown("---")
        st.write(f"### {name}")
        st.write(f"Fluid: {spec.get('fluid','-')}")
        st.write(f"Capacity: {spec.get('capacity','-')}")
        st.write(f"Interval: {spec.get('interval_km','Time-based')} km")

        if "torque" in spec:
            st.write(f"Torque: {spec['torque']}")

        if "sockets" in spec:
            st.write("🔩 Sockets:")
            for k, v in spec["sockets"].items():
                st.write(f"- {k}: {v}")

# ------------------ HISTORY ------------------
elif menu == "📒 History":
    st.subheader("Service History")

    if not data["logs"]:
        st.info("No service records yet.")
    else:
        for log in reversed(data["logs"]):
            st.write(f"**{log['date']}**")
            st.write(f"{log['service']} @ {log['km']} km")
            st.write(log["notes"])
            st.markdown("---")