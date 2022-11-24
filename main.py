from argparse import ArgumentParser
import random
import numpy as np
import pandas as pd
import pickle
import torch
from config import PATH_SUMMARY_DATASETS
from models.GraphTab.graph_tab import GraphTabDataset, create_datasets, BuildModel, GraphTab_v1
import torch.nn as nn
from sklearn.model_selection import train_test_split

from torch_geometric.loader import DataLoader


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--seed', type=int, default=42, help='random seed (default: 42)')
    parser.add_argument('--batch_size', type=int, default=10, help='the batch size (default: 10)')
    parser.add_argument('--lr', type=int, default=0.0001, help='learning rate (default: 0.0001)')
    parser.add_argument('--train_ratio', type=float, default=0.8, help='training set ratio (default: 0.8)')
    parser.add_argument('--val_ratio', type=float, default=0.5, help='validation set ratio inside the test set (default: 0.5)')
    parser.add_argument('--num_epochs', type=int, default=1, help='number of epochs (default: )')
    parser.add_argument('--num_workers', type=int, default=12, help='number of workers for DataLoader (default: 3)')
    parser.add_argument('--dropout', type=float, default=0.1, help='dropout probability (default: 0.1)')
    parser.add_argument('--model', type=str, default='GraphTab', 
                        help='name of the model to run, options: [`TabTab`, `GraphTab`, `TabGraph`, `GraphGraph`]')

    parser.add_argument('--version', type=str, default='v3', help='model version to run')

    return parser.parse_args()

class HyperParameters:
    def __init__(self, batch_size, lr, train_ratio, val_ratio, num_epochs, seed='12345', num_workers=0):
        self.BATCH_SIZE = batch_size
        self.LR = lr
        self.TRAIN_RATIO = train_ratio
        self.TEST_VAL_RATIO = 1-self.TRAIN_RATIO
        self.VAL_RATIO = val_ratio
        self.NUM_EPOCHS = num_epochs
        self.RANDOM_SEED = seed
        self.NUM_WORKERS = num_workers


def main():
    args = parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    # ------------- #
    # Read datasets #
    # ------------- #
    # TODO: Assert that the given version is a folder and that the file exists
    with open(f'{PATH_SUMMARY_DATASETS}{args.model}/{args.version}/drug_response_matrix__gdsc2.pkl', 'rb') as f: 
        drm = pickle.load(f)
        print(f"Finished reading drug response matrix: {drm.shape}")

    if args.model == 'GraphTab':
        with open(f'{PATH_SUMMARY_DATASETS}{args.model}/{args.version}/cl_graphs_dict.pkl', 'rb') as f:
            cl_graphs = pd.read_pickle(f)
            print(f"Finished reading cell-line graphs: {cl_graphs['22RV1']}")
        with open(f'{PATH_SUMMARY_DATASETS}{args.model}/{args.version}/drug_smiles_fingerprints_matrix.pkl', 'rb') as f:
            drug_name_smiles = pickle.load(f) 
            print(f"Finished reading drug SMILES matrix: {drug_name_smiles.shape}")
            fingerprints_dict = drug_name_smiles.set_index('DRUG_ID').T.to_dict('list')      
    # TODO: add else for other models.
    # TODO: add folder with corresponding datasets for each model type. each folder contains subfolder with dev version


    if args.model == 'GraphTab':
        # Build pytorch dataset.
        graph_tab_dataset = GraphTabDataset(cl_graphs=cl_graphs, drugs=fingerprints_dict, drug_response_matrix=drm)
        print("Finished building GraphTabDataset!")
        graph_tab_dataset.print_dataset_summary() 

        hyper_params = HyperParameters(batch_size=args.batch_size, 
                                      lr=args.lr, 
                                      train_ratio=args.train_ratio, 
                                      val_ratio=args.val_ratio, 
                                      num_epochs=args.num_epochs, 
                                      seed=args.seed,
                                      num_workers=args.num_workers)

        # Create pytorch geometric DataLoader datasets.
        # TODO: make some args as separate input parameters
        train_loader, test_loader, val_loader = create_datasets(drm, cl_graphs, fingerprints_dict, hyper_params)
        print("Finished creating pytorch training datasets!")
        print("Number of batches per dataset:")
        print(f"  train : {len(train_loader)}")
        print(f"  test  : {len(test_loader)}")
        print(f"  val   : {len(val_loader)}")

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"device: {device}")

        model = GraphTab_v1().to(device)
        loss_func = nn.MSELoss()
        optimizer = torch.optim.Adam(params=model.parameters(), lr=args.lr) # TODO: include weight_decay of lr

        # Build the model.
        build_model = BuildModel(model=model,
                                criterion=loss_func,
                                optimizer=optimizer,
                                num_epochs=args.num_epochs,
                                train_loader=train_loader,
                                test_loader=test_loader,
                                val_loader=val_loader, 
                                device=device)

        # Train the model.
        performance_stats = build_model.train(build_model.train_loader)

        # ONLY USE A SAMPLE
        # sample = drm.sample(1_000)
        # train_set, test_val_set = train_test_split(sample, test_size=0.8, random_state=args.seed)
        # sample_dataset = GraphTabDataset(cl_graphs=cl_graphs, drugs=fingerprints_dict, drug_response_matrix=train_set)
        # print("\ntrain_dataset:")
        # sample_dataset.print_dataset_summary()
        # sample_loader = DataLoader(dataset=sample_dataset, batch_size=2, shuffle=True) 
        # performance_stats = build_model.train(sample_loader)
    elif args.model == 'TabGraph':
        dataset = TabGraphDataset()
    elif args.model == 'TabTab':
        dataset = TabTabDataset()


    torch.save({
        'epoch': args.num_epochs, # TODO: add here current epoch. For that the epochs must run in the main.
        'batch_size': args.batch_size,
        'learning_rate': args.lr,
        'train_ratio': args.train_ratio,
        'val_ratio': args.val_ratio,
        'model_state_dict': build_model.model.state_dict(),
        'optimizer_state_dict': build_model.optimizer.state_dict(),
        'train_performances': performance_stats['train'],
        'val_performances': performance_stats['val']
    }, f'{PATH_SUMMARY_DATASETS}{args.model}/{args.version}/model_performance.pth')


if __name__ == "__main__":
    main()        
