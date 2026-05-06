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
        "torque": {"drain_plug": "30 ft-lb"},
        "washers": {"drain_plug": "crush washer"},
        "sockets": {"Drain Plug": "14 mm"},
        "workflow": ["Warm engine", "Drain oil", "Replace washer", "Torque drain plug", "Refill oil"]
    },

    "Transmission (Drain & Fill)": {
        "fluid": "Toyota ATF WS",
        "capacity": "3.0–4.3 L",
        "interval_km": 96000,
        "torque": {"fill_plug": "15 ft-lb", "drain_plug": "29 ft-lb"},
        "sockets": {"Fill Plug": "24 mm", "Drain Plug": "14 mm"},
        "washers": {"fill_plug": "crush washer", "drain_plug": "crush washer"},
        "workflow": ["Warm transmission", "Drain", "Fill", "Check temp 40–45°C"]
    },

    "Front Differential": {
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "sockets": {"Fill": "24 mm", "Drain": "24 mm"}
    },

    "Rear Differential": {
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "sockets": {"Fill": "24 mm", "Drain": "24 mm"}
    },

    "Transfer Case": {
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "sockets": {"Fill": "24 mm", "Drain": "24 mm"}
    },

    "Propeller Shaft Grease": {
        "interval_km": 10000,
        "sockets": {"bolts": "14 mm"},
        "workflow": ["Grease U-joints", "Grease slip yoke"]
    },

    "Power Steering Fluid": {
        "interval_km": 80000,
        "workflow": ["Drain reservoir", "Refill ATF", "Cycle steering"]
    },

    "Brake Fluid": {
        "interval_km": 48000,
        "workflow": ["RR → LR → RF → LF bleed sequence"]
    },

    "Coolant": {
        "interval_km": 160000,
        "workflow": ["Drain", "Refill", "Bleed air system"]
    },

    "Cabin Air Filter": {
        "interval_km": 24000,
        "workflow": ["Drop glove box", "Replace filter"]
    },

    "Engine Air Filter": {
        "interval_km": 24000,
        "workflow": ["Open air box", "Replace filter"]
    },

    "MAF Sensor Cleaning": {
        "interval_km": 30000,
        "workflow": ["Remove sensor", "Clean with MAF spray", "Dry", "Reinstall"]
    },

    "Throttle Body Cleaning": {
        "interval_km": 40000,
        "workflow": ["Remove intake hose", "Clean plate", "Reinstall"]
    }
}

# ------------------ SMART INTELLIGENCE LAYER ------------------

def get_overdue_score(service, km):
    spec = WORKSHOP.get(service, {})
    interval = spec.get("interval_km", None)

    if not interval:
        return 0

    last = data["last_service"].get(service, km)
    overdue_km = km - (last + interval)

    if overdue_km <= 0:
        return 0

    return min(100, int((overdue_km / interval) * 100))


def get_risk_level(score):
    if score == 0:
        return "OK"
    elif score < 30:
        return "LOW"
    elif score < 70:
        return "MEDIUM"
    return "HIGH"


DEPENDENCIES = {
    "MAF Sensor Cleaning": ["Throttle Body Cleaning", "Engine Air Filter"],
    "Engine Air Filter": ["MAF Sensor Cleaning"],
    "Throttle Body Cleaning": ["MAF Sensor Cleaning"],
    "Propeller Shaft Grease": ["Clunk / Vibration"],
    "Transmission (Drain & Fill)": ["Slow Acceleration"]
}

# ------------------ DIAGNOSTICS ------------------

DIAGNOSTICS = {
    "Rough Idle": ["Throttle Body Cleaning", "MAF Sensor Cleaning", "Engine Air Filter"],
    "Poor Fuel Economy": ["MAF Sensor Cleaning", "Engine Air Filter"],
    "Clunk / Vibration": ["Propeller Shaft Grease", "Front Differential", "Rear Differential"],
    "Slow Acceleration": ["Transmission (Drain & Fill)", "MAF Sensor Cleaning"],
    "Overheating": ["Coolant"],
    "Hard Starting": ["Battery Inspection", "Spark Plugs"]
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

menu = st.radio("", ["📊 Dashboard", "🛠 Service Mode", "📘 Workshop", "🧠 Diagnostics", "📒 History"])

# ------------------ DASHBOARD ------------------

if menu == "📊 Dashboard":
    km = st.number_input("Current KM", 0)

    if km:
        for item, spec in WORKSHOP.items():
            interval = spec.get("interval_km", 0)
            last = data["last_service"].get(item, 0)

            if interval:
                due = last + interval
                if km >= due:
                    st.error(f"⚠️ {item} DUE")
                else:
                    st.success(f"{item}: {due - km} km remaining")

# ------------------ SERVICE MODE ------------------

elif menu == "🛠 Service Mode":
    service = st.selectbox("Select Service", list(WORKSHOP.keys()))
    km = st.number_input("KM", 0)
    notes = st.text_area("Notes")

    spec = WORKSHOP[service]

    st.write("### Specs")
    st.write(spec.get("fluid", spec.get("capacity", "")))

    if st.button("Save Service"):
        data["logs"].append({
            "service": service,
            "km": km,
            "date": str(datetime.now()),
            "notes": notes
        })

        data["last_service"][service] = km
        save_data(data)
        st.success("Saved ✔")

# ------------------ WORKSHOP ------------------

elif menu == "📘 Workshop":
    for name, spec in WORKSHOP.items():
        st.markdown(f"### {name}")
        st.write(spec)

# ------------------ DIAGNOSTICS (SMART) ------------------

elif menu == "🧠 Diagnostics":
    st.subheader("Smart Diagnostics")

    symptom = st.selectbox("Select Symptom", list(DIAGNOSTICS.keys()))
    km = st.number_input("Current KM", 0)

    st.markdown("### Analysis")

    for item in DIAGNOSTICS[symptom]:

        score = get_overdue_score(item, km)
        risk = get_risk_level(score)

        st.write(f"**{item}**")
        st.write(f"- Risk: {risk}")
        st.write(f"- Score: {score}/100")

        if item in DEPENDENCIES:
            st.write("Related:")
            for d in DEPENDENCIES[item]:
                st.write(f"  • {d}")

        st.markdown("---")

# ------------------ HISTORY ------------------

elif menu == "📒 History":
    if not data["logs"]:
        st.info("No records yet")
    else:
        for log in reversed(data["logs"]):
            st.write(log)