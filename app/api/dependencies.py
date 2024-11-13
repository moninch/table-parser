import pandas as pd


def determine_column_type(column):
    unique_values = column.nunique()
    total_values = len(column)
    dtype = str(column.dtype)

    if pd.api.types.is_numeric_dtype(column):
        return "int" if pd.api.types.is_integer_dtype(column) else "float"
    elif unique_values / total_values < 0.2:
        options = column.unique().tolist()
        return {"type": "ENUM", "options": options}
    else:
        return "string"


def get_columns_info(data):
    df = pd.DataFrame(data)
    return {col: determine_column_type(df[col]) for col in df.columns}
