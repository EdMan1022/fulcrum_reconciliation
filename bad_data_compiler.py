import os
import pandas as pd
import datetime


def fulcrum_bad_data_compiler(month):
    """
    Combine all of the bad data rows from the current month into a single file,

    containing only the columns needed by the vendors.
    These are the Station name, the Vendor, and the ID of the response.

    This function can also easily be set up as a feed for the bad data
    prediction module.
    """

    bad_data_path = "S:/Python/Bad Data/"
    all_files = pd.Series(os.listdir(bad_data_path))
    bad_data_files = all_files[all_files.str.contains("Bad Data")]
    files1 = bad_data_files[bad_data_files.str.contains(datetime.datetime.strftime(month, "%Y-%m"))]

    total_bad_data = pd.DataFrame([])
    for file in files1:
        data = pd.read_excel("{}{}".format(bad_data_path, file))
        not_null_index = data[~data.loc[:, 'VENDOR'].isnull()].index
        data = data.loc[not_null_index, :]
        if data.shape[0] == 0:
            continue

        data_mask = data[data.loc[:, 'VENDOR'].str.lower() == 'fu'].index
        data = data.loc[data_mask, :]
        data = data.loc[:, 'ID']
        total_bad_data = pd.concat([total_bad_data, data],
                                   axis=0,
                                   ignore_index=True)

    total_file_name = "{} Fulcrum Bad Data.txt".format(datetime.datetime.strftime(month, '%B'))
    monthly_bad_data_path = "S:/Python/Bad Data by Month/"

    total_bad_data.to_csv("{}{}".format(monthly_bad_data_path, total_file_name), header=None, index=None, sep=' ', mode='w')


if __name__ == "__main__":

    try:
        last_month = datetime.date(datetime.date.today().year, (datetime.date.today().month - 1), 1)
    except ValueError:
        last_month = datetime.date(datetime.date.today().year - 1, 12, 1)
    fulcrum_bad_data_compiler(last_month)
