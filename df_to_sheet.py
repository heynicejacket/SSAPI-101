import smartsheet
import maya
# import datetime                                                           # uncomment this and remove maya if needed


def import_df(access_token, df, write_to_sheet_id='', new_sheet_name=''):
    """
    Imports a pandas DataFrame into Smartsheet. If a sheet_id is given, the DataFrame is appended to the bottom of the
    sheet. If not, a new sheet is created, in the shape of the DataFrame.
    :param access_token:            str, required; Smartsheet api token
    :param df:                      DataFrame, required; pandas DataFrame
    :param write_to_sheet_id:       int, required; sheet ID
    :return:                        none
    """
    ss = smartsheet.Smartsheet(access_token)                                # initialize client
    ss.errors_as_exceptions(True)                                           # call out errors

    if write_to_sheet_id == '':                                             # if no sheet to write to, create new
        write_to_sheet_id = new_sheet_from_df(ss, df, new_sheet_name)

    append_df(ss, df, write_to_sheet_id)                                    # append sheet with DataFrame


def new_sheet_from_df(ss, df, sheet_name=''):
    """
    Call if no sheet_id given, as Smartsheet needs somewhere to import the DataFrame. Uses column names of DataFrame.
    TODO: add option to create new sheet in specific location
    :param ss:                      initialized smartsheet client instance
    :param df:                      DataFrame, required; pandas DataFrame
    :param sheet_name:              str, optional; name of new Smartsheet to be created (if '', use date/timestamp)
    :return:                        Smartsheet sheet_id
    """
    # col_list = df_to_ss_col_list(df)                                        # retrieve a list of column dictionaries

    if sheet_name == '':
        # if you need datetime, uncomment the line below, and remove the line below that - but seriously, blech city
        # sheet_name = 'newsheet ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        sheet_name = 'new sheet ' + str(maya.now())                         # create new sheet with datetime stamp

    temp_sheet = ss.models.Sheet({                                          # new sheets need a name and a column list
        'name': sheet_name,
        'columns': df_to_ss_col_list(df)                                    # retrieve a list of column dictionaries
    })

    new_sheet_id = ss.Home.create_sheet(temp_sheet).result.id               # create a new sheet and get its id

    return new_sheet_id                                                     # return the sheet id for appending df data


def append_df(ss, df, sheet_id):
    """
    Smartsheet has rate limits (http://smartsheet-platform.github.io/api-docs/#rate-limiting), so it's best to hit it
    as little as possible; this builds a block of i rows, j columns wide, and appends it once, rather than i * j times.
    :param ss:
    :param df:
    :param sheet_id:
    :return:
    """

    list_of_rows = []                                                       # empty list to populate with Row objects
    list_of_columns = []

    for c, column in enumerate(df_to_ss_col_list(df)):                      # done here to limit Smartsheet server hits
        list_of_columns.append(ss.Sheets.get_columns(sheet_id, include_all=True).data[c].id)

    for i, rows in df.iterrows():                                           # populate each row

        temp_row = ss.models.Row()                                          # create a temporary Row object
        temp_row.to_top = True                                              # Smartsheet requires a position for the Row

        for j, columns in enumerate(df):                                    # populate cells in each column along row

            temp_row.cells.append({
                'column_id': list_of_columns[j],                            # column ID
                'value': df.iloc[i, j]                                      # DataFrame cell in row i, column j
            })

        list_of_rows.append(temp_row)                                       # append the row to the list of rows

    ss.Sheets.add_rows(sheet_id, list_of_rows)                              # add the list of rows to the sheet


def df_to_ss_col_list(df):
    """
    Creates a list of column dictionaries from a DataFrame, necessary for creating a new sheet in Smartsheet
    TODO: check that first column is not formatted to datetime, this will probably break the append
    :param df:      DataFrame, required; complete pandas DataFrame
    :return:        Smartsheet-ready formatted array of column headers to create new sheet
    """
    new_sheet_col_list = []                                                 # create empty list for col dict elements
    for col in df:

        i = df.columns.get_loc(col)                                         # get current column number
        p_col = False
        if i == 0:
            p_col = True                                                    # if first column, set primary to True

        temp_new_column_dict = {'title': col, 'primary': p_col, 'type': 'TEXT_NUMBER'}      # column dictionary
        new_sheet_col_list.append(temp_new_column_dict)                                     # add dictionary to list

    return new_sheet_col_list
