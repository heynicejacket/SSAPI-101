import requests
import pandas as pd


def sheet_to_df(access_token, sheet_id):
    """
    Converts raw Smartsheet Sheet objects into a nice and tidy pandas DataFrame, just like mum used to make
    For more detail, see: https://dataideas.blog/2018/11/13/loading-json-it-looks-simple-part-4/
    :param access_token:    str, required; Smartsheet api token
    :param sheet_id:        int, required; sheet ID
    :return:                pandas DataFrame of a Smartsheet sheet's contents
    """

    api_prefix_url = 'https://api.smartsheet.com/2.0/sheets/'       # base Smartsheet api url for Requests
    url = api_prefix_url + str(sheet_id)                            # full url for requests
    header = {                                                      # header for requests
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
        'cache-control': 'no-cache'
    }

    r = requests.get(url, headers=header)                           # create requests Response object of sheet's json
    sheet_dic = r.json()                                            # convert json to a dictionary

    col_list = []
    for c in sheet_dic['columns']:                                  # for all columns in the sheet dictionary
        col_list.append(c['title'])                                 # add title value to col_list

    df = pd.DataFrame(columns=col_list)                             # create an empty DataFrame with the col_list

    for r in sheet_dic['rows']:                                     # iterate through all cells, place in rows and cols
        values = []                                                 # initialize values list for each row
        for c in r['cells']:
            if c.get('value'):                                      # politely handle empty cells
                values.append(c['value'])
            else:
                values.append('')
        df = df.append(dict(zip(col_list, values)), ignore_index=True)      # zip joins col_list and values

    return df
