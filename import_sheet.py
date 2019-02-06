import smartsheet
import os.path

access_token = ''                                       # smartsheet api token
file_name = ''                                          # name of file to import
_dir = os.path.dirname(os.path.abspath(__file__))       # path this code is in


def import_sheet(f, import_to=0, sheet_name='', import_from='', header_row=0):
    """
    A slightly more elegant way to import a file into Smartsheet, regardless of filetype
    TODO: include TSV/txt as an option
    :param f:               str, required; filename with file extension (import.csv or import.xlsx)
    :param sheet_name:      str, optional; what Smartsheet will call the sheet name
    :param import_from:     str, optional; the file path you're importing the file from (ex: C:\foo\bar\ )
    :param import_to:       int, optional; folderID
    :param header_row:      int, optional; which row the header is on
    :return:                none
    """

    ss = smartsheet.Smartsheet(access_token)            # initialize client
    ss.errors_as_exceptions(True)                       # call out errors

    if sheet_name == '':                                # if no sheet name, use the filename (ss removes the file ext)
        sheet_name = file_name

    if import_from == '':                               # if no import location specified, use the filepath of this code
        file_location = _dir
    else:
        file_location = import_from

    ext = get_file_ext(f)                               # calls the filetype function to get the file extension
    file_path = file_location + '\\' + f                # concatenate the filepath and file name

    if ext == 'csv':                                    # import_csv_sheet if csv, with or without import folderID
        if import_to == 0:
            ss.Sheets.import_csv_sheet(file_path, sheet_name, header_row)
        else:
            ss.Folders.import_csv_sheet(import_to, file_path, sheet_name, header_row)

    if ext == 'xlsx':                                   # import_xlsx_sheet if xlsx, with or without import folderID
        if import_to == 0:
            ss.Sheets.import_xlsx_sheet(file_path, sheet_name, header_row)
        else:
            ss.Folders.import_xlsx_sheet(import_to, file_path, sheet_name, header_row)

    if ext == 'csv' or ext == 'xlsx':                   # report to user success or failure
        if import_to == 0:                              # if no location provided, return default string
            import_location = 'default/main location'
        else:                                           # return name value from folderID with .name
            import_location = ss.Folders.get_folder(import_to).name
        print('Importing {} \n from {} \n to {}.'.format(f, file_path, import_location))
    else:
        print('File type .' + ext + ' is invalid. Nothing imported.')


def get_file_ext(f):
    """
    takes in a filename.ext, finds extension by looking for the last . delimiter, and returns the filetype as str
    :param f:       str, required; filename with extension
    :return:        file extension
    """

    delim = f.rfind('.') + 1                            # locate the delimiter between the file name and file extension
    filetype = f[delim:]                                # grabs the substring after the delimiter

    return filetype
