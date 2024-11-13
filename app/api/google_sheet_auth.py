import gspread_asyncio
from google.oauth2.service_account import Credentials
from aiocache import cached


def get_google_sheets_client(credentials_file: str):
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    agcm = gspread_asyncio.AsyncioGspreadClientManager(lambda: credentials)
    return agcm


@cached(ttl=60)
async def fetch_sheet_data(client_manager, spreadsheet_id: str):
    client = await client_manager.authorize()
    spreadsheet = await client.open_by_key(spreadsheet_id)
    worksheet = await spreadsheet.get_worksheet(0)  # выбор листа
    records = await worksheet.get_all_records()
    return records
