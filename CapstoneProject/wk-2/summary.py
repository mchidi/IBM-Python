import pandas as pd


def table_summary(data_frame: pd.DataFrame, only_missing_data=False):

    data_types = []
    for col in data_frame.columns:
        data_types.append(data_frame[col].dtypes)

    data_frame = data_frame.isnull()

    table = pd.DataFrame(
        columns=['Columns', 'Data_type', "Missing_data", "Available_data", "Total"])
    table = table.loc[:0]

    record = []
    missing_value = 0
    available = 0

    for i, column in enumerate(data_frame.columns.values.tolist()):
        type = data_types[i]
        for row in data_frame[column]:
            if row == True:
                missing_value += 1
            else:
                available += 1

        record.append(column)
        record.append(type)
        record.append(missing_value)
        record.append(available)
        record.append(missing_value + available)

        table.loc[len(table)] = record

        # reset
        missing_value = 0
        available = 0
        record = []
        type = ""

    if only_missing_data:
        return table[table['Missing_data'] > 0]
    else:
        return table


def getOutlier(data: pd.DataFrame, col: str):
    Q1 = data.describe().loc['25%', col]
    Q3 = data.describe().loc['75%', col]
    IQR = Q3 - Q1

    higher_outlier = Q3 + (1.5 * IQR)
    lower_outlier = Q1 - (1.5 * IQR)

    return (higher_outlier, lower_outlier, IQR)
