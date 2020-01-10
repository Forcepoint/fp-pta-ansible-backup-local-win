"""
Author: Jeremy Cornett
Date: 2018-08-29
Purpose: Create a zip of the specified folder and store it in the specified location. Retain the specified number of
records.
"""

import argparse
import datetime
import glob
import os
import shutil
import subprocess
import zipfile


if __name__ == "__main__":
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description="Create a zip of the specified folder or registry key and store it in"
                                                 "the specified location. Retain the specified number of records.")
    parser.add_argument("name", help="The name to give the zip.")
    parser.add_argument("target", help="The file or directory to zip up.")
    parser.add_argument("destination", help="The directory to place the zip.")
    parser.add_argument("retention", help="The number of zips to retain. Zero means infinite (i.e. don't delete "
                                          "anything).")
    args = parser.parse_args()

    # Give the log file some space between runs.
    print()
    print()

    is_target_registry = False
    for registry_root_key in ["HKLM", "HKCU", "HKCR", "HKU", "HKCC"]:
        if args.target.startswith(registry_root_key):
            is_target_registry = True
            break

    if is_target_registry:
        path_target = args.target
    else:
        path_target = os.path.abspath(os.path.normpath(args.target))
    path_destination = os.path.abspath(os.path.normpath(args.destination))

    # Ensure the target and destination exist.
    if not is_target_registry and not os.path.exists(path_target):
        raise ValueError("The target path must exist.")
    print("TARGET: {}".format(path_target))
    if not os.path.exists(path_destination):
        raise ValueError("The destination path must exist.")
    else:
        print("DESTINATION: {}".format(path_destination))

    # Ensure retention is a positive number.
    count_retain = int(float(args.retention))
    if count_retain < 0:
        raise ValueError("The retention number ({}) must greater than or equal to zero.".format(args.retention))

    # Construct the zip file name from the current date and time.
    path_zip = os.path.join(path_destination, "{}_{}".format(args.name,
                                                             datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")))

    # By virtue of using a timestamp as part of the name, a collision shouldn't occur, but it's good to check anyways.
    if os.path.exists("{}.zip".format(path_zip)):
        raise ValueError("COLLISION - The calculated path for the zip already exists - {}.zip".format(path_zip))

    # Zip up the target to the destination folder.
    print("ZIP: {}.zip".format(path_zip))
    if is_target_registry:
        path_reg_file = os.path.join(path_destination, "{}.reg".format(args.name))
        # https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/reg-export
        # https://docs.python.org/3/library/subprocess.html#subprocess.call
        subprocess.call(["reg.exe", "export", path_target, path_reg_file, "/y"])
        with zipfile.ZipFile("{}.zip".format(path_zip), 'w') as file_zip:
            file_zip.write(path_reg_file)
    else:
        shutil.make_archive(path_zip, "zip", path_target, path_target)

    # Check how many zips there are. If there's more than the retention value, delete the older ones. Ensure
    # that the timestamp for each is taken from the filename, not the file attributes.
    list_zips = glob.glob(os.path.join(path_destination, "{}_*.zip".format(args.name)))

    if len(list_zips) > count_retain:
        # The files are named in such a way that a lexicographical sort will sort them chronologically as well.
        list_zips.sort()
        # The more recent ones we want to retain.
        for i in range(0, count_retain):
            list_zips.pop()

        for path_zip_delete in list_zips:
            print("DELETE: {}".format(path_zip_delete))
            os.remove(path_zip_delete)
