import networkx as nx
import matplotlib.pyplot as plt

from simulations.risk_analysis import HydraulicRiskAnalyzer
from simulations.stress_simulation import StressSimulator


class AircraftHydraulicSystem:

    def __init__(self):
        self.graph = nx.Graph()

    def build_aircraft(self):

        components = [
            "cockpit",
            "fuselage_center",
            "left_wing",
            "right_wing",
            "tail",
            "vertical_fin"
        ]

        self.graph.add_nodes_from(components)

        connections = [
            ("cockpit", "fuselage_center"),
            ("fuselage_center", "left_wing"),
            ("fuselage_center", "right_wing"),
            ("fuselage_center", "tail"),
            ("tail", "vertical_fin")
        ]

        self.graph.add_edges_from(connections)

    def assign_stress_levels(self):

        simulator = StressSimulator()

        wind_speed = 45
        turbulence = 1.4

        for edge in self.graph.edges:

            destination_component = edge[1]

            stress = simulator.compute_stress(
                destination_component,
                wind_speed,
                turbulence
            )

            self.graph.edges[edge]["stress"] = stress

    def visualize(self):

        pos = nx.spring_layout(self.graph, seed=42)

        edge_labels = {
            edge: f"{data['stress']:.2f}"
            for edge, data in self.graph.edges.items()
        }

        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_size=3000,
            font_size=10
        )

        nx.draw_networkx_edge_labels(
            self.graph,
            pos,
            edge_labels=edge_labels
        )

        plt.title("Aircraft Hydraulic System")
        plt.show()


if __name__ == "__main__":

    system = AircraftHydraulicSystem()

    system.build_aircraft()

    system.assign_stress_levels()

    analyzer = HydraulicRiskAnalyzer(system.graph)

    route = [
        "cockpit",
        "fuselage_center",
        "tail",
        "vertical_fin"
    ]

    risk = analyzer.calculate_route_risk(route)

    print(f"Route Risk Score: {risk}")

    system.visualize()