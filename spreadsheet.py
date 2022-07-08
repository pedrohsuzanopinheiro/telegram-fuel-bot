import os
from datetime import date

import gspread
from dotenv import load_dotenv

load_dotenv()

gc = gspread.service_account(filename="/app/gcp_key.json")

sh = gc.open(os.environ.get("SPREAD_NAME"))
worksheet = sh.worksheet(os.environ.get("SPREAD_WORKSHEET"))


def next_available_pos(worksheet, col):
    str_list = list(filter(None, worksheet.col_values(col)))
    return (len(str_list) + 1, col)


def return_current_date() -> str:
    return date.today().strftime("%d/%m/%Y")


def update_spreadsheet(valor: float, litros: float, km: int) -> None:
    current_date = return_current_date()
    params = [current_date, valor, litros, km]
    for col in range(1, 6):
        next_position = next_available_pos(worksheet, col)
        if col == 1:
            worksheet.update_cell(*next_position, str(next_position[0] - 1))
        else:
            worksheet.update_cell(*next_position, params[col - 2])
