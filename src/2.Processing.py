#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:48:10 2024

@author: filippooberto
"""

import re
import pandas as pd

# Funzione per elaborare le stringhe nel formato richiesto
def process_entities(entities_string):
    # Verifica se l'input è una stringa e controlla se è la stringa '[]'
    if not isinstance(entities_string, str):
        return entities_string
    
    # Se la cella contiene '[]', restituisci una stringa vuota
    if entities_string.strip() == '[]':
        return ''
    
    # Step 1: Sostituisci le virgole tra le tuple con ' | ' (prima sostituzione)
    step1 = re.sub(r"\),\s*\(", r") | (", entities_string)
    
    # Step 2: Elimina le parentesi quadre che contengono le tuple
    # Consideriamo solo i casi di parentesi di apertura di tuple
    step2 = re.sub(r'^\[|\]$', '', step1)
    
    # Step 3: Elimina le parentesi tonde che isolano le tuple ma mantieni quelle interne ai nomi
    step3 = re.sub(r"\(\s*'([^']+?)',\s*'[^']+?'\s*\)", r"\1", step2)
    
    # Step 4: Elimina le etichette (ovvero, rimuovi il secondo elemento della tupla, insieme alla virgola che lo separa)
    step4 = re.sub(r",\s*'[^']+'", '', step3)
    
    # Step 5: Elimina solo le virgolette singole che non fanno parte di un apostrofo
    # Usando un pattern che eviti di toccare gli apostrofi
    step5 = re.sub(r"(?<!\w)'(?!\w)", '', step4)
    
    return step5

# Carica il file CSV
df = pd.read_csv('file_normalizzato.csv', sep=';', encoding='latin1')

# Applica la funzione solo alle colonne che terminano con '_entities'
for col in df.columns:
    if col.endswith('_entities'):
        df[col] = df[col].apply(process_entities)
        
df = df.apply(lambda x: x.str.encode('latin1').str.decode('utf-8') if x.dtype == "object" else x)
df.columns = [col.encode('latin1').decode('utf-8') for col in df.columns]

# Salva il risultato nel CSV
df.to_csv('file_processed.csv', index=False, encoding='utf-8')

print("Processing complete.")
