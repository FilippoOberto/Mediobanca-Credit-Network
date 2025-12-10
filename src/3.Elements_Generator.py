#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:45:16 2024

@author: filippooberto
"""

import json
import pandas as pd
import networkx as nx

#Funzione per sdoppiare le righe che hanno più di un authority separato da #
def split_authoriy_rows(df, col):
    new_rows = []
    
    for index, row in df.iterrows():
        authorities = str(row[col]).split('#')
        for authority in authorities:
            new_row = row.copy()
            new_row[col] = authority.strip()
            new_rows.append(new_row)
            
    return pd.DataFrame(new_rows)

#Funzione per verificare se un nodo è valido
def is_valid_node(name):
    if not name or not name.strip():
        return False
    if all(char in ",.!?;:,(,),[,]" for char in name):
        return False
    return True

#Funzione per pulire le tuple, eliminando il secondo membro
def clean_tuple_data(cell):
    if isinstance(cell, str):
        # Dividi le entità separate da '|'
        entities = [entity.strip() for entity in cell.split('|')]
        # Rimuove parentesi e apostrofi iniziali/finali, mantenendo quelli interni
        cleaned_entities = []
        for entity in entities:
            # Rimuove le parentesi, se presenti
            if entity.startswith("(") and entity.endswith(")"):
                entity = entity.strip("()").strip()
            # Rimuove solo gli apostrofi all'inizio o alla fine
            entity = entity.lstrip("'").rstrip("'")
            cleaned_entities.append(entity)
        return cleaned_entities
    return []

#Carica il file CSV
file_path = 'file_processed.csv'
data = pd.read_csv(file_path, sep=',')

data = split_authoriy_rows(data, 'authority')

#Inizializza dizionari per nodi e archi
nodi = dict()
archi = dict()

#Colonne da cui estrarre entità
cols = ['Utilizzo_entities', 'Garanzie_entities', 'Soci_entities', 'Attività_entities', 'Scopo_entities']

for col in cols:
    data[col] = data[col].apply(lambda x: clean_tuple_data(x) if pd.notna(x) else x)

#Processa i dati per generare nodi e archi
for d in data.to_dict(orient='records'):
    authority = d['authority']
    
    #Verifica se il nodo è valido
    if not is_valid_node(authority):
        continue
    
    if authority not in nodi:
        nodi[authority] = len(nodi)
        
    for c in cols:
        entities = d[c]  # Utilizza la lista di entità
        if isinstance(entities, (list, pd.Series)) and len(entities) > 0:  # Verifica che sia una lista o Series e non sia vuota
            for i in entities:
                if not is_valid_node(i):
                    continue  # Salta se il nodo collegato è vuoto o non valido
                if i not in nodi:
                    nodi[i] = len(nodi)
                x, y = nodi[authority], nodi[i]
                if f'{x}_{y}' not in archi:
                    archi[f'{x}_{y}'] = {'source' : x, 'target' : y, 'type': c, 'weight' : 1}
                else:
                    archi[f'{x}_{y}']['weight'] += 1
                   
#Crea il grafo da pandas edgelist
G = nx.from_pandas_edgelist(pd.DataFrame(archi).T)

#Aggiunge nodi non collegati
for i in range(max(nodi.values())+1):
    if i not in G.nodes:
        G.add_node(i)
        
#Rimuove eventuali archi con self_loop
G.remove_edges_from(nx.selfloop_edges(G))

#Prepara i dati in formato JSON per nodi e archi
archi = [{'data': i} for i in list(archi.values())]
nodi = [{'data': {'id': nodi[i], 'name': i}} for i in nodi if is_valid_node(i)]

#Combina nodi e archi in un unico formato
graph_data = nodi + archi

#Salva i dati in formato JSON
output_path = 'graph-data.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(graph_data, json_file, ensure_ascii=False, indent=4)
    
print(f'File JSON salvato in {output_path}')

        
     

