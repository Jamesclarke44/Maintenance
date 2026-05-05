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
        "sockets": {
            "drain plug": "14 mm",
            "filter": "Toyota cartridge wrench"
        },
        "workflow": [
            "Warm engine slightly",
            "Remove skid plate if equipped",
            "Remove drain plug (14 mm)",
            "Drain oil completely",
            "Replace crush washer",
            "Reinstall drain plug",
            "Replace oil filter",
            "Refill with 5.7 L oil",
            "Start engine and check leaks"
        ]
    },

    "Transmission (Drain & Fill)": {
        "fluid": "Toyota ATF WS",
        "capacity": "3.0–4.3 L",
        "interval_km": 96000,
        "temp": "40–45°C",
        "torque": {
            "fill_plug": "15 ft-lbs",
            "drain_plug": "29 ft-lbs"
        },
        "sockets": {
            "fill plug": "24 mm",
            "drain plug": "14 mm",
            "level check": "5 mm Allen"
        },
        "workflow": [
            "Warm transmission to operating temp",
            "Level vehicle on flat ground",
            "Remove fill plug FIRST (24 mm)",
            "Drain fluid (14 mm)",
            "Reinstall drain plug",
            "Torque to 29 ft-lbs",
            "Fill with ATF WS",
            "Check fluid at 40–45°C",
            "Install level/fill plug",
            "Torque to 15 ft-lbs",
            "Check for leaks"
        ]
    },

    "Front Differential": {
        "fluid": "75W-85 GL-5",
        "capacity": "1.3 L",
        "interval_km": 48000,
        "torque": "48 ft-lbs",
        "sockets": {
            "fill plug": "24 mm",
            "drain plug": "24 mm"
        },
        "workflow": [
            "Remove fill plug FIRST",
            "Drain fluid",
            "Reinstall drain plug",
            "Torque to 48 ft-lbs",
            "Fill until overflow",
            "Reinstall fill plug",
            "Torque to 29 ft-lbs"
        ]
    },

    "Rear Differential": {
        "fluid": "75W-85 GL-5",
        "capacity": "2.7 L",
        "interval_km": 48000,
        "torque": "48 ft-lbs",
        "sockets": {
            "fill plug": "24 mm",
            "drain plug": "24 mm"
        },
        "workflow": [
            "Remove fill plug FIRST",
            "Drain fluid completely",
            "Replace crush washer",
            "Reinstall drain plug",
            "Torque to 48 ft-lbs",
            "Fill until fluid seeps out",
            "Reinstall fill plug",
            "Torque to 29 ft-lbs"
        ]
    },

    "Transfer Case": {
        "fluid": "75W-90 GL-4/GL-5",
        "capacity": "1.0 L",
        "interval_km": 48000,
        "torque": "48 ft-lbs",
        "sockets": {
            "fill plug": "24 mm",
            "drain plug": "24 mm"
        },
        "workflow": [
            "Remove fill plug FIRST",
            "Drain fluid",
            "Reinstall drain plug",
            "Torque to 48 ft-lbs",
            "Fill 1.0 L gear oil",
            "Reinstall fill plug",
            "Torque to 29 ft-lbs"
        ]
    },

    # 🆕 NEW: Propeller Shaft Greasing
    "Propeller Shaft (Greasing)": {
        "fluid": "Lithium-based NLGI #2 grease",
        "capacity": "Grease until fresh appears at seals",
        "interval_km": 10000,
        "sockets": {
            "driveshaft bolts": "14 mm",
            "grease fittings": "Grease gun"
        },
        "workflow": [
            "Lift and safely support vehicle",
            "Locate all grease fittings",
            "Clean grease nipples",
            "Apply grease slowly to U-joints",
            "Grease slip yoke (if equipped)",
            "Stop when fresh grease appears",
            "Rotate driveshaft for access",
            "Wipe excess grease",
            "Inspect boots and joints",
            "Test drive for vibration"
        ]
    },

    "Brake Fluid": {
        "fluid": "DOT 3",
        "capacity": "0.8–1.0 L flush",
        "interval_km": 48000,
        "interval_years": 2,
        "bleed_sequence": [
            "Right Rear (RR)"
            "Left Reat (LR)"
            "Right Front (RF)"
            "Left Frony (LF)"
        ],
        "workflow": [
            "Start with Right Rear caliper",
            "Keep master cylinder reservoir full at all times",
            "Move to Left Rear",
            "Then Right Front",
            "Finish with Left Front",
            "Continue until clear fluid at each corner",
            "Check pedal firmness",
            "Top off reservoir to MAX line"
        ]
    },

    "Coolant": {
        "fluid": "Toyota SLLC (Pink)",
        "capacity": "11–12 L",
        "interval_km": 160000,
        "interval_after": 80000,
        "workflow": [
            "Drain coolant when cold",
            "Refill with Toyota SLLC",
            "Bleed air system",
            "Check level after warm-up"
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
st.set_page_config(page_title="4Runner Workshop OS", layout="centered")

st.title("🔧 4Runner Workshop OS")

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

    st.markdown("## 🔧 Specs")
    st.write(f"Fluid: {spec.get('fluid','-')}")
    st.write(f"Capacity: {spec.get('capacity','-')}")
    st.write(f"Interval: {spec.get('interval_km','Time-based')} km")

    if "torque" in spec:
        st.write(f"Torque: {spec['torque']}")
    if "temp" in spec:
        st.write(f"Temp: {spec.get('temp','-')}")

    if "sockets" in spec:
        st.markdown("### 🔩 Socket Sizes")
        for part, size in spec["sockets"].items():
            st.write(f"{part}: {size}")

    if "workflow" in spec:
        st.markdown("### 📋 Workflow")
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

        st.success("Saved ✔️")

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