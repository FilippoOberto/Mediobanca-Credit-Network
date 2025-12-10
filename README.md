# Mediobanca Credit Network: From Archival Data to Interactive Graphs

This repository contains the full data-processing pipeline and reference dataset used to construct an interactive credit network derived from Mediobanca’s historical internal documentation.  
The project transforms raw archival credit records into a structured graph model, computes network positions, and exports outputs ready for interactive visualisation (e.g. via Cytoscape.js) and integration into archival discovery systems.

---

## Overview

The workflow is organised into modular Python scripts that:

1. **Clean and normalise** the raw CSV dataset.  
2. **Extract and restructure** entities and relationships.  
3. **Generate graph nodes and edges** with appropriate attributes.  
4. **Compute spatial layouts** for reproducible visualisation.  
5. **Export JSON artefacts** for interactive graph platforms and archival systems.  
6. **Optionally generate a standalone HTML visualisation** using Cytoscape.js.

This repository accompanies the research project on **post-war Italian capitalism and Mediobanca’s corporate ecosystem**, illustrating how credit relationships found in archival documents can be modelled as a network.

---

## Repository Structure
data/
  raw/
    2024_10_14_CREDITI_GRAFO_FINALE.csv      # Original dataset
  intermediate/
    file_normalizzato.csv                     # Normalised version
    file_processed.csv                        # Processed dataset
  processed/
    graph-data-with-positions.json            # Final layout-ready graph

src/
  1.Normalizzazione_Formattazione.py
  2.Processing.py
  3.Elements_Generator.py
  4.Positioning_Computation.py
  5.Json_XDAMS.py
  6.HTML_Builder.py
  SVILUPPO-Endgame-No-Live-Server.py

docs/
  Grafo_Endgame.html
  Endgame_NoLiveServer.html

README.md

## Script Descriptions

### 1. Normalizzazione e Formattazione (`1.Normalizzazione_Formattazione.py`)
Cleans and normalises the raw CSV:
- standardises problematic quotation marks and separators;
- removes escape characters;
- parses entity fields into Python-readable structures.  
**Output:** `data/intermediate/file_normalizzato.csv`.

### 2. Processing (`2.Processing.py`)
Reformats the normalised file:
- restructures multi-entity fields;
- isolates relationship-relevant information;
- handles malformed or missing entries robustly.  
**Output:** `data/intermediate/file_processed.csv`.

### 3. Elements Generator (`3.Elements_Generator.py`)
Builds the graph’s fundamental components:
- node objects with labels, categories, metadata;
- edge objects representing credit relationships or co-occurrences;
- prepares data structures for layout algorithms and JSON export.

### 4. Positioning Computation (`4.Positioning_Computation.py`)
Computes node positions via force-directed (or comparable) layout:
- attaches 2D coordinates to every node;
- produces a deterministic graph layout reusable across visualisations.  
**Output:** `data/processed/graph-data-with-positions.json`.

### 5. JSON for XDAMS (`5.Json_XDAMS.py`)
Constructs JSON structures compatible with the XDAMS archival platform:
- maps nodes to archival identifiers;
- arranges the dataset according to XDAMS schema specifications.

### 6. HTML Builder (`6.HTML_Builder.py`)
Generates a standalone HTML page with Cytoscape.js:
- imports the final JSON graph;
- configures styles, preset layout, and interactive tools;
- enables node info panels and links to archival items.

### Development Script (`SVILUPPO-Endgame-No-Live-Server.py`)
A utility script for local testing of the entire workflow.  
Not required for replication, but illustrates how components fit together.

## Acknowledgements
This work forms part of an ongoing research programme on digital methods and network analysis applied to banking and corporate archives.  
We would like to acknowledge the invaluable support of the research team and the archival staff of the *Archivio Storico Vincenzo Maranghi* of Mediobanca, whose dedication to the curation and interpretation of historical records has enabled this study.

