from pyvis.network import Network
from src.utils import parse_neighbors
from src.CSPclass import *
from src.algorithms import AC3
import streamlit as st

titles = ["Algorithms I",
          "Intro to File and Database Management",
          "Practical Programming Methodology",
          "Computer Organization and Arcitecture",
          "Linear Algebra I",
          "Intro to Applied Statistics",
          "Operating Systems"]
neighbors = parse_neighbors('A: B; A: C; B: D; D: E; B: C; C: E; C: F; F: G')
domains = { 'A': ["Mon", "Tue", "Wed"], 
            'B': ["Tue"],
            'C': ["Mon", "Tue", "Wed"],
            'D': ["Mon", "Tue", "Wed"],
            'E': ["Mon", "Tue", "Wed"],
            'F': ["Wed"],
            'G': ["Mon", "Tue", "Wed"],}
constraints = lambda X, x, Y, y: x!=y
task1CSP = CSPBasic(variables=None, domains=domains, neighbors=neighbors, constraints=constraints)

net_task1 = Network( heading="Lab6. Task 1",
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%"
)
nodes=task1CSP.domains
sizes=10*len(nodes)
nodeTitles=[]

for node in nodes:
    nodeTitles.append(nodes[node])
nodes=list(nodes)
i=0 #tmp variable for add_node
for node in nodes:
    net_task1.add_node(node, label=titles[i], title=", ".join(nodeTitles[i]))
    i+=1
for nodeFrom in task1CSP.neighbors.keys():
    for nodeTo in task1CSP.neighbors[nodeFrom]:
        net_task1.add_edge(nodeFrom, nodeTo, size=sizes)
net_task1.show("Task1Graph.html", notebook=False)

AC3(task1CSP)

net_task1_AC3 = Network( heading="Lab6. Task 1 after AC3",
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%"
)
nodes=task1CSP.curr_domains
sizes=10*len(nodes)
nodeTitles=[]

for node in nodes:
    nodeTitles.append(nodes[node])
nodes=list(nodes)
i=0 #tmp variable for add_node
for node in nodes:
    net_task1_AC3.add_node(node, label=titles[i], title=", ".join(nodeTitles[i]))
    i+=1
for nodeFrom in task1CSP.neighbors.keys():
    for nodeTo in task1CSP.neighbors[nodeFrom]:
        net_task1_AC3.add_edge(nodeFrom, nodeTo, size=sizes)
net_task1_AC3.show("Task1GraphAC3.html", notebook=False)