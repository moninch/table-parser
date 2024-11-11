from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.api.schemas import SearchQuery

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "mypython-441415-8a9b22688418.json", scope
)

client = gspread.authorize(creds)
spreadsheet_id = "1-ZwYgQAglAIomCahGYBnwX5PCbFL7a7CqScTA-em7Qk"
spreadsheet = client.open_by_key(spreadsheet_id)
sheet = spreadsheet.sheet1
data = sheet.get_all_records()
data = pd.DataFrame(data)

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
        options = column.unique().tolist()
        return {"type": "ENUM", "options": options}
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


@router.post("/search")
def search_data(query: Dict[str, Optional[str]]):
    filtered_data = data.copy()

    for key, value in query.items():
        if key in filtered_data.columns and value:
            filtered_data = filtered_data[
                filtered_data[key].str.contains(value, case=False, na=False)
            ]

    return filtered_data.to_dict(orient="records")
