import argparse
import csv

targets = ['BRD4', 'HSA', 'sEH']

def consolidate(filename):
    output = "consolidated_" + filename
    with open(filename) as f, open(output, 'w') as out:
        csv_reader = csv.reader(f)
        csv_writer = csv.writer(out)
        data = {}
        row = next(csv_reader)
        while row:
            row_id = int(row[0])
            smiles = row[1:-2]
            category = 0
            multiplier = 1
            for i in range(3):
                if row[1:-2] != smiles:
                    raise Exception("Different smiles at line ", cvs_reader.line_num, " in ", filename)
                target = row[-2]
                if target != targets[i]:
                    raise Exception(f"Unknown target ", target, " at line ", cvs_reader.line_num, " in ", filename)
                active = int(row[-1])
                category += active * multiplier
                multiplier *= 2
                if active < 0 or active > 1:
                    raise Exception(f"Unknown activity ", active, " at line ", cvs_reader.line_num, " in ", filename)
                data[target] = active
                try:
                    row = next(csv_reader)
                except StopIteration:
                    row = None
            csv_writer.writerow([row_id] + smiles + [category])
            data.clear()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Consolidate data')
    parser.add_argument(dest='filename', nargs='+', type=str, help='Input data')
    args = parser.parse_args()
    for filename in args.filename:
            consolidate(filename)
