# Gene-Interaction Graph Neural Network to Predict Cancer Drug Response

## Introduction
This repository contains the process and the final code for my master thesis.

## Installation

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

### Todos 

- [x] fix error with mutations dataset 
- [x] include mutation features in tensor
- [x] build bi-modal network structure and build simple NN
  - [ ] TO FIX: For now I included only the features separately. And for each feature it performs nearly equally. Why is that? Doesn't it learn anything? However, it's still better then for example just predicting the mean. 

__Networks__:

- [ ] 1. Build baseline using e.g. random forest or simple regression
- [ ] 2. `Tab-Tab`: Build normal FFNN using tabular data for the drugs and for the cell-lines _(references: [MOLI-2019](https://academic.oup.com/bioinformatics/article/35/14/i501/5529255) ([code](https://github.com/hosseinshn/MOLI)))_
- [ ] 3. `Graph-Tab`: Replace the cell-line branch with a GNN, while keeping the drug branch with tabular data _(references: [GraphGCN-2021]([file:///Users/cwoest/Downloads/mathematics-09-00772%20(7).pdf](https://www.mdpi.com/2227-7390/9/7/772/htm)) ([code](https://github.com/BML-cbnu/DrugGCN)))_
- [ ] 4. `Tab-Graph`: Leave the cell-line branch using tabular data, while replacing the drug branch with a GNN _(references: [DrugDRP-2022](https://pubmed.ncbi.nlm.nih.gov/33606633/) ([code](https://github.com/hauldhut/GraphDRP)))_
- [ ] 5. `Graph-Graph`: Replace both the cell-line branch and the drug branch with GNNs _(references: [TGSA-2022](https://academic.oup.com/bioinformatics/article/38/2/461/6374919) ([code](https://github.com/violet-sto/TGSA)))_
- [ ] 6. Implement [`GNNExplainer-2019`](https://arxiv.org/abs/1903.03894) ([code](https://github.com/RexYing/gnn-model-explainer)) on the above network methods
  - [ ] Run on `Tab-Tab`
  - [ ] Run on `Graph-Tab`
  - [ ] Run on `Tab-Graph`
  - [ ] Run on `Graph-Graph`