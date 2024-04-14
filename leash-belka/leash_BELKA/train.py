import argparse
import xgboost

from leash_BELKA.DataIterator import DataIterator
#from leash_BELKA.TrainedModel import TrainedModel
#from leash_BELKA.TrainingData import TrainingData


def train() -> None:
    parser = argparse.ArgumentParser(description='Commandline tool for training for Leash BELKA kaggle competition.')
    parser.add_argument('input', type=str, nargs='+', help='full path to the csv files containing the training data.')
    parser.add_argument('-o', '--output', type=str, required=True, help='full path to the trained model (json or ubj).')
    parser.add_argument('-b', '--booster', choices=['lightgbm', 'catboost', 'xgboost'], default='xgboost', help='booster to use for training. Default is xgboost.')
    args = parser.parse_args()
    if args.booster == 'xgboost':
        train_xgboost(args)
    elif args.booster == 'catboost':
        train_catboost(args)
    elif args.booster == 'lightgbm':
        train_lightgbm(args)
    else:
        raise ValueError('Invalid booster: ' + args.booster + '. Expected catboost or xgboost.')

def train_lightgbm(args: argparse.Namespace) -> None:
    import lightgbm as lgb
    from sklearn import datasets
    iris = datasets.load_iris()
    digits = datasets.load_digits()
    pass

def train_catboost(args: argparse.Namespace) -> None:
    import catboost
    from catboost import datasets
    from catboost import CatBoostClassifier
    import sklearn
    train_df, test_df = datasets.amazon() # nice datasets with categorical features only :D
    train_df.shape, test_df.shape
    y = train_df['ACTION']
    X = train_df.drop(columns='ACTION') # or X = train_df.drop('ACTION', axis=1)
    X_test = test_df.drop(columns='id')
    SEED = 1
    from sklearn.model_selection import train_test_split
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.25, random_state=SEED)
    params = {'loss_function':'Logloss', # objective function
          'eval_metric':'AUC', # metric
          'verbose': 200, # output to stdout info about training process every 200 iterations
          'random_seed': SEED
         }
    cbc_1 = CatBoostClassifier(**params)
    cbc_1.fit(X_train, y_train, # data to train on (required parameters, unless we provide X as a pool object, will be shown below)
          eval_set=(X_valid, y_valid), # data to validate on
          use_best_model=True, # True if we don't want to save trees created after iteration with the best validation score
          plot=False # True for visualization of the training process (it is not shown in a published kernel - try executing this code)
         );
    cat_features = list(range(X.shape[1]))
    print(cat_features)
    pass

def train_xgboost(args: argparse.Namespace) -> None:
    data_iterator = DataIterator(args.input)
    print ("creating DMatrix")
    Xy = xgboost.DMatrix(data_iterator)
    print ("training")
    booster = xgboost.train({"tree_method": "hist"}, Xy)
    print ("saving model")
    booster.save_model(args.output)
    #with open(args.input) as dataFile:
    #    line = dataFile.readline()
    #    if not line:
    #        raise ValueError('Invalid training data file: ' + args.input + '. Expected a header line. Got nothing.')
    #    header = line.strip().split(',')
    #    expectedHeader = "id,buildingblock1_smiles,buildingblock2_smiles,buildingblock3_smiles,molecule_smiles,protein_name,binds".split(',')
    #    if header != expectedHeader:
    #        raise ValueError('Invalid training data file: ' + args.input + '. Expected header: ' + ','.join(expectedHeader) + '. Got: ' + ','.join(header))
    #    count = 0
    #    while line := dataFile.readline():
    #        data = line.strip().split(',')
    #        if len(data) != len(header):
    #            raise ValueError('Invalid training data file: ' + args.input + '. Expected ' + str(len(header)) + ' columns. Got: ' + str(len(data)))
    #        protein_name = data[5]
    #        if trainingData.targets and protein_name not in trainingData.targets:
    #            continue
    #        #data_id = data[0]
    #        buildingblock1_smiles = data[1]
    #        buildingblock2_smiles = data[2]
    #        buildingblock3_smiles = data[3]
    #        molecule_smiles = data[4]
    #        binds = data[6]
    #        trainingData.add(protein_name, buildingblock1_smiles, buildingblock2_smiles, buildingblock3_smiles, molecule_smiles, binds)
    #        count += 1
    #        if count > 100:
    #            break
    #    trainedModel = TrainedModel(trainingData)
    #    trainedModel.save(args.output)

