import streamlit as st
import json
from datetime import datetime

FILE = "4runner_maintenance.json"

# ------------------ SETTINGS ------------------
SCHEDULE = {
    "Engine Oil": 8000,
    "Transmission (Drain & Fill)": 60000,
    "Front Differential": 30000,
    "Rear Differential": 30000,
    "Transfer Case": 30000,
    "Brake Fluid": 40000,
    "Coolant": 160000
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

# ------------------ MOBILE UI SETTINGS ------------------
st.set_page_config(page_title="4Runner Tracker", layout="centered")

st.title("🚗 4Runner Maintenance")

menu = st.radio("", ["📊 Status", "🛠 Log", "✏️ Edit / Fix", "📒 History"])

# ------------------ STATUS ------------------
if menu == "📊 Status":
    st.subheader("Maintenance Status")

    km = st.number_input("Current KM", min_value=0, step=100)

    if km:
        for service, interval in SCHEDULE.items():
            last = data["last_service"].get(service, 0)
            due = last + interval

            if km >= due:
                st.error(f"⚠️ {service} DUE")
            else:
                st.success(f"{service}: {due - km} km left")

# ------------------ LOG ------------------
elif menu == "🛠 Log":
    st.subheader("Add Service")

    service = st.selectbox("Service", list(SCHEDULE.keys()))
    km = st.number_input("KM", min_value=0, step=100)
    notes = st.text_area("Notes")

    if st.button("Save"):
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

# ------------------ EDIT / FIX ------------------
elif menu == "✏️ Edit / Fix":
    st.subheader("Fix or Delete Entries")

    if not data["logs"]:
        st.info("No logs yet.")
    else:
        for i, log in enumerate(data["logs"]):
            st.markdown("---")

            st.write(f"**{log['service']} @ {log['km']} km**")
            st.write(log["notes"])

            col1, col2 = st.columns(2)

            # DELETE BUTTON
            with col1:
                if st.button(f"Delete {i}"):
                    service = log["service"]

                    data["logs"].pop(i)

                    # reset last_service safely
                    remaining = [l for l in data["logs"] if l["service"] == service]
                    if remaining:
                        data["last_service"][service] = max(l["km"] for l in remaining)
                    else:
                        data["last_service"].pop(service, None)

                    save_data(data)
                    st.rerun()

            # FIX BUTTON
            with col2:
                new_km = st.number_input(f"Fix KM {i}", value=log["km"], step=100)

                if st.button(f"Update {i}"):
                    data["logs"][i]["km"] = new_km

                    service = log["service"]
                    data["last_service"][service] = new_km

                    save_data(data)
                    st.rerun()

# ------------------ HISTORY ------------------
elif menu == "📒 History":
    st.subheader("Service History")

    if not data["logs"]:
        st.info("No records yet.")
    else:
        for log in reversed(data["logs"]):
            st.write(f"**{log['date']}**")
            st.write(f"{log['service']} @ {log['km']} km")
            st.write(log["notes"])
            st.markdown("---")