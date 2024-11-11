from fastapi import APIRouter, HTTPException, Query
import pandas as pd

from app.api.schemas import SearchQuery

data = pd.read_csv("C:\goal\\table-parser\\test_table.csv")
data.fillna("Неизвестно", inplace=True)
data.columns = data.columns.str.replace(" ", "_")
data.columns = data.columns.str.replace("-", "_")

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
    responses={404: {"description": "Not found"}},
)


def determine_column_type(column):
    unique_values = column.nunique()
    total_values = len(column)
    dtype = str(column.dtype)

    if pd.api.types.is_numeric_dtype(column):
        return "int" if pd.api.types.is_integer_dtype(column) else "float"
    elif unique_values / total_values < 0.2:  # Если менее 20% уникальных значений
        return "ENUM"
    else:
        return "string"


@router.get("/columns")
def get_columns():
    columns_info = {col: determine_column_type(data[col]) for col in data.columns}
    return columns_info


@router.get("/column/{column_name}")
def get_column_data(
    column_name: str,
    unique: bool = Query(False, description="Получить только уникальные значения"),
):

    if column_name not in data.columns:
        raise HTTPException(status_code=404, detail="Column not found")

    column_data = (
        data[column_name].unique().tolist() if unique else data[column_name].tolist()
    )
    return column_data


# Наименование: Набор 4 банана 6-8 ягод
# Город: Ижевск


@router.post("/search/")
def search(query: SearchQuery):
    filtered_data = data.copy()

    if query.Наименование:
        filtered_data = filtered_data[
            filtered_data["Наименование"].str.contains(
                query.Наименование, case=False, na=False
            )
        ]
    if query.Город:
        filtered_data = filtered_data[
            filtered_data["Город"].str.contains(query.Город, case=False, na=False)
        ]
    if query.Категория:
        filtered_data = filtered_data[
            filtered_data["Категория"].str.contains(
                query.Категория, case=False, na=False
            )
        ]
    if query.Для_кого:
        filtered_data = filtered_data[
            filtered_data["Для_кого"].str.contains(query.Для_кого, case=False, na=False)
        ]
    if query.Размер_упаковки:
        filtered_data = filtered_data[
            filtered_data["Размер_упаковки"].str.contains(
                query.Размер_упаковки, case=False, na=False
            )
        ]
    if query.Шоколад:
        filtered_data = filtered_data[
            filtered_data["Шоколад"].str.contains(query.Шоколад, case=False, na=False)
        ]
    if query.Наполнение_набора:
        filtered_data = filtered_data[
            filtered_data["Наполнение_набора"].str.contains(
                query.Наполнение_набора, case=False, na=False
            )
        ]
    if query.Ссылка:
        filtered_data = filtered_data[
            filtered_data["Ссылка"].str.contains(query.Ссылка, case=False, na=False)
        ]

    if query.Стоимость is not None:
        filtered_data = filtered_data[filtered_data["Стоимость"] == query.Стоимость]
    if query.Кол_во_ягод is not None:
        filtered_data = filtered_data[filtered_data["Кол_во_ягод"] == query.Кол_во_ягод]

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="No matching records found")

    result = filtered_data.to_dict(orient="records")
    return result
