import argparse

from leash_BELKA.TrainingData import TrainingData
from leash_BELKA.TrainedModel import TrainedModel

def train() -> None:
    parser = argparse.ArgumentParser(description='Commandline tool for training for Leash BELKA kaggle competition.')
    parser.add_argument('-i', '--input', type=str, required=True, help='full path to the csv file containing the training data.')
    parser.add_argument('-o', '--output', type=str, required=True, help='full path to the trained model.')
    parser.add_argument('-t', '--targets', type=str, help='list of target names.')
    args = parser.parse_args()
    targets = args.targets.split(',') if args.targets else []
    trainingData = TrainingData(targets)
    with open(args.input) as dataFile:
        line = dataFile.readline()
        if not line:
            raise ValueError('Invalid training data file: ' + args.input + '. Expected a header line. Got nothing.')
        header = line.strip().split(',')
        expectedHeader = "id,buildingblock1_smiles,buildingblock2_smiles,buildingblock3_smiles,molecule_smiles,protein_name,binds".split(',')
        if header != expectedHeader:
            raise ValueError('Invalid training data file: ' + args.input + '. Expected header: ' + ','.join(expectedHeader) + '. Got: ' + ','.join(header))
        count = 0
        while line := dataFile.readline():
            data = line.strip().split(',')
            if len(data) != len(header):
                raise ValueError('Invalid training data file: ' + args.input + '. Expected ' + str(len(header)) + ' columns. Got: ' + str(len(data)))
            protein_name = data[5]
            if trainingData.targets and protein_name not in trainingData.targets:
                continue
            data_id = data[0]
            buildingblock1_smiles = data[1]
            buildingblock2_smiles = data[2]
            buildingblock3_smiles = data[3]
            molecule_smiles = data[4]
            binds = data[6]
            trainingData.add(protein_name, buildingblock1_smiles, buildingblock2_smiles, buildingblock3_smiles, molecule_smiles, binds)
            count += 1
            if count > 100:
                break
        trainedModel = TrainedModel(trainingData)
        trainedModel.save(args.output)

