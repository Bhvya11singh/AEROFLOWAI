import random
import pandas as pd

from simulations.aircraft_graph import AircraftHydraulicSystem
from simulations.risk_analysis import HydraulicRiskAnalyzer
from simulations.stress_simulation import StressSimulator


def generate_dataset(num_samples=1000):

    dataset = []

    for _ in range(num_samples):

        wind_speed = random.randint(20, 80)
        turbulence = round(random.uniform(0.5, 2.0), 2)

        system = AircraftHydraulicSystem()
        system.build_aircraft()

        simulator = StressSimulator()

        # assign dynamic stress
        for edge in system.graph.edges:

            destination_component = edge[1]

            stress = simulator.compute_stress(
                destination_component,
                wind_speed,
                turbulence
            )

            system.graph.edges[edge]["stress"] = stress

        analyzer = HydraulicRiskAnalyzer(system.graph)

        route = [
            "cockpit",
            "fuselage_center",
            "tail",
            "vertical_fin"
        ]

        route_risk = analyzer.calculate_route_risk(route)

        failure = 1 if route_risk > 3.5 else 0

        dataset.append({
            "wind_speed": wind_speed,
            "turbulence": turbulence,
            "route_risk": route_risk,
            "failure": failure
        })

    return pd.DataFrame(dataset)


if __name__ == "__main__":

    df = generate_dataset(1000)

    print(df.head())

    df.to_csv("hydraulic_system_dataset.csv", index=False)

    print("\nDataset saved successfully.")