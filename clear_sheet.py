import requests
import smartsheet


def clear_sheet(access_token, sheet_id):
    """
    Removes all cell data from a given Smartsheet Sheet, while preserving columns, etc., by gathering a list of row
    IDs, then deleting those rows. Could probably be done without utilizing Requests - Requests in and Smartsheet
    out seems wonky - but I believe it's cleanest/shortest path to the solution.
    :param access_token:    str, required; Smartsheet api token
    :param sheet_id:        int, required; sheet ID
    :return:                none
    """

    api_prefix_url = 'https://api.smartsheet.com/2.0/sheets/'           # base Smartsheet api url for Requests
    url = api_prefix_url + str(sheet_id)                                # full url for requests
    header = {                                                          # header for requests
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
        'cache-control': 'no-cache'
    }

    ss = smartsheet.Smartsheet(access_token)                            # initialize Smartsheet client
    del_tbl = requests.get(url, headers=header).json()                  # GET table for row IDs to delete

    del_row_ids = []                                                    # empty list for row IDs
    for i, rows in enumerate(del_tbl['rows']):
        del_row_ids.append(del_tbl['rows'][i]['id'])                    # append list with row IDs

    ss.Sheets.delete_rows(sheet_id, del_row_ids)                        # delete all rows on sheet
