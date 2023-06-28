import csv
from abc import ABC, abstractmethod
import subprocess
import importlib
import sys


class Checker(ABC):
    """
    Abstract Class for marking mini-assignment
    Implement this for each assignment
    A new Checker instance is created for each student's assignment


    Attributes:
        sid : (str) student ID number
        grade : (float) tracks the student's grade
        comments : (str) gathers the comments into a string
        out_file : (str) path to self.sid-out.txt; write to and read from when running the script #TODO still true?
        err_file : (str) path to self.sid-err.txt; redirects standard error to this file
        module_out_file : (str) path to self.sid-module_out.txt; write to and reead from when importing

    """

    project: str
    modules: [str]

    def __init__(self, sid):
        """
        :param sid: student id number
        """
        self.csv = f"{self.project}.csv"
        self.sid = sid
        self.comments = ""
        self.out_file = "{}-out.txt".format(self.sid)
        self.err_file = "{}-err.txt".format(self.sid)
        self.module_out_file = "{}-module-out.txt".format(self.sid)
        self.show_subtractions = False  # if True, prints the subtracted marks for each infraction
        self.full_points_if_runs = True  # if True, students lose points only for code that throws errors
        self.max_output_grade = 1  # everything we've made assumes this is out of 10, so let's keep that and use this
        # for outputting the student's final grade
        self.max_internal_grade = 10  # max score for the grader, traditionally 10
        self.grade = self.max_internal_grade
        self.minimum_score = self.max_internal_grade/2   # this'll replace their mark if it goes below it

    def module_name(self, n=0):
        """
        makes the module name for the nth module of self.modules
        Args:
            n: int: which module

        Returns:
            str: f"{self.sid}_{self.modules[n]}"
        """
        return f"{self.modules[n]}_{self.sid}"

    def module_file_name(self, n=0):
        """
        Makes the file name for the nth module of self.modules
        Args:
            n: int: which module

        Returns:
            str: f"{self.sid}_{self.modules[n]}.py"
        """
        return f"{self.module_name(n)}.py"

    def output_checker(self):
        """
        opens self.out_file and updates grade and comments
        if there's no such file for this HW, just pass.
        :return:
        """
        pass

    def module_checker(self):
        """
        imports all modules and updates grades and comments
        Note we check in check() whether the modules are importable,
        and remove them from self.modules if not.
        :return:
        """
        pass

    def module_output_checker(self):
        """
        checks module_out_file
        Default behaviour: checks that nothing was printed on import.
        Override it if you want a different behaviour
        """
        i = 0
        try:
            for i in range(len(self.modules)):
                import_output = subprocess.check_output(["python", "importer.py", self.module_name(0)],
                                                        timeout=10).decode("utf-8").strip()
                if len(import_output) > 0:
                    self.lower_score(
                        2,
                        f"{self.modules[i]} shouldn't print when called as a module, but it prints {trunc(import_output)}"
                    )
        except subprocess.CalledProcessError as e:
            self.lower_score(10, f"importing {self.modules[i]} raised error: {e}")

    def add_comment(self, c):
        """
        makes a comment appropriate for the csv out of a string
        removes any commas, adds a space and a semi-colon at the end
        :param c: string
        :return: string
        """
        c = c.replace('\n', ' ')
        self.comments += f"{c}; "

    def lower_score(self, points, comment=None):
        if comment is None:
            comment = ""
        if self.show_subtractions:
            self.add_comment("(-{}) {}".format(points, comment))
        else:
            self.add_comment(comment)
        self.grade -= points

    def check(self):
        """
        checks the homework, calling output_checker, module_output_checker, and module_checker
        """

        # add command line errors to comments
        with open(self.err_file) as e:
            l = e.read().strip()
            if l != "":
                self.add_comment(l)

        self.output_checker()

        # we imported it with importer.py. Check if it printed right
        self.module_output_checker()

        # check the modules
        self.module_checker()

        if self.grade < self.minimum_score:
            self.grade = self.minimum_score

        if self.grade >= self.max_internal_grade:
            self.add_comment("Excellent!")

        if self.full_points_if_runs and self.grade < self.max_internal_grade:
            self.grade = self.max_internal_grade

        self.grade = self.grade * (self.max_output_grade / self.max_internal_grade)
        self.comments = f"Score {self.grade}/{self.max_output_grade}; Comments: {self.comments}"

        # write to csv
        with open(self.csv, 'a') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow([self.sid, self.grade, self.comments])


def trunc(text, length=100):
    """
    truncates `text` to `length`
    Args:
        text: string
        length: int (default 30)

    Returns:
        string of length `length` plus "..."
    """
    if len(text) > length:
        return text[:30] + "..."
    else:
        return text
