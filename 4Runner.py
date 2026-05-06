import streamlit as st
import json
from datetime import datetime

FILE = "4runner_maintenance.json"
MAX_KM = 300000
SOON_THRESHOLD = 5000  # km

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

# ------------------ WORKSHOP DATABASE (CATEGORIZED) ------------------

WORKSHOP = {

    # ============================================================
    # FLUIDS & DRIVETRAIN
    # ============================================================

    "engine_oil": {
        "category": "Fluids & Drivetrain",
        "fluid": "0W-20 Full Synthetic",
        "capacity": "5.7 L",
        "interval_km": 8000,
        "torque": {"drain_plug": "30 ft-lb"},
        "sockets": {"drain_plug": "14 mm"},
        "tools": [
            "14 mm socket",
            "Ratchet",
            "Torque wrench (10–80 ft-lb)",
            "Oil drain pan",
            "Funnel"
        ],
        "workflow": [
            "Warm engine",
            "Remove drain plug",
            "Install new crush washer",
            "Torque drain plug to 30 ft-lb",
            "Refill 5.7 L 0W-20",
            "Check level"
        ]
    },

    "front_differential": {
        "category": "Fluids & Drivetrain",
        "fluid": "75W-90 GL-5",
        "capacity": "1.3 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "48 ft-lb", "drain_plug": "48 ft-lb"},
        "sockets": {"fill_plug": "24 mm", "drain_plug": "24 mm"},
        "tools": [
            "24 mm socket",
            "Ratchet",
            "Torque wrench (10–100 ft-lb)",
            "Fluid pump",
            "Drain pan"
        ],
        "workflow": [
            "Remove fill plug first",
            "Remove drain plug",
            "Drain fluid completely",
            "Install drain plug (48 ft-lb)",
            "Fill until fluid drips from fill hole",
            "Install fill plug (48 ft-lb)"
        ]
    },

    "rear_differential": {
        "category": "Fluids & Drivetrain",
        "fluid": "75W-90 GL-5",
        "capacity": "2.7 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "36 ft-lb", "drain_plug": "36 ft-lb"},
        "sockets": {"fill_plug": "24 mm", "drain_plug": "24 mm"},
        "tools": [
            "24 mm socket",
            "Ratchet",
            "Torque wrench (10–100 ft-lb)",
            "Fluid pump",
            "Drain pan"
        ],
        "workflow": [
            "Remove fill plug first",
            "Remove drain plug",
            "Drain fluid",
            "Install drain plug (36 ft-lb)",
            "Fill until overflow",
            "Install fill plug (36 ft-lb)"
        ]
    },

    "transfer_case": {
        "category": "Fluids & Drivetrain",
        "fluid": "75W-90 GL-5 (Toyota LF 75W equivalent)",
        "capacity": "1.0 L",
        "interval_km": 48000,
        "torque": {"fill_plug": "27 ft-lb", "drain_plug": "27 ft-lb"},
        "sockets": {"fill_plug": "24 mm", "drain_plug": "24 mm"},
        "tools": [
            "24 mm socket",
            "Ratchet",
            "Torque wrench (10–80 ft-lb)",
            "Fluid pump",
            "Drain pan"
        ],
        "workflow": [
            "Remove fill plug first",
            "Remove drain plug",
            "Drain fluid",
            "Install drain plug (27 ft-lb)",
            "Fill until overflow",
            "Install fill plug (27 ft-lb)"
        ]
    },

    "transmission": {
        "category": "Fluids & Drivetrain",
        "fluid": "Toyota ATF WS",
        "capacity": "3.0–4.3 L per drain",
        "interval_km": 96000,
        "torque": {"fill_plug": "29 ft-lb", "drain_plug": "15 ft-lb"},
        "sockets": {"fill_plug": "24 mm", "drain_plug": "14 mm"},
        "tools": [
            "24 mm socket",
            "14 mm socket",
            "Torque wrench",
            "ATF fill pump",
            "Scan tool or temp monitoring"
        ],
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

    "brake_fluid": {
        "category": "Fluids & Drivetrain",
        "interval_km": 48000,
        "fluid": "DOT 3 or DOT 4",
        "capacity": "Approx. 1 L",
        "tools": [
            "Brake bleeder",
            "8/10 mm line wrench",
            "Catch bottle"
        ],
        "workflow": [
            "Bleed sequence: RR → LR → RF → LF"
        ]
    },

    "coolant": {
        "category": "Fluids & Drivetrain",
        "interval_km": 160000,
        "secondary_interval_km": 80000,
        "fluid": "Toyota Super Long Life Coolant (Pink)",
        "capacity": "Approx. 11.4 L",
        "tools": [
            "Drain pan",
            "Funnel",
            "Spill-free funnel"
        ],
        "workflow": [
            "Drain cold engine",
            "Refill with Toyota SLLC Pink",
            "Run engine with heater on",
            "Bleed air system"
        ]
    },

    "propeller_shaft": {
        "category": "Fluids & Drivetrain",
        "interval_km": 12000,
        "grease_type": "NLGI #2 Lithium EP Moly Grease",
        "grease_amount": "1–3 pumps per zerk",
        "tools": [
            "Grease gun",
            "Moly grease cartridges"
        ],
        "workflow": [
            "Grease front U-joints",
            "Grease rear U-joints",
            "Grease front slip yoke",
            "Grease rear slip yoke"
        ]
    },

    # ============================================================
    # FILTERS & AIR SYSTEM
    # ============================================================

    "engine_air_filter": {
        "category": "Filters & Air System",
        "interval_km": 24000,
        "tools": ["None"],
        "workflow": ["Open air box", "Replace filter"]
    },

    "cabin_air_filter": {
        "category": "Filters & Air System",
        "interval_km": 16000,
        "tools": ["None"],
        "workflow": ["Drop glove box", "Replace filter"]
    },

    "MAF_sensor": {
        "category": "Filters & Air System",
        "interval_km": 30000,
        "tools": ["Screwdriver", "MAF cleaner"],
        "workflow": [
            "Remove sensor",
            "Spray MAF cleaner",
            "Dry fully",
            "Reinstall"
        ]
    },

    "throttle_body": {
        "category": "Filters & Air System",
        "interval_km": 40000,
        "tools": ["Screwdriver", "Throttle body cleaner"],
        "workflow": [
            "Remove intake hose",
            "Clean throttle plate",
            "Reinstall"
        ]
    },

    # ============================================================
    # IGNITION
    # ============================================================

    "spark_plugs": {
        "category": "Ignition",
        "interval_km": 192000,
        "tools": [
            "10 mm socket",
            "14 mm spark plug socket",
            "Extensions",
            "Torque wrench"
        ],
        "torque": {"spark_plug": "15 ft-lb"},
        "workflow": [
            "Remove intake tube",
            "Disconnect coil connectors",
            "Remove coils",
            "Remove spark plugs",
            "Install new plugs (15 ft-lb)",
            "Reinstall coils and intake"
        ]
    },

    # ============================================================
    # BELTS
    # ============================================================

    "serpentine_belt": {
        "category": "Belts",
        "interval_km": 160000,
        "tools": [
            "14 mm wrench",
            "Breaker bar",
            "Belt routing diagram"
        ],
        "workflow": [
            "Release tensioner",
            "Remove belt",
            "Route new belt",
            "Apply tension"
        ]
    },

    # ============================================================
    # BRAKES
    # ============================================================

    "front_brake_pads": {
        "category": "Brakes",
        "interval_km": 50000,
        "tools": [
            "14 mm socket",
            "C-clamp",
            "Brake cleaner"
        ],
        "torque": {"caliper_bolts": "91 ft-lb"},
        "workflow": [
            "Remove caliper",
            "Compress piston",
            "Install new pads",
            "Torque caliper bolts to 91 ft-lb"
        ]
    },

    "rear_brake_pads": {
        "category": "Brakes",
        "interval_km": 50000,
        "tools": [
            "14 mm socket",
            "C-clamp",
            "Brake cleaner"
        ],
        "torque": {"caliper_bolts": "65 ft-lb"},
        "workflow": [
            "Remove caliper",
            "Compress piston",
            "Install new pads",
            "Torque caliper bolts to 65 ft-lb"
        ]
    },

    "rotor_thickness": {
        "category": "Brakes",
        "interval_km": 50000,
        "tools": ["Micrometer"],
        "workflow": [
            "Measure rotor thickness",
            "Compare to minimum spec"
        ]
    },

    # ============================================================
    # TIRES & WHEELS
    # ============================================================

    "tire_rotation": {
        "category": "Tires & Wheels",
        "interval_km": 8000,
        "tools": ["Jack", "Jack stands", "21 mm socket"],
        "workflow": [
            "Lift vehicle",
            "Rotate tires in cross pattern",
            "Check tread depth"
        ]
    },

    "lug_nut_torque": {
        "category": "Tires & Wheels",
        "interval_km": 8000,
        "torque": {"lug_nuts": "83 ft-lb"},
        "tools": ["21 mm socket", "Torque wrench"],
        "workflow": [
            "Torque lug nuts to 83 ft-lb"
        ]
    },

    "tread_depth": {
        "category": "Tires & Wheels",
        "interval_km": 8000,
        "tools": ["Tread depth gauge"],
        "workflow": [
            "Measure tread depth at 3 points per tire"
        ]
    },

    # ============================================================
    # ENGINE COMPONENTS
    # ============================================================

    "PCV_valve": {
        "category": "Engine Components",
        "interval_km": 96000,
        "tools": ["Pliers", "Replacement PCV valve"],
        "workflow": [
            "Remove PCV hose",
            "Unscrew PCV valve",
            "Install new valve"
        ]
    },

    "battery_service": {
        "category": "Engine Components",
        "interval_km": 24000,
        "tools": ["Battery brush", "Dielectric grease"],
        "workflow": [
            "Clean terminals",
            "Apply dielectric grease",
            "Check voltage"
        ]
    },

    "fuel_system_cleaner": {
        "category": "Engine Components",
        "interval_km": 16000,
        "tools": ["Fuel system cleaner bottle"],
        "workflow": [
            "Pour cleaner into fuel tank"
        ]
    },

    "radiator_cap": {
        "category": "Engine Components",
        "interval_km": 80000,
        "tools": ["None"],
        "workflow": [
            "Inspect cap seal",
            "Replace if cracked or hardened"
        ]
    },

    "coolant_hoses": {
        "category": "Engine Components",
        "interval_km": 80000,
        "tools": ["Pliers", "Hose clamp tool"],
        "workflow": [
            "Inspect hoses for cracks",
            "Replace if swollen or leaking"
        ]
    },

    # ============================================================
    # SUSPENSION & STEERING
    # ============================================================

    "suspension_grease_points": {
        "category": "Suspension & Steering",
        "interval_km": 24000,
        "tools": ["Grease gun"],
        "workflow": [
            "Grease upper control arm bushings",
            "Grease lower control arm bushings"
        ]
    },

    "wheel_bearings": {
        "category": "Suspension & Steering",
        "interval_km": 96000,
        "tools": ["Pry bar", "Dial indicator"],
        "workflow": [
            "Check for play",
            "Replace if excessive movement"
        ]
    },

    "alignment_check": {
        "category": "Suspension & Steering",
        "interval_km": 24000,
        "tools": ["Alignment rack"],
        "workflow": [
            "Check toe, camber, caster",
            "Adjust if out of spec"
        ]
    },

    "power_steering_inspection": {
        "category": "Suspension & Steering",
        "interval_km": 24000,
        "tools": ["None"],
        "workflow": [
            "Inspect electric steering components",
            "Check for noises or binding"
        ]
    },

    # ============================================================
    # BREATHERS
    # ============================================================

    "diff_breather": {
        "category": "Breathers",
        "interval_km": 48000,
        "tools": ["Wrench"],
        "workflow": [
            "Inspect breather",
            "Ensure it moves freely",
            "Replace if clogged"
        ]
    },

    "transfer_case_breather": {
        "category": "Breathers",
        "interval_km": 48000,
        "tools": ["Wrench"],
        "workflow": [
            "Inspect breather",
            "Replace if stuck"
        ]
    },

    # ============================================================
    # EXTERIOR
    # ============================================================

    "wiper_blades": {
        "category": "Exterior",
        "interval_km": 12000,
        "tools": ["None"],
        "workflow": [
            "Lift wiper arm",
            "Remove old blade",
            "Install new blade"
        ]
    }
}
# ------------------ PARTS DATABASE ------------------

PARTS = {
    "filters": {
        "engine_oil_filter": {
            "label": "Engine Oil Filter",
            "oem": "Toyota 04152-YZZA5",
            "notes": "Cartridge type"
        },
        "engine_air_filter": {
            "label": "Engine Air Filter",
            "oem": "Toyota 17801-31120",
            "notes": ""
        },
        "cabin_air_filter": {
            "label": "Cabin Air Filter",
            "oem": "Toyota 87139-07010",
            "notes": "Charcoal optional"
        }
    },

    "washers": {
        "engine_oil_drain": {
            "label": "Engine Oil Drain Plug Washer",
            "oem": "Toyota 90430-12031",
            "notes": "Aluminum crush washer"
        },
        "front_diff_drain": {
            "label": "Front Diff Drain/Fill Washer",
            "oem": "Toyota 12157-10010",
            "notes": "Aluminum"
        },
        "rear_diff_drain": {
            "label": "Rear Diff Drain/Fill Washer",
            "oem": "Toyota 12157-10010",
            "notes": "Same as front diff"
        },
        "transfer_case": {
            "label": "Transfer Case Plug Washer",
            "oem": "Toyota 90430-24003",
            "notes": ""
        },
        "transmission": {
            "label": "Transmission Drain Plug Washer",
            "oem": "Toyota 90430-12031",
            "notes": "Same as engine oil"
        }
    },

    "fluids": {
        "engine_oil": {
            "label": "Engine Oil",
            "spec": "0W-20 Full Synthetic",
            "capacity": "5.7 L"
        },
        "front_diff": {
            "label": "Front Differential",
            "spec": "75W-90 GL-5",
            "capacity": "1.3 L"
        },
        "rear_diff": {
            "label": "Rear Differential",
            "spec": "75W-90 GL-5",
            "capacity": "2.7 L"
        },
        "transfer_case": {
            "label": "Transfer Case",
            "spec": "75W-90 GL-5 (Toyota LF 75W equivalent)",
            "capacity": "1.0 L"
        },
        "transmission": {
            "label": "Automatic Transmission",
            "spec": "Toyota ATF WS",
            "capacity": "3.0–4.3 L per drain"
        },
        "coolant": {
            "label": "Engine Coolant",
            "spec": "Toyota Super Long Life Coolant (Pink)",
            "capacity": "Approx. 11.4 L"
        },
        "brake_fluid": {
            "label": "Brake Fluid",
            "spec": "DOT 3 or DOT 4",
            "capacity": "Approx. 1 L"
        },
        "prop_shaft_grease": {
            "label": "Propeller Shaft Grease",
            "spec": "NLGI #2 Lithium EP Moly Grease",
            "capacity": "1–3 pumps per zerk"
        }
    }
}

# ------------------ UI CONFIG ------------------

st.set_page_config(page_title="4Runner Workshop OS", layout="centered")
st.title("🔧 2017 4Runner Limited — Workshop OS")

menu = st.radio(
    "",
    [
        "📊 Dashboard",
        "🛠 Service Mode",
        "📘 Workshop",
        "🔧 Torque Lookup",
        "🧰 Parts Database",
        "📅 Maintenance Timeline",
        "📒 History"
    ]
)

# ------------------ DASHBOARD ------------------

if menu == "📊 Dashboard":
    st.subheader("📊 Dashboard")

    km = st.number_input("Current KM", 0, step=100)

    if km:

        st.markdown("### ✅ Next-Due Summary")

        overdue = []
        soon = []
        never = []
        ok = []

        for name, spec in WORKSHOP.items():
            last = data["last_service"].get(name)
            status = get_next_due_status(km, name, spec, last)
            if not status:
                continue

            if status["status"] == "overdue":
                overdue.append(status)
            elif status["status"] == "soon":
                soon.append(status)
            elif status["status"] == "never":
                never.append(status)
            else:
                ok.append(status)

        if overdue:
            st.markdown("#### 🔴 Overdue")
            for s in overdue:
                st.error(
                    f"{label(s['service'])} — DUE (was due at {s['due_km']} km)"
                )

        if soon:
            st.markdown("#### 🟠 Due Soon (≤ 5,000 km)")
            for s in soon:
                st.warning(
                    f"{label(s['service'])} — {s['remaining']} km remaining (due at {s['due_km']} km)"
                )

        if never:
            st.markdown("#### 🟡 Never Serviced")
            for s in never:
                st.warning(f"{label(s['service'])} — never logged")

        if not overdue and not soon and not never:
            st.success("All interval-based services are up to date.")

        st.markdown("---")
        st.markdown("### 📋 Detailed Status")

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
                        st.info(f"{label(name)}: {remaining} km remaining (due at {due} km)")
# ------------------ SERVICE MODE ------------------

elif menu == "🛠 Service Mode":

    st.subheader("🛠 Service Mode")

    # Build dropdown with category labels
    display_map = {f"{spec['category']} — {label(k)}": k for k, spec in WORKSHOP.items()}
    service_display = st.selectbox("Select Service", sorted(display_map.keys()))
    service = display_map[service_display]

    km = st.number_input("Current KM", 0, step=100)
    notes = st.text_area("Notes")

    spec = WORKSHOP[service]

    st.markdown(f"## 🔧 {label(service)}")

    # CATEGORY
    st.write(f"**Category:** {spec['category']}")

    # FLUID
    if "fluid" in spec:
        st.write("### Fluid")
        st.write(spec["fluid"])

    # CAPACITY
    if "capacity" in spec:
        st.write("### Capacity")
        st.write(spec["capacity"])

    # INTERVALS
    if "interval_km" in spec:
        st.write("### Interval (Primary)")
        st.write(f"{spec['interval_km']} km")

    if "secondary_interval_km" in spec:
        st.write("### Interval (Secondary)")
        st.write(f"{spec['secondary_interval_km']} km")

    st.markdown("---")

    # TOOLS
    if "tools" in spec:
        st.markdown("### 🧰 Tools Needed")
        for t in spec["tools"]:
            st.write(f"- {t}")

    # TORQUE
    if "torque" in spec:
        st.markdown("### 🔧 Torque Specs")
        for k, v in spec["torque"].items():
            st.write(f"- {label(k)}: {v}")

    # SOCKETS
    if "sockets" in spec:
        st.markdown("### 🔩 Socket Sizes")
        for k, v in spec["sockets"].items():
            st.write(f"- {label(k)}: {v}")

    # GREASE
    if "grease_type" in spec:
        st.markdown("### 🧴 Grease")
        st.write(f"Type: {spec['grease_type']}")
        st.write(f"Amount: {spec['grease_amount']}")

    # WORKFLOW
    st.markdown("### 📋 Workflow")
    workflow = spec.get("workflow", [])
    if workflow:
        for i, step in enumerate(workflow, 1):
            st.write(f"{i}. {step}")
    else:
        st.write("— No workflow defined —")

    # SAVE BUTTON
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

# ------------------ WORKSHOP VIEW (CATEGORIZED) ------------------

elif menu == "📘 Workshop":

    st.markdown("## 📘 Workshop — All Services (Categorized)")

    # Build category groups
    categories = {}
    for name, spec in WORKSHOP.items():
        cat = spec["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((name, spec))

    # Display categories
    for category, items in categories.items():
        st.markdown(f"## 🗂 {category}")

        for name, spec in items:
            with st.expander(label(name)):

                if "fluid" in spec:
                    st.write(f"**Fluid:** {spec['fluid']}")

                if "capacity" in spec:
                    st.write(f"**Capacity:** {spec['capacity']}")

                if "interval_km" in spec:
                    st.write(f"**Interval:** {spec['interval_km']} km")

                if "secondary_interval_km" in spec:
                    st.write(f"**Secondary Interval:** {spec['secondary_interval_km']} km")

                if "torque" in spec:
                    st.write("**Torque Specs:**")
                    for k, v in spec["torque"].items():
                        st.write(f"- {label(k)}: {v}")

                if "sockets" in spec:
                    st.write("**Socket Sizes:**")
                    for k, v in spec["sockets"].items():
                        st.write(f"- {label(k)}: {v}")

                if "grease_type" in spec:
                    st.write(f"**Grease Type:** {spec['grease_type']}")
                    st.write(f"**Grease Amount:** {spec['grease_amount']}")

                if "tools" in spec:
                    st.write("**Tools Needed:**")
                    for t in spec["tools"]:
                        st.write(f"- {t}")

                if "workflow" in spec:
                    st.write("**Workflow:**")
                    for i, step in enumerate(spec["workflow"], 1):
                        st.write(f"{i}. {step}")

# ------------------ TORQUE LOOKUP ------------------

elif menu == "🔧 Torque Lookup":

    st.subheader("🔧 Torque & Socket Lookup")

    query = st.text_input("Search (e.g., 'drain', 'front diff', 'caliper bolts', 'spark plug')")

    if query:
        q = query.lower()
        results = []

        for name, spec in WORKSHOP.items():
            if "torque" in spec:
                for k, v in spec["torque"].items():
                    text = f"{label(name)} {label(k)}"
                    if q in text.lower():
                        results.append({
                            "service": label(name),
                            "item": label(k),
                            "torque": v,
                            "socket": spec.get("sockets", {}).get(k, "—"),
                            "category": spec["category"]
                        })

        if results:
            for r in results:
                st.markdown(f"### {r['service']} — {r['item']}")
                st.write(f"**Category:** {r['category']}")
                st.write(f"**Torque:** {r['torque']}")
                st.write(f"**Socket:** {r['socket']}")
                st.markdown("---")
        else:
            st.info("No matching torque entries found.")
    else:
        st.info("Type a keyword to search torque and socket specs.")
# ------------------ PARTS DATABASE UI ------------------

elif menu == "🧰 Parts Database":

    st.subheader("🧰 Parts & Fluids Database")

    section = st.selectbox("Category", ["Filters", "Washers", "Fluids"])

    if section == "Filters":
        st.markdown("### 🧼 Filters")
        for key, p in PARTS["filters"].items():
            st.markdown(f"**{p['label']}**")
            st.write(f"OEM: {p['oem']}")
            if p["notes"]:
                st.write(f"Notes: {p['notes']}")
            st.markdown("---")

    elif section == "Washers":
        st.markdown("### 🫧 Crush Washers")
        for key, p in PARTS["washers"].items():
            st.markdown(f"**{p['label']}**")
            st.write(f"OEM: {p['oem']}")
            if p["notes"]:
                st.write(f"Notes: {p['notes']}")
            st.markdown("---")

    elif section == "Fluids":
        st.markdown("### 🛢 Fluids")
        for key, p in PARTS["fluids"].items():
            st.markdown(f"**{p['label']}**")
            st.write(f"Spec: {p['spec']}")
            st.write(f"Capacity: {p['capacity']}")
            st.markdown("---")

# ------------------ MAINTENANCE TIMELINE (DROPDOWN VERSION) ------------------

elif menu == "📅 Maintenance Timeline":

    st.subheader("📅 Maintenance Timeline (0–300,000 km)")

    km_now = st.number_input("Current KM", 0, step=100)

    st.markdown("### 📂 Select a service to view its full timeline")

    for name, spec in WORKSHOP.items():

        interval = spec.get("interval_km")
        if not interval:
            continue  # skip items without intervals

        with st.expander(f"{spec['category']} — {label(name)}"):

            last = data["last_service"].get(name)

            st.write(f"**Primary Interval:** {interval} km")
            if "secondary_interval_km" in spec:
                st.write(f"**Secondary Interval:** {spec['secondary_interval_km']} km")

            if last is not None:
                st.write(f"**Last Recorded Service:** {last} km")
            else:
                st.write("**Last Recorded Service:** —")

            st.markdown("#### 🔧 Service Points (0–300,000 km)")

            # Generate interval points
            points = []
            km_point = interval
            while km_point <= MAX_KM:
                points.append(km_point)
                km_point += interval

            # Display timeline with status
            for p in points:
                status = ""
                if km_now:
                    if last is not None and last >= p:
                        status = "✅ done"
                    elif km_now >= p:
                        status = "🔴 overdue"
                    elif p - km_now <= SOON_THRESHOLD:
                        status = "🟠 soon"
                    else:
                        status = "⚪ upcoming"

                st.write(f"- {p} km {status}")

            st.markdown("---")

# ------------------ HISTORY ------------------

elif menu == "📒 History":
    st.subheader("📒 Service History")

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
