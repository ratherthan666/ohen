"""Module for converting google sheet in proper format to csv"""

import re
import pandas as pd


def replacement(m) -> str:
    """
    Replace function to construct the new URL for CSV export
    If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    :param m: extracted parts from url
    :return: recreated url
    """
    return f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (
        f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'


def convert_google_sheet_url(sheet_url: str) -> str:
    """
    Convert url into pandas-acceptable url
    :param sheet_url: url to convert
    :return: converted url
    """
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'
    # Replace using regex
    new_url = re.sub(pattern, replacement, sheet_url)
    return new_url


def get_racers_list(sheet_url: str, dst_filename: str) -> None:
    """
    Extract a racer list from a form result
    :param sheet_url: link to data
    :param dst_filename: file to store list in
    """
    csv_url = convert_google_sheet_url(sheet_url)
    orig_df = pd.read_csv(csv_url)
    df = orig_df[['Časová značka', 'E-mailová adresa', 'Kontaktní telefonní číslo',
        'Jméno závodníka', 'Příjmení závodníka', 'Závodní kategorie závodníka']]
    for i in range(1, 46):
        tmp = orig_df[['Časová značka', 'E-mailová adresa', 'Kontaktní telefonní číslo',
            'Jméno závodníka.'+str(i), 'Příjmení závodníka.'+str(i),
                       'Závodní kategorie závodníka.'+str(i)]]
        tmp = tmp.rename(columns={'Jméno závodníka.'+str(i): 'Jméno závodníka',
                                  'Příjmení závodníka.'+str(i): 'Příjmení závodníka',
                                  'Závodní kategorie závodníka.'+ str(i): 'Závodní'
                                  ' kategorie závodníka'}).dropna()
        df = pd.concat([df, tmp])
    df["Časová značka"] = pd.to_datetime(df["Časová značka"])
    df = df.sort_values("Časová značka")
    df.to_csv(dst_filename)


if __name__ == "__main__":
    url = input("Zadejte url: ")
    filename = input("Zadejte název souboru: ")
    get_racers_list(url, filename)
