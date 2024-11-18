from numpy import float64, int64
import pandas as pd
from fastapi import HTTPException


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


def get_columns_info(df):
    return {col: determine_column_type(df[col]) for col in df.columns}


def validate_data(data):
    df = pd.DataFrame(data)
    for column in df.columns:
        if df[column].dtype == object:
            if df[column].isnull().any():
                raise HTTPException(
                    status_code=400,
                    detail=f"Столбец '{column}' содержит пустые значения",
                )

            if df[column].astype(str).str.contains(r"^\d+$").any():
                raise HTTPException(
                    status_code=400,
                    detail=f"Столбец '{column}' содержит целочисленные значения",
                )

    if df["Стоимость"].min() < 0:
        raise HTTPException(
            status_code=400,
            detail=f"Столбец 'Стоимость' содержит значения вне диапазона(<0)",
        )

    df["Для кого"] = df["Для кого"].replace("", "Взрослый")
    return df
