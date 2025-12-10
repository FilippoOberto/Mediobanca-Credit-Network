#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:43:28 2024

@author: filippooberto
"""

import pandas as pd
import ast
import re

# Carica il file CSV
df = pd.read_csv('2024_10_14_CREDITI_GRAFO_FINALE.csv', delimiter=';', encoding='latin1')

# Funzione per normalizzare le entità
def normalize_entities(cell):
    if isinstance(cell, str):
        # Rimuovi le barre inverse davanti agli apostrofi
        cell = cell.replace(r"\'", "'")
        # Sostituisci le virgolette quadruple o doppie con virgolette singole
        cell = re.sub(r'"+', "'", cell)
        # Se possibile, converte le stringhe rappresentative delle entità in strutture dati
        try:
            cell = ast.literal_eval(cell)
        except (ValueError, SyntaxError):
            pass  # Ignora le celle che non contengono strutture dati
    return cell

# Applica la funzione di normalizzazione alle colonne che contengono entità
df['Utilizzo_entities'] = df['Utilizzo_entities'].apply(normalize_entities)
df['Garanzie_entities'] = df['Garanzie_entities'].apply(normalize_entities)
df['Soci_entities'] = df['Soci_entities'].apply(normalize_entities)
df['Attività_entities'] = df['Attività_entities'].apply(normalize_entities)
df['Scopo_entities'] = df['Scopo_entities'].apply(normalize_entities)

# Salva il CSV normalizzato
df.to_csv('file_normalizzato.csv', index=False, sep=';')
