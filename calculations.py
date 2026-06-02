import networkx as nx

G = nx.Graph()

G.add_edge("cockpit", "fuselage", stress=0.3)
G.add_edge("fuselage", "left_wing", stress=0.7)
G.add_edge("fuselage", "tail", stress=0.9)

print(G.edges(data=True))