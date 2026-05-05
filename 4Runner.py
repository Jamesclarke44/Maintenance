import streamlit as st
import json
from datetime import datetime

FILE = "4runner_maintenance.json"

# ------------------ WORKSHOP SPEC DATABASE ------------------
WORKSHOP = {
    "Engine Oil": {
        "fluid": "0W-20 Synthetic Oil",
        "capacity": "5.7 L",
        "interval_km": 8000,
        "notes": "Oil + filter change"
    },
    "Transmission (Drain & Fill)": {
        "fluid": "Toyota ATF WS",
        "capacity": "3.0–4.3 L",
        "interval_km": 150000,
        "temp": "40–45°C",
        "torque": "20 Nm (check plug)"
    },
    "Front Differential": {
        "fluid": "75W-85 GL-5",
        "capacity": "1.3 L",
        "interval_km": 80000,
        "torque": "65 Nm"
    },
    "Rear Differential": {
        "fluid": "75W-85 GL-5",
        "capacity": "2.7 L",
        "interval_km": 80000,
        "torque": "65 Nm"
    },
    "Transfer Case": {
        "fluid": "75W-90 GL-4/GL-5",
        "capacity": "1.0 L",
        "interval_km": 80000,
        "torque": "65 Nm"
    },
    "Brake Fluid": {
        "fluid": "DOT 3",
        "capacity": "0.8–1.0 L flush",
        "interval_km": 0,
        "interval_years": 2
    },
    "Coolant": {
        "fluid": "Toyota SLLC (Pink)",
        "capacity": "11–12 L",
        "interval_km": 160000,
        "interval_after": 80000
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

menu = st.radio("", ["📊 Dashboard", "🛠 Service", "📘 Workshop Specs", "📒 History"])

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

# ------------------ SERVICE LOG ------------------
elif menu == "🛠 Service":
    st.subheader("Log Service")

    service = st.selectbox("Select System", list(WORKSHOP.keys()))
    km = st.number_input("Current KM", min_value=0, step=100)
    notes = st.text_area("Notes")

    spec = WORKSHOP[service]

    st.markdown("### 🔧 Factory Spec")
    st.write(f"Fluid: {spec.get('fluid','-')}")
    st.write(f"Capacity: {spec.get('capacity','-')}")
    st.write(f"Interval: {spec.get('interval_km','Time-based')}")
    if "torque" in spec:
        st.write(f"Torque: {spec['torque']}")
    if "temp" in spec:
        st.write(f"Temp: {spec['temp']}")

    if st.button("Save Service"):
        entry = {
            "service": service,
            "km": km,
            "date": str(datetime.now()),
            "notes": notes
        }

        data["logs"].append(entry)
        data["last_service"][service] = km
        save_data(data)

        st.success("Service logged ✔️")

# ------------------ WORKSHOP SPECS ------------------
elif menu == "📘 Workshop Specs":
    st.subheader("Factory Specifications")

    for name, spec in WORKSHOP.items():
        st.markdown("---")
        st.write(f"### {name}")
        st.write(f"Fluid: {spec.get('fluid','-')}")
        st.write(f"Capacity: {spec.get('capacity','-')}")
        st.write(f"Interval: {spec.get('interval_km','Time-based')} km")
        if "interval_after" in spec:
            st.write(f"After first change: {spec['interval_after']} km")
        if "torque" in spec:
            st.write(f"Torque: {spec['torque']}")

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