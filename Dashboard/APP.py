import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import numpy as np
import joblib
import random

from streamlit_autorefresh import st_autorefresh
from simulations.aircraft_graph import AircraftHydraulicSystem

# -----------------------------
# PAGE CONFIG (NASA STYLE)
# -----------------------------
st.set_page_config# Auto refresh every 1 second (LIVE MODE)
st_autorefresh(interval=1000, key="live_simulation")(
    page_title="Aerospace Hydraulic Control Center",
    layout="wide"
)

st.title("🚀 Aerospace Hydraulic Control Center")
st.markdown("Real-time Aircraft Risk Simulation System")

# -----------------------------
# LOAD MODEL
# -----------------------------
model = joblib.load("hydraulic_failure_model.pkl")

# -----------------------------
# SIDEBAR (MISSION INPUT)
# -----------------------------
st.sidebar.header("Mission Parameters")

wind_speed = random.randint(20, 120)
turbulence = round(random.uniform(0.5, 3.0), 2)
route_risk = round(random.uniform(0.0, 6.0), 2)
# -----------------------------
# PREDICTION ENGINE
# -----------------------------
input_data = np.array([[wind_speed, turbulence, route_risk]])

prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]

# STATUS LOGIC
if probability < 0.3:
    status = "🟢 SAFE"
    color = "green"
elif probability < 0.7:
    status = "🟡 WARNING"
    color = "orange"
else:
    status = "🔴 CRITICAL"

# -----------------------------
# TOP CONTROL PANEL
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("System Status", status)
col2.metric("Failure Probability", f"{probability:.2f}")
col3.metric("ML Prediction", "FAIL" if prediction == 1 else "OK")

st.divider()

# -----------------------------
# AIRCRAFT GRAPH (NASA STYLE HEATMAP)
# -----------------------------
st.subheader("🧠 Aircraft Hydraulic Stress Map")

system = AircraftHydraulicSystem()
system.build_aircraft()

G = system.graph
pos = nx.spring_layout(G, seed=42)

edge_traces = []

# deterministic stress simulation
def compute_stress(u, v):
    base = hash(u + v) % 100
    return (base / 100) * 5  # 0 → 5 scale

def get_color(s):
    if s < 1.5:
        return "#00ff88"  # green
    elif s < 3.0:
        return "#ffcc00"  # yellow
    else:
        return "#ff3333"  # red

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]

    stress = compute_stress(edge[0], edge[1])

    edge_traces.append(
        go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode="lines",
            line=dict(width=5, color=get_color(stress)),
            hoverinfo="text",
            text=f"Stress Level: {stress:.2f}"
        )
    )

# nodes
node_x = []
node_y = []
node_text = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    text=node_text,
    textposition="top center",
    marker=dict(size=18, color="#00d4ff")
)

fig = go.Figure(data=edge_traces + [node_trace])

fig.update_layout(
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="white"),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# SYSTEM ANALYTICS PANEL
# -----------------------------
st.subheader("📊 System Diagnostics")

st.write("Wind Load:", wind_speed)
st.write("Turbulence:", turbulence)
st.write("Route Stress:", route_risk)

st.info("AI continuously evaluates hydraulic system integrity under flight conditions.")