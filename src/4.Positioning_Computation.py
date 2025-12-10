#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 15:30:52 2024

@author: filippooberto
"""
import json
from graph_tool.all import Graph, sfdp_layout

# Percorsi dei file
input_file = 'graph-data.json'
output_file = 'graph-data-with-positions.json'

# Carica il file JSON
with open(input_file, 'r') as f:
    data = json.load(f)

# Separa nodi e archi
nodes = [item for item in data if 'data' in item and 'id' in item['data']]  # Nodi
edges = [item for item in data if 'data' in item and 'source' in item['data']]  # Archi

# Crea il grafo in graph-tool
g = Graph(directed=False)

# Mappa per associare ogni nodo al suo corrispondente nel grafo
node_map = {}
node_positions = {}

# Aggiungi i nodi al grafo
for node in nodes:
    v = g.add_vertex()
    node_id = node['data']['id']
    node_map[node_id] = v

# Aggiungi gli archi al grafo
for edge in edges:
    source_id = edge['data']['source']
    target_id = edge['data']['target']
    g.add_edge(node_map[source_id], node_map[target_id])

# Calcola le posizioni dei nodi usando SFDP layout
pos = sfdp_layout(g, cooling_step=0.95, epsilon=1e-3, max_iter=10000)  # Puoi modificare questi parametri

# Aggiungi le posizioni ai nodi
for node in nodes:
    node_id = node['data']['id']
    node_pos = pos[node_map[node_id]]
    node['position'] = {'x': float(node_pos[0]), 'y': float(node_pos[1])}

# Salva il file JSON con le posizioni
with open(output_file, 'w') as f:
    json.dump(nodes + edges, f, indent=2)

print(f"Posizioni calcolate e salvate in {output_file}")
