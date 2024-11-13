from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Union
from app.api.dependencies import get_columns_info
from app.api.google_sheet_auth import get_google_sheets_client, fetch_sheet_data
import pandas as pd
from app.settings import SETTINGS

client = get_google_sheets_client(SETTINGS.CREDENTIALS_FILE)
router = APIRouter(
    prefix="/parser", tags=["parser"], responses={404: {"description": "Not found"}}
)


@router.get("/columns")
async def get_columns():
    """
    Эндпоинт для получения информации о всех столбцах в таблице.
    Загружает данные из Google Sheets и возвращает информацию по каждому столбцу.
    """
    data = await fetch_sheet_data(client, SETTINGS.SPREADSHEET_ID)
    columns_info = get_columns_info(data)
    return columns_info


@router.get("/column/{column_name}")
async def get_column_data(
    column_name: str,
    unique: bool = Query(False, description="Получить только уникальные значения"),
):
    """
    Эндпоинт для получения данных из конкретного столбца по его названию.

    Параметры:
    - column_name (str): Название столбца, данные которого нужно получить.
    - unique (bool): Если True, возвращаются только уникальные значения столбца.

    Возвращает данные указанного столбца или выбрасывает ошибку 404, если столбец не найден.
    """
    data = await fetch_sheet_data(client, SETTINGS.SPREADSHEET_ID)
    df = pd.DataFrame(data)

    if column_name not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")

    column_data = (
        df[column_name].unique().tolist() if unique else df[column_name].tolist()
    )
    return column_data


@router.post("/search")
async def search_data(query: Dict[str, Union[str, int, float]]):
    """
    Эндпоинт для поиска данных по заданным критериям.

    Параметры:
    - query: Словарь, где ключ — название столбца,
      а значение — искомое значение. Поддерживается частичный поиск по строке.

    Возвращает записи, соответствующие условиям поиска.
    """
    data = await fetch_sheet_data(client, SETTINGS.SPREADSHEET_ID)

    df = pd.DataFrame(data)

    for key, value in query.items():

        if key == "Стоимость" and "-" in value:
            value = value.split("-")

            cost_from, cost_to = value[0], value[1]

            if cost_from == "":
                cost_from = 0
            elif cost_to == "":
                cost_to = 10000000

            cost_to = int(cost_to)
            cost_from = int(cost_from)

            if cost_from > cost_to:
                raise HTTPException(
                    status_code=400, detail="Cost from must be less than cost to"
                )
            df = df[(df["Стоимость"] >= cost_from) & (df["Стоимость"] <= cost_to)]

        elif isinstance(value, int) or isinstance(value, float):
            df = df[df[key] == value]
        else:
            df = df[df[key].astype(str).str.contains(value, case=False, na=False)]

    return df.to_dict(orient="records")
