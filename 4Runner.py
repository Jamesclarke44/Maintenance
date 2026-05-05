import streamlit as st
import json
from datetime import datetime

FILE = "4runner_maintenance.json"

# ------------------ SETTINGS ------------------
SCHEDULE = {
    "Engine Oil": 8000,
    "Transmission (Drain & Fill)": 60000,
    "Front Differential": 80000,
    "Rear Differential": 80000,
    "Transfer Case": 80000,
    "Brake Fluid": 40000,
    "Coolant": 160000
}

# ------------------ DATA FUNCTIONS ------------------
def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {"logs": [], "last_service": {}}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ UI ------------------
st.set_page_config(page_title="4Runner Maintenance Tracker", layout="centered")

st.title("🚗 4Runner Maintenance Tracker")

data = load_data()

menu = st.sidebar.radio("Menu", ["Dashboard", "Log Service", "Check Due", "History"])

# ------------------ DASHBOARD ------------------
if menu == "Dashboard":
    st.subheader("📊 Maintenance Overview")

    current_km = st.number_input("Enter current KM", min_value=0, step=100)

    if current_km:
        for service, interval in SCHEDULE.items():
            last_km = data["last_service"].get(service, 0)
            due_km = last_km + interval
            remaining = due_km - current_km

            if current_km >= due_km:
                st.error(f"⚠️ {service} is DUE (last: {last_km} km)")
            else:
                st.success(f"✅ {service}: {remaining} km remaining")

# ------------------ LOG SERVICE ------------------
elif menu == "Log Service":
    st.subheader("🛠 Log Maintenance")

    service = st.selectbox("Service Type", list(SCHEDULE.keys()))
    km = st.number_input("Current KM", min_value=0, step=100)
    notes = st.text_area("Notes (fluid, parts, etc)")

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

        st.success("Service logged successfully!")

# ------------------ CHECK DUE ------------------
elif menu == "Check Due":
    st.subheader("🔧 Maintenance Status Check")

    current_km = st.number_input("Current KM", min_value=0, step=100)

    if st.button("Check"):
        for service, interval in SCHEDULE.items():
            last_km = data["last_service"].get(service, 0)
            due_km = last_km + interval

            if current_km >= due_km:
                st.error(f"⚠️ {service} is DUE")
            else:
                st.info(f"{service} OK (due in {due_km - current_km} km)")

# ------------------ HISTORY ------------------
elif menu == "History":
    st.subheader("📒 Service History")

    if not data["logs"]:
        st.info("No service records yet.")
    else:
        for log in reversed(data["logs"]):
            st.write(f"**{log['date']}**")
            st.write(f"{log['service']} @ {log['km']} km")
            st.write(f"Notes: {log['notes']}")
            st.markdown("---")