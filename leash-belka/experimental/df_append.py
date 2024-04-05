"""Append data directly to a DataFrame, one row at a time"""

import timeit

import pandas as pd

input_path = 'data/train.csv'
total = 12000000

def df_append() -> None:
    print("Total rows: ", total)
    # The fastest - just a bit faster than dict
    # with 4GB of memory, does 8M rows in 8s then slows down
    # to 12M in 18s
    print("File  : ", timeit.timeit(with_file, number=1))
    # Concat and loc are quadratic and already 1000x slower than dict
    # when total is 10K
    #print("Concat: ", timeit.timeit(with_concat, number=1))
    #print("Loc   : ", timeit.timeit(with_loc, number=1))
    # Dict is twice as fast as CSV but there is the issue of memory and swapping
    #print("Dict  : ", timeit.timeit(with_dict, number=1))
    #print("CSV   : ", timeit.timeit(with_csv, number=1))

def with_file() -> None:
    with open(input_path) as data_file:
        df = pd.read_csv(data_file, nrows=total)
        print("Rows: ", len(df))

def with_concat() -> None:
    with open(input_path) as data_file:
        line = data_file.readline()
        columns = line.strip().split(',')
        df = pd.DataFrame(columns=columns)
        for line in data_file:
            fields = line.strip().split(',')
            if len(fields) != len(columns):
                raise ValueError('Unexpected number of fields')
            new_row = pd.Series(fields, index=columns)
            # Append data to the DataFrame - append was removed
            # df = df.append(new_row, ignore_index=True)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            if len(df) > total:
                break
        print("Rows: ", len(df))

def with_loc() -> None:
    with open(input_path) as data_file:
        line = data_file.readline()
        columns = line.strip().split(',')
        df = pd.DataFrame(columns=columns)
        for line in data_file:
            fields = line.strip().split(',')
            if len(fields) != len(columns):
                raise ValueError('Unexpected number of fields')
            new_row = pd.Series(fields, index=columns)
            # Append data to the DataFrame - append was removed
            df.loc[len(df)] = new_row
            if len(df) > total:
                break
        print("Rows: ", len(df))

def with_csv() -> None:
    #from io import BytesIO
    from csv import writer
    from io import StringIO
    #output = BytesIO()
    output = StringIO()
    csv_writer = writer(output)
    with open(input_path) as data_file:
        line = data_file.readline()
        columns = line.strip().split(',')
        csv_writer.writerow(columns)
        #df = pd.DataFrame(columns=columns)
        for count, line in enumerate(data_file):
            fields = line.strip().split(',')
            if len(fields) != len(columns):
                raise ValueError('Unexpected number of fields')
            #new_row = pd.Series(fields, index=columns)
            # Append data to the DataFrame - append was removed
            #df.loc[len(df)] = new_row
            csv_writer.writerow(fields)
            if count > total:
                break
    output.seek(0)
    df = pd.read_csv(output)
    print("Rows: ", len(df))

def with_dict() -> None:
    output = {}
    with open(input_path) as data_file:
        line = data_file.readline()
        columns = line.strip().split(',')
        for count, line in enumerate(data_file):
            fields = line.strip().split(',')
            if len(fields) != len(columns):
                raise ValueError('Unexpected number of fields')
            output[count] = fields
            if count > total:
                break
    df = pd.DataFrame.from_dict(output, orient='index', columns=columns)
    print("Rows: ", len(df))

