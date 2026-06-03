import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
import sys
import os
import joblib

# =========================================
# ADD PROJECT ROOT TO PYTHON PATH
# =========================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

# =========================================
# IMPORT PROJECT MODULES
# =========================================

from simulations.aircraft_graph import AircraftHydraulicSystem
from simulations.risk_analysis import HydraulicRiskAnalyzer

# =========================================
# LOAD TRAINED ML MODEL
# =========================================

model = joblib.load("hydraulic_failure_model.pkl")

# =========================================
# BUILD AIRCRAFT SYSTEM
# =========================================

system = AircraftHydraulicSystem()

system.build_aircraft()

G = system.graph

# =========================================
# GRAPH POSITIONING
# =========================================

pos = {
    "cockpit": (-1, 0),

    "fuselage_center": (0, 0),

    "left_wing": (-0.5, 1),

    "right_wing": (-0.5, -1),

    "tail": (1, 0),

    "vertical_fin": (1.5, 0.5)
}

# =========================================
# FIGURE SETUP
# =========================================

fig, ax = plt.subplots(figsize=(16, 9))

fig.patch.set_facecolor("#0b0f19")

ax.set_facecolor("#0b0f19")

# =========================================
# LIVE DATA STORAGE
# =========================================

risk_history = []

# =========================================
# STRESS COLOR LOGIC
# =========================================

def get_color(stress):

    if stress < 1.5:
        return "#00ff88"

    elif stress < 3.0:
        return "#ffcc00"

    else:
        return "#ff3333"

# =========================================
# LIVE UPDATE FUNCTION
# =========================================

def update(frame):

    ax.clear()

    ax.set_facecolor("#0b0f19")

    # -------------------------------------
    # RANDOM ENVIRONMENT CONDITIONS
    # -------------------------------------

    wind_speed = random.randint(20, 120)

    turbulence = round(
        random.uniform(0.5, 3.0),
        2
    )

    edge_colors = []

    total_stress = 0

    # -------------------------------------
    # EDGE STRESS CALCULATION
    # -------------------------------------

    for edge in G.edges():

        stress = round(
            (wind_speed / 40) * turbulence
            + random.uniform(0.2, 1.2),
            2
        )

        G.edges[edge]["stress"] = stress

        total_stress += stress

        edge_colors.append(
            get_color(stress)
        )

    # -------------------------------------
    # RISK ANALYSIS
    # -------------------------------------

    analyzer = HydraulicRiskAnalyzer(G)

    route = [
        "cockpit",
        "fuselage_center",
        "tail",
        "vertical_fin"
    ]

    risk = analyzer.calculate_route_risk(route)

    risk_history.append(risk)

    # -------------------------------------
    # AI FAILURE PREDICTION
    # -------------------------------------

    input_data = np.array([[
        wind_speed,
        turbulence,
        risk
    ]])

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    # -------------------------------------
    # SYSTEM STATUS
    # -------------------------------------

    if probability < 0.3:

        system_status = "SAFE"

        status_color = "#00ff88"

    elif probability < 0.7:

        system_status = "WARNING"

        status_color = "#ffcc00"

    else:

        system_status = "CRITICAL"

        status_color = "#ff3333"

    # -------------------------------------
    # DRAW NODES
    # -------------------------------------

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=3500,
        node_color="#00d4ff",
        edgecolors="white",
        linewidths=2
    )

    # -------------------------------------
    # DRAW LABELS
    # -------------------------------------

    nx.draw_networkx_labels(
        G,
        pos,
        font_color="white",
        font_size=10,
        font_weight="bold"
    )

    # -------------------------------------
    # DRAW EDGES
    # -------------------------------------

    nx.draw_networkx_edges(
        G,
        pos,
        width=5,
        edge_color=edge_colors
    )

    # -------------------------------------
    # EDGE LABELS
    # -------------------------------------

    edge_labels = {

        edge: f"{G.edges[edge]['stress']:.2f}"

        for edge in G.edges()
    }

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_color="white",
        font_size=9
    )

    # -------------------------------------
    # TITLE
    # -------------------------------------

    plt.title(
        "🚀 AeroFlowAI - Intelligent Aerospace Monitoring System",
        fontsize=18,
        color="white",
        weight="bold"
    )

    # -------------------------------------
    # HUD PANEL
    # -------------------------------------

    hud_text = f"""
WIND SPEED       : {wind_speed} km/h

TURBULENCE       : {turbulence}

ROUTE RISK       : {risk:.2f}

FAILURE PROB     : {probability:.2f}

ML PREDICTION    : {"FAILURE" if prediction == 1 else "SAFE"}

SYSTEM STATUS    : {system_status}
"""

    ax.text(
        1.6,
        0.6,
        hud_text,
        fontsize=12,
        color=status_color,
        bbox=dict(
            facecolor="#111827",
            edgecolor=status_color,
            boxstyle="round,pad=0.8"
        )
    )

    # -------------------------------------
    # LEGEND
    # -------------------------------------

    ax.text(
        -1.5,
        -1.5,
        "GREEN = SAFE   |   YELLOW = WARNING   |   RED = CRITICAL",
        fontsize=11,
        color="white"
    )

    ax.set_axis_off()

# =========================================
# START LIVE ANIMATION
# =========================================

ani = animation.FuncAnimation(
    fig,
    update,
    interval=1500,
    cache_frame_data=False
)

plt.tight_layout()
plt.show()