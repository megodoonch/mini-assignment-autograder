""""
Wrapper script for checking a mini assignment

author:  Meaghan Fowlie
contact: m.fowlie@uu.nl

Given a path to a spreadsheet and to a zip file of assignments, both as downloaded from Blackboard,
    and the path to the folder of the assignment,
    runs <assignment>.hw_checker.py

For me, if student with id 0512784 hands in Mini-Assignment 0 by submitting a file called my_number.py
    at 11:46:08 on 2022-06-13, Blackboard renames the file
    Mini-Assignment 0_0512784_attempt_2022-06-13-11-46-08_my_number.py

    If Blackboard does something different for you, update function extract_id_and_module_from_file_name

You'll also need to update local_marks_path
"""

from all_submissions_checker import SubmissionsChecker
import csv
import shutil
import subprocess
import os
import argparse
import zipfile
from pathlib import Path

from bases.checker import student_module_path
from bases.checker import Checker

# This is the parent directory where the output will be saved to. Update it for your system.
local_marks_path = "~/Documents/UU_teaching/student-data/introCL/introCL2023/minis/"




# get the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--spreadsheet", help="path to downloaded BB spreadsheet for marks")
parser.add_argument("-z", "--zip", help="path to zip file of submissions")
parser.add_argument('-p', '--project', required=True,
                    help="path to assignment folder (e.g. favourite_number)")
parser.add_argument("-e", "--extra-file", dest='extra_files', action='append',
                    help="path to extra file to copy into the working directory (use more than once if needed)")

args = parser.parse_args()

# extract the name of the project from the path to the project file
project_path = args.project
# project_parts = [s for s in project_path.split("/") if len(s) > 0]
# project_name = project_parts[-1]

checker = SubmissionsChecker(args.project, args.spreadsheet, args.zip, args.extra_files)
# whether we need to unzip (this can be false if it's not your first pass)
unzip = args.zip is not None
if unzip:
    checker.set_up_working_directory()
# TODO remove
checker.copy_in_checkers()
checker.check_all_submissions()
if args.spreadsheet is not None:
    checker.update_spreadsheet()



# update the path to where the marks will be written
# local_marks_path += project_name
# local_marks_path = Path(local_marks_path).expanduser()

# files to be copied into the working directory
# checker_files = f"checker.py hw_checker.py".split()

# whether we need to unzip (this can be false if it's not your first pass)
# unzip = args.zip is not None







# # unzip
# working_directory = f"{project_path}/marking/"
# os.makedirs(working_directory, exist_ok=True)
# if unzip:
#     try:
#         with zipfile.ZipFile(args.zip) as z:
#             z.extractall(working_directory)
#             print("Extracted all submissions")
#
#     except Exception as err:
#         print(f"couldn't unzip: {err}")

# copy in files
# shutil.copy(f"{project_path}/hw_checker.py", working_directory)
# shutil.copy("bases/checker.py", working_directory)
# if args.extra_files is not None:
#     for path in args.extra_files:
#         shutil.copy(path, working_directory)
#         shutil.copy(path, "../src/")
#         checker_files.append(path.split("/")[-1])
#

# # rename the files and get a list of all ids
# # student with e.g. id 1234567 handed in e.g. my_number.py
# # we'll rename them 1234567_my_number.py
# ids = []  # all student IDs encountered, used to loop through the assignments
#
# for file in os.listdir(working_directory):
#     if file.endswith(".py") and file not in checker_files:
#         current_id, module = extract_id_and_module_from_file_name(file)
#         if unzip:
#             os.makedirs(f"{working_directory}/{current_id}")
#             os.rename(f"{working_directory}/{file}", f"{working_directory}/{student_module_path(module, current_id)}")
#         ids.append(current_id)
#
# ids = sorted(set(ids))

# os.chdir(working_directory)

# initialise the CSV file of marks
# dummy_checker = Checker("")
# with open(dummy_checker.csv, 'a') as f:
#     writer = csv.writer(f, dialect='unix')
#     writer.writerow(
#         ["Username", "Mark", "Feedback"])



# # mark the assignments
# for student_id in ids:
#     print(f"student {student_id}")
#
#     try:
#         subprocess.run(["python", f"hw_checker.py", student_id], timeout=40, check=True,
#                        capture_output=True)
#         failed = False
#     except subprocess.TimeoutExpired:
#         err = "timeout"
#         failed = True
#     except Exception as err:
#         print("\n**FAILED**", err)
#         failed = True
#     if failed:
#         with open(dummy_checker.csv, 'a') as f:
#             writer = csv.writer(f, dialect='unix')
#             writer.writerow([student_id, dummy_checker.min_output_grade,
#                              f"autograding threw error: {err}"])
#
# os.chdir("../..")
# os.makedirs(local_marks_path, exist_ok=True)
#
# print("updating spreadsheet", args.spreadsheet)
# command = f"python bases/spreadsheet_updater.py {working_directory}/{dummy_checker.csv} {args.spreadsheet}"
# result = subprocess.run(command.split())
#
# if result.returncode == 0:
#     print("copying marks to", local_marks_path)
#     shutil.copy(f"{working_directory}/{dummy_checker.csv}", local_marks_path)
#     shutil.copy("marks.csv", local_marks_path)
