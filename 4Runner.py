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

    "engine_oil": {
        "fluid": "0W-20 Synthetic Oil",
        "capacity": "5.7 L",
        "interval_km": 8000,
        "torque": {"drain_plug": "30 ft-lb"},
        "washers": {
            "drain_plug": {
                "type": "crush",
                "material": "aluminum",
                "replace": True
            }
        },
        "sockets": {"drain_plug": "14 mm"},
        "workflow": [
            "Warm engine",
            "Drain oil",
            "Replace washer",
            "Torque drain plug",
            "Refill oil"
        ]
    },

    "front_differential": {
        "fluid": "75W-85 GL-5",
        "capacity": "1.3 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "washers": {
            "fill_plug": {"type": "crush", "material": "aluminum", "replace": True},
            "drain_plug": {"type": "crush", "material": "aluminum", "replace": True}
        },
        "sockets": {"fill_plug": "24 mm", "drain_plug": "24 mm"},
        "workflow": ["Remove fill plug", "Drain", "Fill until overflow"]
    },

    "rear_differential": {
        "fluid": "75W-85 GL-5",
        "capacity": "2.7 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "washers": {
            "fill_plug": {"type": "crush", "material": "aluminum", "replace": True},
            "drain_plug": {"type": "crush", "material": "aluminum", "replace": True}
        },
        "sockets": {"fill_plug": "24 mm", "drain_plug": "24 mm"},
        "workflow": ["Remove fill plug", "Drain", "Fill until overflow"]
    },

    "transfer_case": {
        "fluid": "75W-90 GL-4/GL-5",
        "capacity": "1.0 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "washers": {
            "fill_plug": {"type": "crush", "material": "aluminum", "replace": True},
            "drain_plug": {"type": "crush", "material": "aluminum", "replace": True}
        },
        "sockets": {"fill_plug": "24 mm", "drain_plug": "24 mm"},
        "workflow": ["Remove fill plug", "Drain", "Fill oil", "Install plug"]
    },

    "transmission": {
        "fluid": "Toyota ATF WS",
        "capacity": "3.0–4.3 L",
        "interval_km": 96000,
        "torque": {"fill_plug": "15 ft-lb", "drain_plug": "29 ft-lb"},
        "washers": {
            "fill_plug": {"type": "crush", "material": "aluminum", "replace": True},
            "drain_plug": {"type": "crush", "material": "aluminum", "replace": True}
        },
        "sockets": {"fill_plug": "24 mm", "drain_plug": "14 mm"},
        "workflow": [
            "Warm transmission",
            "Remove fill plug first",
            "Drain fluid",
            "Reinstall drain plug",
            "Fill ATF WS",
            "Check temp 40–45°C",
            "Install fill plug"
        ]
    },

    "propeller_shaft": {
        "interval_km": 10000,
        "sockets": {"bolts": "14 mm"},
        "workflow": ["Grease U-joints", "Grease slip yoke"]
    },

    "power_steering": {
        "interval_km": 80000,
        "workflow": ["Drain reservoir", "Refill ATF", "Cycle steering lock-to-lock"]
    },

    "brake_fluid": {
        "interval_km": 48000,
        "workflow": ["RR → LR → RF → LF bleed sequence"]
    },

    "coolant": {
        "interval_km": 160000,
        "workflow": ["Drain cold engine", "Refill coolant", "Bleed air system"]
    },

    "cabin_air_filter": {
        "interval_km": 24000,
        "workflow": ["Drop glove box", "Replace filter"]
    },

    "engine_air_filter": {
        "interval_km": 24000,
        "workflow": ["Open air box", "Replace filter"]
    },

    "maf_sensor": {
        "interval_km": 30000,
        "workflow": ["Remove sensor", "Clean MAF spray", "Dry", "Reinstall"]
    },

    "throttle_body": {
        "interval_km": 40000,
        "workflow": ["Remove intake hose", "Clean plate", "Reinstall"]
    }
}

# ------------------ UI ------------------

st.set_page_config(page_title="4Runner Workshop OS", layout="centered")
st.title("🔧 4Runner Workshop OS")

menu = st.radio("", ["📊 Dashboard", "🛠 Service Mode", "📘 Workshop", "📒 History"])

# ------------------ DASHBOARD ------------------

if menu == "📊 Dashboard":
    km = st.number_input("Current KM", 0)

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
                        st.error(f"⚠️ {label(name)} DUE")
                    else:
                        st.success(f"{label(name)}: {due - km} km remaining")

# ------------------ SERVICE MODE (FIXED UI) ------------------

elif menu == "🛠 Service Mode":

    # FIX: no underscores in dropdown
    display_map = {label(k): k for k in WORKSHOP.keys()}
    service_display = st.selectbox("Select Service", list(display_map.keys()))
    service = display_map[service_display]

    km = st.number_input("Current KM", 0)
    notes = st.text_area("Notes")

    spec = WORKSHOP[service]

    st.markdown(f"# 🔧 {label(service)}")

    st.write("### Fluid")
    st.write(spec.get("fluid", "—"))

    st.write("### Capacity")
    st.write(spec.get("capacity", "—"))

    st.write("### Interval")
    st.write(spec.get("interval_km", "—"))

    st.markdown("---")

    # TORQUE
    if "torque" in spec:
        st.markdown("## 🔧 Torque")
        for k, v in spec["torque"].items():
            st.write(f"- {label(k)}: {v}")

    # SOCKETS
    if "sockets" in spec:
        st.markdown("## 🔩 Sockets")
        for k, v in spec["sockets"].items():
            st.write(f"- {label(k)}: {v}")

    # WASHERS
    if "washers" in spec:
        st.markdown("## 🧰 Washers")
        for k, w in spec["washers"].items():
            st.write(
                f"- {label(k)}: {w['type']} ({w['material']}) | Replace: {w['replace']}"
            )

    # WORKFLOW (FIX: NO RAW LIST)
    st.markdown("## 📋 Workflow")

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

        if "workflow" in spec:
            for i, step in enumerate(spec["workflow"], 1):
                st.write(f"{i}. {step}")

        st.markdown("---")

# ------------------ HISTORY ------------------

elif menu == "📒 History":
    if not data["logs"]:
        st.info("No records yet")
    else:
        for log in reversed(data["logs"]):
            st.write(log)