import argparse
import xgboost

from leash_BELKA.DataIterator import DataIterator
#from leash_BELKA.TrainedModel import TrainedModel
#from leash_BELKA.TrainingData import TrainingData


def train() -> None:
    parser = argparse.ArgumentParser(description='Commandline tool for training for Leash BELKA kaggle competition.')
    parser.add_argument('input', type=str, nargs='+', help='full path to the csv files containing the training data.')
    parser.add_argument('-o', '--output', type=str, required=True, help='full path to the trained model (json or ubj).')
    args = parser.parse_args()
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

