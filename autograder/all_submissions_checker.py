import csv
import importlib
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from bases.checker import student_module_path


def extract_id_and_module_from_file_name(file_name):
    """
    files look like this: "Mini-Assignment 0_0512784_attempt_2022-06-13-11-46-08_my_number.py"
    Args:
        file_name: str: the name of the file as downloaded from Blackboard

    Returns: string pair: (student id, module name)
    """
    file_parts = file_name.split("_")
    student_id_number = file_parts[1]  # 0512784
    the_module = "_".join(file_parts[4:])  # my_number.py
    the_module = the_module.split(".")[0]  # my_number
    return student_id_number, the_module


class SubmissionsChecker():
    def __init__(self, project_path, spreadsheet_path, zip_path=None, extra_files=None):
        project_parts = [s for s in project_path.split("/") if len(s) > 0]
        self.project = project_parts[-1]
        self.project_path = project_path
        self.csv = f"{self.project}.csv"
        self.working_directory = f"{self.project_path}/marking/"
        # self.modules = modules
        self.zip_path = zip_path
        self.ids = []
        self.local_marks_path = "~/Documents/UU_teaching/student-data/introCL/introCL2023/minis/"
        # update the path to where the marks will be written
        self.local_marks_path += self.project
        self.local_marks_path = Path(self.local_marks_path).expanduser()
        self.spreadsheet_path = spreadsheet_path
        self.extra_files = extra_files

    def set_up_working_directory(self):

        os.makedirs(self.working_directory, exist_ok=True)
        try:
            with zipfile.ZipFile(self.zip_path) as z:
                z.extractall(self.working_directory)
                print("Extracted all submissions")

        except Exception as err:
            print(f"couldn't unzip: {err}")

        # rename the files and get a list of all ids
        # put them in their own folders
        ids = []
        for file in os.listdir(self.working_directory):
            if file.endswith(".py") and file != "checker.py" and file != "hw_checker.py":
                current_id, module = extract_id_and_module_from_file_name(file)
                os.makedirs(f"{self.working_directory}/{current_id}")
                print(f"made directory {self.working_directory}/{current_id}")
                os.rename(f"{self.working_directory}/{file}",
                          f"{self.working_directory}/{student_module_path(module, current_id)}")
                ids.append(current_id)

        self.ids = sorted(set(ids))

        shutil.copy(f"{self.project_path}/hw_checker.py", self.working_directory)
        shutil.copy("bases/checker.py", self.working_directory)
        if self.extra_files is not None:
            for path in self.extra_files:
                shutil.copy(path, self.working_directory)
                shutil.copy(path, "../src/")
                # checker_files.append(path.split("/")[-1])

    def check_all_submissions(self):

        os.chdir(self.working_directory)
        sys.path.append(self.working_directory)

        # initialise the CSV file of marks
        with open(self.csv, 'w') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow(
                ["Username", "Mark", "Feedback"])

        checker = importlib.import_module(f"{self.project}.marking.hw_checker")
        # mark the assignments
        for student_id in os.listdir("."):
            if re.search(r'[a-zA-Z]', student_id):
                continue
            print(f"student {student_id}")
            student_checker = checker.HWChecker(student_id)
            try:
                grade, comments = student_checker.check()
                grade = round(grade, 3)
                with open(self.csv, 'a') as f:
                    writer = csv.writer(f, dialect='unix')
                    writer.writerow([student_id, grade, comments])
            except Exception as err:
                print("\n**FAILED**", err)
                with open(self.csv, 'a') as f:
                    writer = csv.writer(f, dialect='unix')
                    writer.writerow([student_id, student_checker.min_output_grade,
                                     f"autograding threw error: {err}"])


        os.chdir("../..")
        os.makedirs(self.local_marks_path, exist_ok=True)

    def update_spreadsheet(self):
        print("updating spreadsheet", self.spreadsheet_path)
        command = f"python bases/spreadsheet_updater.py {self.working_directory}/{self.csv} {self.spreadsheet_path}"
        result = subprocess.run(command.split())

        if result.returncode == 0:
            print("copying marks to", self.local_marks_path, "marks.csv")
            shutil.copy(f"{self.working_directory}/{self.csv}", self.local_marks_path)
            shutil.copy("marks.csv", self.local_marks_path)

    def copy_in_checkers(self):
        shutil.copy(f"{self.project_path}/hw_checker.py", self.working_directory)
        shutil.copy("bases/checker.py", self.working_directory)
