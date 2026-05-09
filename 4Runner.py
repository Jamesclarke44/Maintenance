import streamlit as st
import json
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================

FILE = "4runner_maintenance.json"
MAX_KM = 300000
SOON_THRESHOLD = 5000

VEHICLE = {
    "year": 2017,
    "model": "4Runner Limited",
    "engine": "1GR-FE 4.0L V6",
    "drivetrain": "Full-Time 4WD"
}

# ============================================================
# DATA
# ============================================================

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        return {
            "logs": [],
            "last_service": {}
        }


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


data = load_data()

# ============================================================
# HELPERS
# ============================================================

def label(text):
    return text.replace("_", " ").title()


def get_next_due_status(km_now, name, spec, last_km):

    interval = spec.get("interval_km")

    if not interval:
        return None

    if last_km is None:
        return {
            "service": name,
            "status": "never",
            "due_km": None,
            "remaining": None
        }

    due_km = last_km + interval
    remaining = due_km - km_now

    if km_now >= due_km:
        status = "overdue"

    elif remaining <= SOON_THRESHOLD:
        status = "soon"

    else:
        status = "ok"

    return {
        "service": name,
        "status": status,
        "due_km": due_km,
        "remaining": remaining
    }

# ============================================================
# WORKSHOP DATABASE
# ============================================================

WORKSHOP = {

    "engine_oil": {
        "category": "Fluids & Drivetrain",
        "difficulty": "Beginner",
        "estimated_time": "30-45 min",
        "fluid": "0W-20 Full Synthetic",
        "capacity": "5.7 L",
        "interval_km": 8000,

        "torque": {
            "drain_plug": "30 ft-lb"
        },

        "sockets": {
            "drain_plug": "14 mm"
        },

        "washers": {
            "drain_plug": {
                "type": "Aluminum Crush Washer",
                "oem": "Toyota 90430-12031"
            }
        },

        "tools": [
            "14 mm socket",
            "Ratchet",
            "Torque wrench",
            "Drain pan",
            "Funnel"
        ],

        "important_notes": [
            "Warm engine before draining",
            "Replace crush washer every oil change"
        ],

        "common_mistakes": [
            "Overtightening drain plug",
            "Overfilling engine oil"
        ],

        "workflow": [
            "Warm engine",
            "Remove drain plug",
            "Install new crush washer",
            "Torque drain plug to 30 ft-lb",
            "Refill with 5.7 L oil",
            "Check oil level"
        ]
    },

    "front_differential": {
        "category": "Fluids & Drivetrain",
        "difficulty": "Intermediate",
        "estimated_time": "45-60 min",
        "fluid": "75W-90 GL-5",
        "capacity": "1.3 L",
        "interval_km": 48000,

        "torque": {
            "fill_plug": "48 ft-lb",
            "drain_plug": "48 ft-lb"
        },

        "sockets": {
            "fill_plug": "24 mm",
            "drain_plug": "24 mm"
        },

        "washers": {
            "fill_plug": {
                "type": "Aluminum Washer",
                "oem": "Toyota 12157-10010"
            },

            "drain_plug": {
                "type": "Aluminum Washer",
                "oem": "Toyota 12157-10010"
            }
        },

        "tools": [
            "24 mm socket",
            "Fluid pump",
            "Torque wrench",
            "Drain pan"
        ],

        "important_notes": [
            "Remove fill plug first",
            "Vehicle must be level"
        ],

        "common_mistakes": [
            "Removing drain plug before fill plug",
            "Using incorrect fluid"
        ],

        "workflow": [
            "Remove fill plug first",
            "Remove drain plug",
            "Drain fluid",
            "Install drain plug",
            "Fill until overflow",
            "Install fill plug"
        ]
    },

    "transmission": {
        "category": "Fluids & Drivetrain",
        "difficulty": "Advanced",
        "estimated_time": "2-3 hours",
        "fluid": "Toyota ATF WS",
        "capacity": "3.0-4.3 L per drain",
        "interval_km": 96000,

        "torque": {
            "fill_plug": "29 ft-lb",
            "drain_plug": "15 ft-lb"
        },

        "sockets": {
            "fill_plug": "24 mm",
            "drain_plug": "14 mm"
        },

        "tools": [
            "ATF pump",
            "Torque wrench",
            "Scan tool"
        ],

        "important_notes": [
            "Vehicle must remain level",
            "Transmission temperature critical"
        ],

        "temperature_notes": [
            "Overflow check at 40-45°C",
            "Too hot = overfilled",
            "Too cold = underfilled"
        ],

        "common_mistakes": [
            "Using non-WS fluid",
            "Incorrect overflow procedure"
        ],

        "workflow": [
            "Warm transmission",
            "Remove fill plug first",
            "Drain fluid",
            "Install drain plug",
            "Fill with WS fluid",
            "Perform overflow procedure"
        ]
    },

    "spark_plugs": {
        "category": "Ignition",
        "difficulty": "Intermediate",
        "estimated_time": "2-3 hours",
        "interval_km": 192000,

        "oem": [
            "Denso FK20HR11",
            "NGK IFR6T11"
        ],

        "torque": {
            "spark_plug": "15 ft-lb"
        },

        "tools": [
            "10 mm socket",
            "14 mm spark plug socket",
            "Extensions",
            "Torque wrench"
        ],

        "important_notes": [
            "Engine should be cool",
            "Use OEM heat range"
        ],

        "common_mistakes": [
            "Cross-threading spark plugs",
            "Overtightening plugs"
        ],

        "workflow": [
            "Remove intake tube",
            "Disconnect coils",
            "Remove spark plugs",
            "Install new plugs",
            "Torque to 15 ft-lb"
        ]
    },

    "tire_rotation": {
        "category": "Tires & Wheels",
        "difficulty": "Beginner",
        "estimated_time": "30-45 min",
        "interval_km": 8000,

        "torque": {
            "lug_nuts": "83 ft-lb"
        },

        "tools": [
            "Jack",
            "Jack stands",
            "21 mm socket",
            "Torque wrench"
        ],

        "important_notes": [
            "Use star torque pattern",
            "Retorque after 100 km"
        ],

        "workflow": [
            "Lift vehicle safely",
            "Rotate tires",
            "Torque lug nuts",
            "Set tire pressures"
        ]
    }
}

# ============================================================
# UI CONFIG
# ============================================================

st.set_page_config(
    page_title="4Runner Workshop OS",
    layout="centered"
)

st.title("🔧 2017 4Runner Limited — Workshop OS")

st.caption(
    f"{VEHICLE['year']} {VEHICLE['model']} • "
    f"{VEHICLE['engine']} • "
    f"{VEHICLE['drivetrain']}"
)

menu = st.radio(
    "",
    [
        "📊 Dashboard",
        "🛠 Service Mode",
        "📘 Workshop",
        "🔧 Torque Lookup",
        "📒 History"
    ]
)

# ============================================================
# DASHBOARD
# ============================================================

if menu == "📊 Dashboard":

    st.subheader("📊 Dashboard")

    km = st.number_input(
        "Current KM",
        0,
        step=100
    )

    st.download_button(
        "⬇ Backup Maintenance Data",
        data=json.dumps(data, indent=4),
        file_name="4runner_backup.json",
        mime="application/json"
    )

    if km:

        overdue = []
        soon = []
        never = []

        for name, spec in WORKSHOP.items():

            last = data["last_service"].get(name)

            status = get_next_due_status(
                km,
                name,
                spec,
                last
            )

            if not status:
                continue

            if status["status"] == "overdue":
                overdue.append(status)

            elif status["status"] == "soon":
                soon.append(status)

            elif status["status"] == "never":
                never.append(status)

        st.markdown("## ✅ Service Summary")

        if overdue:

            st.markdown("### 🔴 Overdue")

            for s in overdue:

                st.error(
                    f"{label(s['service'])} "
                    f"(due at {s['due_km']} km)"
                )

        if soon:

            st.markdown("### 🟠 Due Soon")

            for s in soon:

                st.warning(
                    f"{label(s['service'])} "
                    f"({s['remaining']} km remaining)"
                )

        if never:

            st.markdown("### 🟡 Never Logged")

            for s in never:

                st.warning(
                    f"{label(s['service'])}"
                )

# ============================================================
# SERVICE MODE
# ============================================================

elif menu == "🛠 Service Mode":

    st.subheader("🛠 Service Mode")

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    search = st.text_input("Search Service")

    filtered = {}

    for k, spec in WORKSHOP.items():

        if search:
            if search.lower() not in k.lower():
                continue

        filtered[
            f"{spec['category']} — {label(k)}"
        ] = k

    # --------------------------------------------------------
    # EMPTY SEARCH PROTECTION
    # --------------------------------------------------------

    if not filtered:
        st.warning("No matching services found.")
        st.stop()

    # --------------------------------------------------------
    # SERVICE SELECT
    # --------------------------------------------------------

    service_display = st.selectbox(
        "Select Service",
        sorted(filtered.keys())
    )

    service = filtered[service_display]

    spec = WORKSHOP[service]

    # --------------------------------------------------------
    # INPUTS
    # --------------------------------------------------------

    km = st.number_input(
        "Current KM",
        0,
        step=100
    )

    notes = st.text_area("Notes")

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(f"# 🔧 {label(service)}")

    st.write(f"**Category:** {spec['category']}")

    if "difficulty" in spec:
        st.write(f"**Difficulty:** {spec['difficulty']}")

    if "estimated_time" in spec:
        st.write(f"**Estimated Time:** {spec['estimated_time']}")

    # --------------------------------------------------------
    # FLUID
    # --------------------------------------------------------

    if "fluid" in spec:
        st.markdown("## 🛢 Fluid")
        st.write(spec["fluid"])

    # --------------------------------------------------------
    # CAPACITY
    # --------------------------------------------------------

    if "capacity" in spec:
        st.markdown("## 📦 Capacity")
        st.write(spec["capacity"])

    # --------------------------------------------------------
    # INTERVAL
    # --------------------------------------------------------

    if "interval_km" in spec:
        st.markdown("## 🔁 Interval")
        st.write(f"{spec['interval_km']} km")

    # --------------------------------------------------------
    # OEM
    # --------------------------------------------------------

    if "oem" in spec:
        st.markdown("## 🔌 OEM Parts")

        for item in spec["oem"]:
            st.write(f"- {item}")

    # --------------------------------------------------------
    # WASHERS
    # --------------------------------------------------------

    if "washers" in spec:

        st.markdown("## 🫧 Washers")

        for k, w in spec["washers"].items():

            st.write(
                f"- {label(k)}: "
                f"{w['type']} "
                f"({w['oem']})"
            )

    # --------------------------------------------------------
    # TOOLS
    # --------------------------------------------------------

    if "tools" in spec:

        st.markdown("## 🧰 Tools")

        for t in spec["tools"]:
            st.write(f"- {t}")

    # --------------------------------------------------------
    # TORQUE
    # --------------------------------------------------------

    if "torque" in spec:

        st.markdown("## 🔧 Torque Specs")

        for k, v in spec["torque"].items():

            st.write(
                f"- {label(k)}: {v}"
            )

    # --------------------------------------------------------
    # SOCKETS
    # --------------------------------------------------------

    if "sockets" in spec:

        st.markdown("## 🔩 Socket Sizes")

        for k, v in spec["sockets"].items():

            st.write(
                f"- {label(k)}: {v}"
            )

    # --------------------------------------------------------
    # IMPORTANT NOTES
    # --------------------------------------------------------

    if "important_notes" in spec:

        st.markdown("## ⚠ Important Notes")

        for note in spec["important_notes"]:
            st.warning(note)

    # --------------------------------------------------------
    # TEMPERATURE NOTES
    # --------------------------------------------------------

    if "temperature_notes" in spec:

        st.markdown("## 🌡 Temperature Notes")

        for note in spec["temperature_notes"]:
            st.info(note)

    # --------------------------------------------------------
    # COMMON MISTAKES
    # --------------------------------------------------------

    if "common_mistakes" in spec:

        st.markdown("## ❌ Common Mistakes")

        for mistake in spec["common_mistakes"]:
            st.error(mistake)

    # --------------------------------------------------------
    # WORKFLOW CHECKLIST
    # --------------------------------------------------------

    st.markdown("## 📋 Workflow Checklist")

    workflow = spec.get("workflow", [])

    for i, step in enumerate(workflow):

        st.checkbox(
            step,
            key=f"{service}_{i}"
        )

    # --------------------------------------------------------
    # SAVE BUTTON
    # --------------------------------------------------------

    if st.button("✔ Save Service"):

        data["logs"].append({
            "service": service,
            "km": km,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "notes": notes
        })

        data["last_service"][service] = km

        save_data(data)

        st.success("Service Saved ✔")

# ============================================================
# WORKSHOP
# ============================================================

elif menu == "📘 Workshop":

    st.subheader("📘 Workshop")

    for category in sorted(
        set(spec["category"] for spec in WORKSHOP.values())
    ):

        st.markdown(f"# 🗂 {category}")

        for name, spec in WORKSHOP.items():

            if spec["category"] != category:
                continue

            with st.expander(label(name)):

                for k, v in spec.items():

                    if isinstance(v, list):

                        st.write(f"**{label(k)}:**")

                        for item in v:
                            st.write(f"- {item}")

                    elif isinstance(v, dict):

                        st.write(f"**{label(k)}:**")

                        for kk, vv in v.items():
                            st.write(f"- {label(kk)}: {vv}")

                    else:

                        st.write(
                            f"**{label(k)}:** {v}"
                        )

# ============================================================
# TORQUE LOOKUP
# ============================================================

elif menu == "🔧 Torque Lookup":

    st.subheader("🔧 Torque Lookup")

    query = st.text_input("Search")

    if query:

        q = query.lower()

        for name, spec in WORKSHOP.items():

            if "torque" not in spec:
                continue

            for k, v in spec["torque"].items():

                search_text = f"{name} {k}".lower()

                if q in search_text:

                    st.markdown(
                        f"## {label(name)}"
                    )

                    st.write(
                        f"**Item:** {label(k)}"
                    )

                    st.write(
                        f"**Torque:** {v}"
                    )

                    socket = spec.get(
                        "sockets",
                        {}
                    ).get(k, "—")

                    st.write(
                        f"**Socket:** {socket}"
                    )

                    st.markdown("---")

# ============================================================
# HISTORY
# ============================================================

elif menu == "📒 History":

    st.subheader("📒 History")

    if not data["logs"]:

        st.info("No records yet")

    else:

        for log in reversed(data["logs"]):

            st.markdown(
                f"## {label(log['service'])}"
            )

            st.write(
                f"KM: {log['km']}"
            )

            st.write(
                f"Date: {log['date']}"
            )

            if log["notes"]:
                st.write(
                    f"Notes: {log['notes']}"
                )

            st.markdown("---")