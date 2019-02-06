import smartsheet
import os.path

access_token = ''                                       # smartsheet api token
_dir = os.path.dirname(os.path.abspath(__file__))       # path this code is in


def export(sheet_id, export_type, export_format='csv', export_to=''):
    """
    A slightly more elegant way to export a file from Smartsheet
        * get_sheet_as_ does not support Gantt chart export
        * for Excel format, get_sheet_as and get_report_as only support xlsx output
    TODO: prevent overwriting files with the same name
    :param sheet_id:        int, required; sheet ID
    :param export_type:     str, required; 'sheet' or 'report' to call get_sheet_* or get_report_*
    :param export_format:   str, optional: 'csv', 'xlsx', or (sheet only) 'pdf' to call get_*_csv, get_*_xlsx, etc. (default 'csv')
    :param export_to:       str, optional; the file path you're exporting the file to (ex: C:\foo\bar\ ) (default
    :return:                none
    """

    ss = smartsheet.Smartsheet(access_token)            # initialize client
    ss.errors_as_exceptions(True)                       # call out errors

    if export_to == '':                                 # if no export location specified, use the filepath of this code
        export_path = _dir
    else:
        export_path = export_to

    sheet_name = ss.Sheets.get_sheet(sheet_id).name

    if export_type == 'sheet':                          # calls get_sheet_as_
        user_msg = export_sheet(ss, sheet_id, export_format, export_path, sheet_name)
    elif export_type == 'report':                       # calls get_report_as_
        user_msg = export_report(ss, sheet_id, export_format, export_path, sheet_name)
    else:
        user_msg = 'export_type not valid. Please use \'sheet\' or \'report\'.'

    print(user_msg)


def export_sheet(ss, sheet_id, export_format, export_path, sheet_name):
    """
    Exports a sheet, given export filetype and location. Allows export format 'csv', 'pdf', or 'xlsx'.
    :param ss:              initialized smartsheet client instance
    :param sheet_id:        int, required; sheet id
    :param export_format:   str, required; 'csv', 'pdf', or 'xlsx'
    :param export_path:     str, required; filepath to export sheet to
    :param sheet_name:      str, required; name of sheet exported
    :return:                str, indicating failure or success, with path, filename, extension
    """

    if export_format == 'csv':
        ss.Sheets.get_sheet_as_csv(sheet_id, export_path)
    elif export_format == 'xlsx':
        ss.Sheets.get_sheet_as_excel(sheet_id, export_path)
    elif export_format == 'pdf':                        # there is an optional paperSize parameter; default is A1
        ss.Sheets.get_sheet_as_pdf(sheet_id, export_path)

    if export_format == 'csv' or export_format == 'xlsx' or export_format == 'pdf':
        return 'Sheet exported to {}{}.{}'.format(export_path, sheet_name, export_format)
    else:
        return 'export_format \'{}\' is not valid. Must be \'csv\', \'pdf\', or \'xlsx\''.format(export_format)


def export_report(ss, report_id, export_format, export_path, sheet_name):
    """
    Exports a report, given export filetype and location. Allows export format 'csv' or 'xlsx'.
    :param ss:              initialized smartsheet client instance
    :param report_id:       int, required; report id
    :param export_format:   str, required; 'csv' or 'xlsx'
    :param export_path:     str, required; filepath to export sheet to
    :param sheet_name:      str, required; name of sheet exported
    :return:                str, indicating failure or success, with path, filename, extension
    """

    if export_format == 'csv':
        ss.Sheets.get_sheet_as_csv(report_id, export_path)
    elif export_format == 'xlsx':
        ss.Sheets.get_sheet_as_excel(report_id, export_path)

    if export_format == 'csv' or export_format == 'xlsx':
        return 'Report exported to {}{}.{}'.format(export_path, sheet_name, export_format)
    else:
        return 'export_format \'{}\' is not valid. Must be \'csv\' or \'xlsx\''.format(export_format)
