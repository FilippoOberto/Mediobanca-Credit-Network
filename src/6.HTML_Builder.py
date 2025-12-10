#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 10:41:09 2024

@author: filippooberto
"""

import json

# File di input e output
json_file_path = "updated-graph-data-with-codes.json"
output_html_file = "grafo_con_posizioni.html"

# Leggi il file JSON
with open(json_file_path, 'r') as f:
    graph_data = json.load(f)

# Converti il JSON in stringa per inserirlo nell'HTML
elements_string = json.dumps(graph_data, indent=4)

# Template HTML
html_template = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <link rel="icon" href="data:,">

<!-- Cytoscape.js -->
	<script src="https://unpkg.com/cytoscape/dist/cytoscape.min.js"></script>
    <script src="https://unpkg.com/layout-base/layout-base.js"></script>
    <script src="https://unpkg.com/cose-base/cose-base.js"></script>
    <script src="https://unpkg.com/cytoscape-fcose/cytoscape-fcose.js"></script>

    <style>
        html, body {
            height: 100%;
            width: 100%;
            padding: 0;
            margin: 0;
            overflow: hidden;
            background: #000000;
            color: white;
        }

        #cy {
            height: 100%;
            width: 100%;
            background-color: #000000;
        }

        #export-positions {
            position: absolute;
            top: 10px;
            left: 10px;
            background-color: #222;
            color: #ddd;
            border: 1px solid #555;
            border-radius: 8px;
            padding: 6px;
            cursor: pointer;
            font-family: Arial, sans-serif;
        }

        #export-positions:hover {
            background-color: #ff6600;
            border-color: #ff6600;
        }
    </style>
</head>
<body>
    <div id="cy"></div>
    <button id="export-positions">Esporta posizioni nodi</button>

    <script>
        const elements = {json_data_placeholder};

        // Inizializzazione di Cytoscape
        const cy = cytoscape({
            container: document.getElementById('cy'),
            elements: elements,
            style: [
                {
                    selector: 'node',
                    style: {
                        'background-color': '#0074d9',
                        'label': 'data(name)',
                        'text-valign': 'center',
                        'color': '#fff',
                        'font-size': '12px',
                        'width': 30,
                        'height': 30
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 2,
                        'line-color': '#ccc',
                        'target-arrow-color': '#ccc',
                        'target-arrow-shape': 'triangle'
                    }
                }
            ],
            layout: {
                name: 'fcose',
                quality: 'proof',
                randomize: false,
                animate: false,
                fit: true,
                padding: 200,
                nodeRepulsion: 150000,  // Usa un valore statico per la repulsione
                idealEdgeLength: 300,  // Lunghezza ideale degli archi
                edgeElasticity: 0.05,   // Elasticità degli archi
                numIter: 10000,
                gravity: 0.05,
                gravityRangeCompound: 3.5,
                gravityCompound: 1.2,
                gravityRange: 5.0,
                tile: false,
                packComponents: true, 
                fixedNodeConstraint: undefined,
                alignmentConstraint: undefined,
                relativePlacementConstraint: undefined,
            },
        });

        // Funzione per esportare le posizioni dei nodi
        document.getElementById('export-positions').addEventListener('click', function() {
        const updatedGraph = JSON.parse(JSON.stringify(elements)); // Clona il JSON originale
    
        // Aggiorna le posizioni dei nodi
        updatedGraph.forEach(element => {
            if (element.data && element.data.id) {
                const node = cy.getElementById(element.data.id);
                if (node.isNode()) {
                    element.position = {
                        x: node.position('x'),
                        y: node.position('y')
                    };
                }
            }
        });
    
        // Serializza il JSON aggiornato
        const json = JSON.stringify(updatedGraph, null, 2);
    
        // Scarica il file JSON
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'updated-graph-data-final.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });

    </script>
</body>
</html>
"""

# Sostituisci il placeholder con i dati JSON
final_html = html_template.replace('{json_data_placeholder}', elements_string)

# Scrivi il file HTML
with open(output_html_file, 'w') as f:
    f.write(final_html)

print(f"File HTML generato con successo: {output_html_file}")
