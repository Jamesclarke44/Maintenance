import streamlit as st
import json
from datetime import datetime

FILE = "4runner_maintenance.json"

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

# ------------------ WORKSHOP DATABASE ------------------

WORKSHOP = {

    "Engine Oil": {
        "fluid": "0W-20 Synthetic Oil",
        "capacity": "5.7 L",
        "interval_km": 8000,
        "torque": {"drain_plug": "30 ft-lb"},
        "washers": {"drain_plug": "crush washer"},
        "sockets": {"Drain Plug": "14 mm"},
        "workflow": [
            "Warm engine",
            "Drain oil",
            "Replace washer",
            "Torque drain plug",
            "Refill oil"
        ]
    },

    "Transmission (Drain & Fill)": {
        "fluid": "Toyota ATF WS",
        "capacity": "3.0–4.3 L",
        "interval_km": 96000,
        "torque": {"fill_plug": "15 ft-lb", "drain_plug": "29 ft-lb"},
        "sockets": {"Fill Plug": "24 mm", "Drain Plug": "14 mm"},
        "washers": {"fill_plug": "crush washer", "drain_plug": "crush washer"},
        "workflow": [
            "Warm transmission",
            "Remove fill plug FIRST",
            "Drain fluid",
            "Reinstall drain plug",
            "Fill with ATF WS",
            "Check temp 40–45°C",
            "Install fill plug"
        ]
    },

    "Front Differential": {
        "fluid": "75W-85 GL-5",
        "capacity": "1.3 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "sockets": {"Fill": "24 mm", "Drain": "24 mm"},
        "workflow": ["Remove fill plug", "Drain", "Fill until overflow"]
    },

    "Rear Differential": {
        "fluid": "75W-85 GL-5",
        "capacity": "2.7 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "sockets": {"Fill": "24 mm", "Drain": "24 mm"},
        "workflow": ["Remove fill plug", "Drain", "Fill until overflow"]
    },

    "Transfer Case": {
        "fluid": "75W-90 GL-4/GL-5",
        "capacity": "1.0 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "sockets": {"Fill": "24 mm", "Drain": "24 mm"},
        "workflow": ["Remove fill plug", "Drain", "Fill"]
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
        "workflow": ["Drain cold", "Refill", "Bleed air system"]
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
        "workflow": ["Remove sensor", "Clean MAF spray", "Dry", "Reinstall"]
    },

    "Throttle Body Cleaning": {
        "interval_km": 40000,
        "workflow": ["Remove intake hose", "Clean plate", "Reinstall"]
    }
}

# ------------------ INTELLIGENCE ------------------

def get_overdue_score(service, km):
    spec = WORKSHOP.get(service)
    if not spec:
        return 0

    interval = spec.get("interval_km")
    if not interval:
        return 0

    last = data["last_service"].get(service)

    if last is None:
        return 100

    overdue = km - (last + interval)

    if overdue <= 0:
        return 0

    return min(100, int((overdue / interval) * 100))


def get_risk(score):
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
    "Transmission (Drain & Fill)": ["Slow Acceleration"]
}

DIAGNOSTICS = {
    "Rough Idle": ["Throttle Body Cleaning", "MAF Sensor Cleaning", "Engine Air Filter"],
    "Poor Fuel Economy": ["MAF Sensor Cleaning", "Engine Air Filter"],
    "Clunk / Vibration": ["Propeller Shaft Grease", "Front Differential", "Rear Differential"],
    "Slow Acceleration": ["Transmission (Drain & Fill)", "MAF Sensor Cleaning"],
    "Overheating": ["Coolant"]
}

# ------------------ UI ------------------

st.set_page_config(page_title="4Runner Workshop OS", layout="centered")
st.title("🔧 4Runner Workshop OS")

menu = st.radio("", ["📊 Dashboard", "🛠 Service Mode", "📘 Workshop", "🧠 Diagnostics", "📒 History"])

# ------------------ DASHBOARD ------------------

if menu == "📊 Dashboard":
    km = st.number_input("Current KM", 0)

    if km:
        for item, spec in WORKSHOP.items():
            interval = spec.get("interval_km")
            last = data["last_service"].get(item)

            if interval:
                if last is None:
                    st.warning(f"⚠️ {item}: NEVER SERVICED")
                else:
                    due = last + interval
                    if km >= due:
                        st.error(f"⚠️ {item} DUE")
                    else:
                        st.success(f"{item}: {due - km} km remaining")

# ------------------ SERVICE MODE (FIXED) ------------------

elif menu == "🛠 Service Mode":

    service = st.selectbox("Select Service", list(WORKSHOP.keys()))
    km = st.number_input("Current KM", 0)
    notes = st.text_area("Notes")

    spec = WORKSHOP[service]

    st.markdown(f"# 🔧 {service}")

    col1, col2 = st.columns(2)

    with col1:
        st.write("🛢 Fluid")
        st.write(spec.get("fluid", "—"))

    with col2:
        st.write("📦 Capacity")
        st.write(spec.get("capacity", "—"))

    st.write(f"📅 Interval: {spec.get('interval_km', '—')} km")

    st.markdown("---")

    # QUICK SPECS
    if "sockets" in spec:
        st.markdown("### 🔩 Sockets")
        for k, v in spec["sockets"].items():
            st.write(f"- {k}: {v}")

    if "torque" in spec:
        st.markdown("### 🔧 Torque")
        for k, v in spec["torque"].items():
            st.write(f"- {k}: {v}")

    if "washers" in spec:
        st.markdown("### 🧰 Washers")
        for k, v in spec["washers"].items():
            st.write(f"- {k}: {v}")

    st.markdown("---")

    # WORKFLOW CHECKLIST
    st.markdown("## 📋 Workflow")

    completed = []

    for i, step in enumerate(spec.get("workflow", []), 1):
        done = st.checkbox(f"{i}. {step}", key=f"{service}_{i}")
        if done:
            completed.append(step)

    st.markdown("---")

    if st.button("✔ Save Service"):

        data["logs"].append({
            "service": service,
            "km": km,
            "date": str(datetime.now()),
            "notes": notes,
            "steps_completed": completed
        })

        data["last_service"][service] = km
        save_data(data)

        st.success("Saved ✔")

# ------------------ WORKSHOP ------------------

elif menu == "📘 Workshop":
    st.subheader("🔧 Workshop Reference")

    for name, spec in WORKSHOP.items():
        st.markdown(f"## {name}")

        if "fluid" in spec:
            st.write(f"Fluid: {spec['fluid']}")

        if "capacity" in spec:
            st.write(f"Capacity: {spec['capacity']}")

        if "interval_km" in spec:
            st.write(f"Interval: {spec['interval_km']} km")

        if "workflow" in spec:
            st.markdown("Workflow:")
            for i, step in enumerate(spec["workflow"], 1):
                st.write(f"{i}. {step}")

        st.markdown("---")

# ------------------ DIAGNOSTICS ------------------

elif menu == "🧠 Diagnostics":

    symptom = st.selectbox("Select Symptom", list(DIAGNOSTICS.keys()))
    km = st.number_input("Current KM", 0)

    for item in DIAGNOSTICS[symptom]:

        score = get_overdue_score(item, km)
        risk = get_risk(score)

        st.write(f"**{item}**")
        st.write(f"Risk: {risk}")
        st.write(f"Score: {score}/100")

        if item in DEPENDENCIES:
            st.write("Related:")
            for d in DEPENDENCIES[item]:
                st.write(f"• {d}")

        st.markdown("---")

# ------------------ HISTORY ------------------

elif menu == "📒 History":
    if not data["logs"]:
        st.info("No records yet")
    else:
        for log in reversed(data["logs"]):
            st.write(log)