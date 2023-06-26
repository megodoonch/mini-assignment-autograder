from bases.checker import *

import sys
import subprocess


class HWChecker(Checker):

    def __init__(self, sid):
        super().__init__(sid)

        # give the list of modules to import here
        self.modules = ["module_script"]
        self.project = "module_script"
        self.module_import_path = f'{self.project}.marking.{self.sid}.{self.module_name(0)}'

    def script_checker(self):
        """
        to check the output
        make this pass if we didn't print anything by calling the script(s) from
        the command line
        :return:
        """
        output_string = subprocess.check_output(["python", self.module_file_path()]).decode("utf-8")
        text = output_string.strip("\n")
        if not text.lower().startswith("hello world"):
            self.lower_score(2,
                f"when run as a script, should print 'hello world!', but instead it prints {text}")


    def module_checker(self):

        hello = importlib.import_module(self.module_import_path)

        # check variables etc
        try:
            msg = hello.message
            if msg != "hello world!":
                if msg.lower().startswith("hello world"):
                    self.lower_score(1,
                                     f"message should be 'hello world!' but it is '{msg}'")
                else:
                    self.lower_score(3, f"message should be 'hello world!' but it is '{msg}'")

        except Exception as e:

            self.lower_score(3,
                "message failed with exception '{}'".format(e))


if __name__ == "__main__":
    checker = HWChecker(sys.argv[1])
    checker.check()


