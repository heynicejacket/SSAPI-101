import smartsheet
import os.path

access_token = ''                                       # smartsheet api token
file_name = ''                                          # name of file to import
_dir = os.path.dirname(os.path.abspath(__file__))       # path this code is in


def import_sheet(f, upload_to=0, sheet_name='', upload_from='', header_row=0):
    """
    A slightly more elegant way to import a file into smartsheet, regardless of filetype
    TODO: include TSV/txt as an option
    TODO: pull folder name to return to user over folder id
    :param f:               str, required; filename with file extension (import.csv or import.xlsx)
    :param sheet_name:      str, optional; what Smartsheet will call the sheet name
    :param upload_from:     str, optional; the file path you're uploading the file from (ex: C:\foo\bar\ )
    :param upload_to:       int, optional; folderID
    :param header_row:      int, optional; which row the header is on
    :return:                none
    """

    ss = smartsheet.Smartsheet(access_token)            # initialize client
    ss.errors_as_exceptions(True)                       # call out errors

    if sheet_name == '':                                # if no sheet name, use the filename (ss removes the file ext)
        sheet_name = file_name

    if upload_from == '':                               # if no upload location specified, use the filepath of this code
        file_location = _dir
    else:
        file_location = upload_from

    ext = get_file_ext(f)                               # calls the filetype function to get the file extension
    file_path = file_location + '\\' + f                # concatenate the filepath and file name

    # calls import_csv_sheet if csv, with or without upload folderID
    if ext == 'csv':
        if upload_to == 0:
            ss.Sheets.import_csv_sheet(file_path, sheet_name, header_row)
        else:
            ss.Folders.import_csv_sheet(upload_to, file_path, sheet_name, header_row)

    # calls import_xlsx_sheet if xlsx, with or without upload folderID
    if ext == 'xlsx':
        if upload_to == 0:
            ss.Sheets.import_xlsx_sheet(file_path, sheet_name, header_row)
        else:
            ss.Folders.import_xlsx_sheet(upload_to, file_path, sheet_name, header_row)

    # if neither csv or xlsx, fail
    if ext == 'csv' or ext == 'xlsx':
        if upload_to == 0:
            upload_location = 'default/main location'
        else:
            upload_location = upload_to
        print('Uploading {} \n from {} \n to {}.'.format(f, file_path, upload_location))
    else:
        print('File type .' + ext + ' is invalid. Nothing uploaded.')


def get_file_ext(f):
    """
    takes in a filename.ext, finds extension by looking for the last . delimiter, and returns the filetype as str
    :param f:       str, required; filename with extension
    :return:        file extension
    """

    delim = f.rfind('.') + 1                            # locate the delimiter between the file name and file extension
    filetype = f[delim:]                                # grabs the substring after the delimiter

    return filetype
