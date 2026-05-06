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

# ------------------ HELPERS ------------------

def label(text):
    return text.replace("_", " ").title()


# ------------------ WORKSHOP DATABASE ------------------

WORKSHOP = {

    # ENGINE OIL
    "engine_oil": {
        "fluid": "0W-20 Full Synthetic",
        "capacity": "5.7 L",
        "interval_km": 8000,
        "torque": {"drain_plug": "30 ft-lb"},
        "washers": {
            "drain_plug": {"type": "crush", "material": "aluminum", "replace": True}
        },
        "sockets": {"drain_plug": "14 mm"},
        "workflow": [
            "Warm engine",
            "Remove drain plug",
            "Replace crush washer",
            "Torque drain plug to 30 ft-lb",
            "Refill 5.7 L 0W-20",
            "Check level"
        ]
    },

    # FRONT DIFFERENTIAL
    "front_differential": {
        "fluid": "75W-90 GL-5",
        "capacity": "1.3 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "washers": {
            "fill_plug": {"type": "crush", "material": "aluminum", "replace": True},
            "drain_plug": {"type": "crush", "material": "aluminum", "replace": True}
        },
        "sockets": {"fill_plug": "24 mm", "drain_plug": "24 mm"},
        "workflow": [
            "Remove fill plug first",
            "Remove drain plug",
            "Drain fluid completely",
            "Install drain plug (48 ft-lb)",
            "Fill until fluid drips from fill hole",
            "Install fill plug (48 ft-lb)"
        ]
    },

    # REAR DIFFERENTIAL
    "rear_differential": {
        "fluid": "75W-90 GL-5",
        "capacity": "2.7 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "36 ft-lb", "drain_plug": "36 ft-lb"},
        "washers": {
            "fill_plug": {"type": "crush", "material": "aluminum", "replace": True},
            "drain_plug": {"type": "crush", "material": "aluminum", "replace": True}
        },
        "sockets": {"fill_plug": "24 mm", "drain_plug": "24 mm"},
        "workflow": [
            "Remove fill plug first",
            "Remove drain plug",
            "Drain fluid",
            "Install drain plug (36 ft-lb)",
            "Fill until overflow",
            "Install fill plug (36 ft-lb)"
        ]
    },

    # TRANSFER CASE
    "transfer_case": {
        "fluid": "75W-90 GL-5 (Toyota LF 75W equivalent)",
        "capacity": "1.0 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "27 ft-lb", "drain_plug": "27 ft-lb"},
        "washers": {
            "fill_plug": {"type": "crush", "material": "aluminum", "replace": True},
            "drain_plug": {"type": "crush", "material": "aluminum", "replace": True}
        },
        "sockets": {"fill_plug": "24 mm", "drain_plug": "24 mm"},
        "workflow": [
            "Remove fill plug first",
            "Remove drain plug",
            "Drain fluid",
            "Install drain plug (27 ft-lb)",
            "Fill until overflow",
            "Install fill plug (27 ft-lb)"
        ]
    },

    # TRANSMISSION (A750F)
    "transmission": {
        "fluid": "Toyota ATF WS",
        "capacity": "3.0–4.3 L per drain",
        "interval_km": 96000,
        "torque": {"fill_plug": "29 ft-lb", "drain_plug": "15 ft-lb"},
        "washers": {
            "fill_plug": {"type": "crush", "material": "aluminum", "replace": True},
            "drain_plug": {"type": "crush", "material": "aluminum", "replace": True}
        },
        "sockets": {"fill_plug": "24 mm", "drain_plug": "14 mm"},
        "workflow": [
            "Warm transmission to ~40°C",
            "Remove fill plug first",
            "Remove drain plug",
            "Install drain plug (15 ft-lb)",
            "Fill ATF WS",
            "Monitor temp 40–45°C",
            "Open overflow plug until dribble",
            "Install fill plug (29 ft-lb)"
        ]
    },

    # PROPELLER SHAFT
    "propeller_shaft": {
        "interval_km": 12000,
        "workflow": [
            "Grease front U-joints",
            "Grease rear U-joints",
            "Grease front slip yoke",
            "Grease rear slip yoke"
        ]
    },

    # BRAKE FLUID
    "brake_fluid": {
        "interval_km": 48000,
        "workflow": [
            "Use DOT 3 or DOT 4",
            "Bleed sequence: RR → LR → RF → LF"
        ]
    },

    # COOLANT
    "coolant": {
        "interval_km": 160000,
        "secondary_interval_km": 80000,
        "fluid": "Toyota Super Long Life Coolant (Pink)",
        "workflow": [
            "Drain cold engine",
            "Refill with Toyota SLLC Pink",
            "Run engine with heater on",
            "Bleed air system"
        ]
    },

    # CABIN AIR FILTER
    "cabin_air_filter": {
        "interval_km": 16000,
        "workflow": ["Drop glove box", "Replace filter"]
    },

    # ENGINE AIR FILTER
    "engine_air_filter": {
        "interval_km": 24000,
        "workflow": ["Open air box", "Replace filter"]
    },

    # MAF SENSOR
    "maf_sensor": {
        "interval_km": 30000,
        "workflow": ["Remove sensor", "Spray MAF cleaner", "Dry fully", "Reinstall"]
    },

    # THROTTLE BODY
    "throttle_body": {
        "interval_km": 40000,
        "workflow": ["Remove intake hose", "Clean throttle plate", "Reinstall"]
    }
}

# ------------------ UI ------------------

st.set_page_config(page_title="4Runner Workshop OS", layout="centered")
st.title("🔧 2017 4Runner Limited — Workshop OS")

menu = st.radio("", ["📊 Dashboard", "🛠 Service Mode", "📘 Workshop", "📒 History"])

# ------------------ DASHBOARD ------------------

if menu == "📊 Dashboard":
    km = st.number_input("Current KM", 0, step=100)

    if km:
        for name, spec in WORKSHOP.items():
            interval = spec.get("interval_km")
            last = data["last_service"].get(name)

            if interval:
                if last is None:
                    st.warning(f"⚠️ {label(name)} never serviced")
                else:
                    due = last + interval
                    if km >= due:
                        st.error(f"⚠️ {label(name)} DUE (was due at {due} km)")
                    else:
                        remaining = due - km
                        st.success(f"{label(name)}: {remaining} km remaining (due at {due} km)")

# ------------------ SERVICE MODE ------------------

elif menu == "🛠 Service Mode":

    display_map = {label(k): k for k in WORKSHOP.keys()}
    service_display = st.selectbox("Select Service", list(display_map.keys()))
    service = display_map[service_display]

    km = st.number_input("Current KM", 0, step=100)
    notes = st.text_area("Notes")

    spec = WORKSHOP[service]

    st.markdown(f"## 🔧 {label(service)}")

    # FLUID
    st.write("### Fluid")
    st.write(spec.get("fluid", "—"))

    # CAPACITY
    st.write("### Capacity")
    st.write(spec.get("capacity", "—"))

    # INTERVAL
    st.write("### Interval (Primary)")
    st.write(spec.get("interval_km", "—"))
    if "secondary_interval_km" in spec:
        st.write("### Interval (Secondary)")
        st.write(spec.get("secondary_interval_km"))

    st.markdown("---")

    # TORQUE
    if "torque" in spec:
        st.markdown("### 🔧 Torque")
        for k, v in spec["torque"].items():
            st.write(f"- {label(k)}: {v}")

    # SOCKETS
    if "sockets" in spec:
        st.markdown("### 🔩 Sockets")
        for k, v in spec["sockets"].items():
            st.write(f"- {label(k)}: {v}")

    # WASHERS
    if "washers" in spec:
        st.markdown("### 🧰 Washers")
        for k, w in spec["washers"].items():
            st.write(
                f"- {label(k)}: {w['type']} ({w['material']}) | Replace: {w['replace']}"
            )

    # WORKFLOW
    st.markdown("### 📋 Workflow")
    workflow = spec.get("workflow", [])
    if workflow:
        for i, step in enumerate(workflow, 1):
            st.write(f"{i}. {step}")
    else:
        st.write("— No workflow defined —")

    if st.button("✔ Save Service"):
        data["logs"].append({
            "service": service,
            "km": km,
            "date": str(datetime.now()),
            "notes": notes
        })
        data["last_service"][service] = km
        save_data(data)
        st.success("Saved ✔")

# ------------------ WORKSHOP VIEW ------------------

elif menu == "📘 Workshop":
    for name, spec in WORKSHOP.items():
        st.markdown(f"## {label(name)}")

        if "fluid" in spec:
            st.write(f"**Fluid:** {spec['fluid']}")
        if "capacity" in spec:
            st.write(f"**Capacity:** {spec['capacity']}")
        if "interval_km" in spec:
            st.write(f"**Interval:** {spec['interval_km']} km")
        if "secondary_interval_km" in spec:
            st.write(f"**Secondary Interval:** {spec['secondary_interval_km']} km")

        if "torque" in spec:
            st.write("**Torque:**")
            for k, v in spec["torque"].items():
                st.write(f"- {label(k)}: {v}")

        if "sockets" in spec:
            st.write("**Sockets:**")
            for k, v in spec["sockets"].items():
                st.write(f"- {label(k)}: {v}")

        if "washers" in spec:
            st.write("**Washers:**")
            for k, w in spec["washers"].items():
                st.write(
                    f"- {label(k)}: {w['type']} ({w['material']}) | Replace: {w['replace']}"
                )

        if "workflow" in spec:
            st.write("**Workflow:**")
            for i, step in enumerate(spec["workflow"], 1):
                st.write(f"{i}. {step}")

        st.markdown("---")

# ------------------ HISTORY ------------------

elif menu == "📒 History":
    if not data["logs"]:
        st.info("No records yet")
    else:
        for log in reversed(data["logs"]):
            st.markdown(f"### {label(log['service'])}")
            st.write(f"KM: {log['km']}")
            st.write(f"Date: {log['date']}")
            if log["notes"]:
                st.write(f"Notes: {log['notes']}")
            st.markdown("---")
            