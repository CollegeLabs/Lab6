# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code

import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object

from src.CSPclass import *
from src.algorithms import *
from src.agents import *
from src.utils import *

nodeColors={
    "empty":"white",
    "filled": "yellow"
}

#commit



'''
def main():
    if "clicked" not in st.session_state:
        st.session_state["clicked"] = False
        
    if not st.session_state["clicked"]:
        #Set header title
        st.header("CSP: Simple Sudoku Example")
        st.header("_Initial Sudoku._", divider=True)
        
        sudokuNeighbors,sudokuDomains,sudokuConstraints1=getSudokuData()        
        basicSudokuCSP=CSP(variables=sudokuNeighbors.keys(),neighbors=sudokuNeighbors, domains=sudokuDomains, constraints=sudokuConstraints1)

        buildGraph(basicSudokuCSP, nodeColors)
        
    if st.button("Run AC-3"):
        AC3(basicSudokuCSP)
        buildGraph(basicSudokuCSP, nodeColors, True)

        if st.button("Run Backtrack Search"):
            backtracking_search(basicSudokuCSP)
            buildGraph(basicSudokuCSP, nodeColors, False)
            
        
        #st.button("Run AC-3", on_click= , args= [option])
'''
def main():
    st.header("CSP: Simple Sudoku Example")
    st.header("_Initial Sudoku._", divider=True)

    # Initialize CSP once
    if "csp" not in st.session_state:
        sudokuNeighbors, sudokuDomains, sudokuConstraints1 = getSudokuData()
        st.session_state.csp = CSP(
            variables=sudokuNeighbors.keys(),
            neighbors=sudokuNeighbors,
            domains=sudokuDomains,
            constraints=sudokuConstraints1
        )
        st.session_state.ac3_done = False
        buildGraph(st.session_state.csp, nodeColors)

    if st.button("Run AC-3", key="btn_ac3"):
        AC3(st.session_state.csp)
        buildGraph(st.session_state.csp, nodeColors, True)
        st.session_state["ac3_done"] = True

    if st.session_state.get("ac3_done") and st.button("Run Backtrack Search", key="btn_bt"):
        result = backtracking_search(st.session_state.csp)

        for var, val in result.items():
            st.session_state.csp.domains[var] = [val]
            st.session_state.csp.curr_domains[var] = [val]

        buildGraph(st.session_state.csp, nodeColors, False)
        
         

        
def getSudokuData():
    var1=list("ABCDEFGHI")
    var2=range(1,10)
    filled = {
    'A2': 1, 'A8': 6,
    'B1': 3, 'B3': 9, 'B7': 1, 'B9': 5,
    'C2': 8, 'C4': 3, 'C6': 5, 'C8': 7,
    'D3': 2, 'D5': 7, 'D7': 8,
    'E4': 6, 'E6': 8,
    'F3': 8, 'F5': 9, 'F7': 2,
    'G2': 2, 'G4': 4, 'G6': 1, 'G8': 9,
    'H1': 9, 'H3': 4, 'H7': 6, 'H9': 1,
    'I2': 3, 'I8': 8
    }

    vars=set()

    for letter in var1:
        for number in var2:
            vars.add(letter+str(number))

    sudokuNeighbors={}

    for letter in var1:
        for number in var2:
            sudokuNeighbors[letter+str(number)]=[]

    row_groups = [
        ['A', 'B', 'C'], # top
        ['D', 'E', 'F'], # middle
        ['G', 'H', 'I']  # bottom
    ]

    col_groups = [
        ['1', '2', '3'], # left
        ['4', '5', '6'], # middle
        ['7', '8', '9']  # right
    ]

    asterisk_group = [
        ['B5','C3','C7',
         'E2','E5','E8',
         'G3','G7','H5']
    ]

    for key1 in sudokuNeighbors.keys():
        for key2 in sudokuNeighbors.keys():
            if key1 != key2:
                if key1[0] == key2[0]:
                    if key2 not in sudokuNeighbors[key1]:
                        sudokuNeighbors[key1].append(key2) 
                if key1[1] == key2[1]:
                    if key2 not in sudokuNeighbors[key1]:
                        sudokuNeighbors[key1].append(key2)
                for row in row_groups:
                    if key1[0] in row and key2[0] in row:
                        for col in col_groups:
                            if key1[1] in col and key2[1] in col:
                                if key2 not in sudokuNeighbors[key1]:
                                    sudokuNeighbors[key1].append(key2)
                for asterisk in asterisk_group:
                    if key1 in asterisk and key2 in asterisk:
                        if key2 not in sudokuNeighbors[key1]:
                            sudokuNeighbors[key1].append(key2)
            
    sudokuDomains={var:[filled[var]] if var in filled else [ch for ch in range(1,10)] for var in sudokuNeighbors.keys()}
    sudokuConstraints1 = lambda X, x, Y, y: x!=y
    
    return sudokuNeighbors,sudokuDomains,sudokuConstraints1

        
        
        
def buildGraph(SudokuCSP, nodeColors, ac3=False):
    netSudoku= Network(
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%"
                ) 
    
    netSudoku.toggle_physics(False)
    
    nodeColorsDict={}
    nodeTitlesDict={}
    nodeLabelsDict={}
    nodes=list(SudokuCSP.variables)

    for node in nodes:
        if ac3:
            if len(SudokuCSP.curr_domains[node])==1:
                nodeColorsDict.setdefault(node,nodeColors["filled"])
                nodeTitlesDict.setdefault(node,str(SudokuCSP.curr_domains[node][0]))
                nodeLabelsDict.setdefault(node,str(SudokuCSP.curr_domains[node][0]))
        if len(SudokuCSP.domains[node])==1:
            nodeColorsDict.setdefault(node,nodeColors["filled"])
            if ac3:
                nodeTitlesDict.setdefault(node,str(SudokuCSP.curr_domains[node][0]))
            else:
                nodeTitlesDict.setdefault(node,str(SudokuCSP.domains[node][0]))
            nodeLabelsDict.setdefault(node,str(SudokuCSP.domains[node][0]))           
        else:
            nodeColorsDict.setdefault(node,nodeColors["empty"])
            if ac3:
                string_list = [str(i) for i in SudokuCSP.curr_domains[node]]
               
            else:
                string_list = [str(i) for i in SudokuCSP.domains[node]]
            nodeTitlesDict.setdefault(node, ",".join(string_list) )
                
            nodeLabelsDict.setdefault(node,"")      
           
            
    x_coords = {}
    y_coords = {} 

    for node in nodes:
        if node[0]=="A":
            y_coords.setdefault(node,50)           
        elif node[0]=="B":
            y_coords.setdefault(node,100)
        elif node[0]=="C":
            y_coords.setdefault(node,150)
        elif node[0]=="D":
            y_coords.setdefault(node,200)
        elif node[0]=="E":
            y_coords.setdefault(node,250)
        elif node[0]=="F":
            y_coords.setdefault(node,300)
        elif node[0]=="G":
            y_coords.setdefault(node,350)
        elif node[0]=="H":
            y_coords.setdefault(node,400)
        elif node[0]=="I":
            y_coords.setdefault(node,450)
        x_coords.setdefault(node,int(node[1])*50)
           
            
    
    # initialize graph
    g = nx.Graph()
    
    # add the nodes
    for node in nodes:
        g.add_node(node, color=nodeColorsDict[node], size=10, title=nodeTitlesDict[node], label=nodeLabelsDict[node],  x=x_coords[node],y=y_coords[node])

    # add the edges
    print(SudokuCSP.neighbors)
    
    
    for nodeFrom in SudokuCSP.neighbors.keys():
        for nodeTo in SudokuCSP.neighbors[nodeFrom]:        
            if nodeFrom[0]==nodeTo[0]: # row const-s
                g.add_edge(nodeFrom,nodeTo, color="red")
            elif nodeFrom[1]==nodeTo[1]: # col const-s
                g.add_edge(nodeFrom,nodeTo, color="blue")
            else:
                g.add_edge(nodeFrom,nodeTo, color="green") # diag con-s
            
    print(g.edges)
    # generate the graph
    netSudoku.from_nx(g)
    
    netSudoku.save_graph('L6_SimpleSudoku.html')
    HtmlFile = open(f'L6_SimpleSudoku.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 1200,width=1000)
    
    
    
    
if __name__ == '__main__':
    main()
        