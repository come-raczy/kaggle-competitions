import argparse
import csv

import rdkit.Chem as Chem
from rdkit.Chem import Descriptors


def generate_descriptors(input_file, output_file, descriptors):
    with open(input_file) as f:
        reader = csv.reader(f)
        with open(output_file, 'w') as o:
            writer = csv.writer(o)
            for row in reader:
                smiles = row[4]
                m = Chem.MolFromSmiles(smiles)
                descriptor_dict = Descriptors.CalcMolDescriptors(m)
                values = list(descriptor_dict.values())
                writer.writerow([row[0]] + values + [row[-1]])

if __name__ == '__main__':
    smiles = "c1ccccc1C(=O)O"
    m = Chem.MolFromSmiles(smiles)
    descriptor_dict = Descriptors.CalcMolDescriptors(m)
    default_descriptors = ','.join(list(descriptor_dict.keys()))
    print("Default descriptors: ", default_descriptors)
    parser = argparse.ArgumentParser(description='Generate descriptors from input file')
    parser.add_argument('filename', nargs='+', type=str, help='Input files')
    parser.add_argument('--prefix', type=str, default="desc01_", help='Output files prefix')
    parser.add_argument('--descriptors', type=str, default=default_descriptors, help='List of descriptors to generate, separated by commas')
    args = parser.parse_args()
    descriptors = args.descriptors.split(',')
    for filename in args.filename:
        generate_descriptors(filename, args.prefix + filename, descriptors)

