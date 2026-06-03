from simulations.aircraft_graph import AircraftHydraulicSystem
from simulations.risk_analysis import HydraulicRiskAnalyzer

def run():

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

    print("\n🚀 AIRCRAFT HYDRAULIC SYSTEM")
    print("Route Risk Score:", risk)

    system.visualize()


if __name__ == "__main__":
    run()