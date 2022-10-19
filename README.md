# Gene-Graph Neural Network for Cancer Cell Line Drug Response Prediction
Clemens Woest

## Introduction
This repository contains the process and the final code for my master thesis.

## Installation
- [ ] TODO
```bash
conda create ...
conda activate ...
pip install ...
```

## Contents
### Notebooks

| Notebook | Content |
| -------- | ------- |
| `02_GDSC_map_GenExpr.ipynb` | Contains the code for the creation of the base dataset containing gene expressions for cell-line drug combinations. |
| `03_GDSC_map_CNV.ipynb` | Contains the code for the creation of the base dataset containing gistic and picnic copy numbers for cell-line drug combinations. |
| `04_GDSC_map_mutations.ipynb` | |
| `05_DrugFeatures.ipynb` | |
| `06_create_base_dataset.ipynb` | |
| `07_Linking.ipynb` | Contains the code for the creation of the graph using the STRING database. |
| `07_v1_2_get_linking_dataset.ipynb` | Creates the graph per cell-line with all 4 node features (gene expr, cnv gistic, cnv picnic and mutation). | 