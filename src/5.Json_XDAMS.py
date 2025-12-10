#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 09:57:36 2024

@author: filippooberto
"""

import json
import pandas as pd

# File di input
json_file = "graph-data-with-positions.json"
csv_file = "exportCSV_Auth-EACCPF_Mediobanca.csv"

# Leggi il file JSON
with open(json_file, "r", encoding="utf-8") as f:
    graph_data = json.load(f)

# Leggi il file CSV
csv_data = pd.read_csv(csv_file, sep=';', encoding="ISO-8859-1")  

# Normalizza i nomi per evitare problemi di maiuscole/minuscole o spazi
csv_data['forma_autorizzata'] = csv_data['forma_autorizzata'].str.strip().str.lower()
csv_data['codice'] = csv_data['codice'].astype(str)

# Aggiungi il campo "codice" al JSON
for node in graph_data:
    if "data" in node and "name" in node["data"]:
        name = node["data"]["name"].strip().lower()  # Normalizza il nome del nodo
        matching_row = csv_data[csv_data["forma_autorizzata"] == name]  # Trova corrispondenze
        if not matching_row.empty:
            node["data"]["codice"] = matching_row.iloc[0]["codice"]  # Aggiungi il codice

# Salva il file JSON aggiornato
output_file = "updated-graph-data-with-codes.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=4)

print(f"File JSON aggiornato salvato come: {output_file}")
