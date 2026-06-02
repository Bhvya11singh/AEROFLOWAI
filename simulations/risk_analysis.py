class HydraulicRiskAnalyzer:

    def __init__(self, graph):
        self.graph = graph

    def calculate_route_risk(self, route):

        total_risk = 0

        for i in range(len(route) - 1):

            edge = (route[i], route[i + 1])

            stress = self.graph.edges[edge]["stress"]

            total_risk += stress

        return round(total_risk, 2)