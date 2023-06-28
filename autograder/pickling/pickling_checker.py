import io
import pickle
import subprocess
import sys
from collections import Counter
from contextlib import redirect_stdout

from nltk.corpus import conll2000
from checker import *


def tag_types_input_codec(path):
    """
    inverts printing a TagTypes object to file, but since we only print
     the counts, we only get a counter back
    :param path: path to printed file
    :return: counter for tag types
    """
    pos_dict = Counter()

    with open(path, 'r') as conn:
        for line in conn.readlines():
            parts = line.split()
            if len(parts) == 3:
                pos = parts[0]
                n = parts[1]
                try:
                    pos_dict[pos] = int(n)
                except ValueError:
                    pass
            else:
                pass
    return pos_dict


def string2tag_types(string):
    """
    inverts printing a TagTypes object to file, but since we only print
     the counts, we only get a counter back
    :param string: the string rep of the object
    :return: counter for tag types
    """
    pos_dict = Counter()

    lines = string.split("\n")
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            pos = parts[0]
            n = parts[1]
            try:
                pos_dict[pos] = int(n)
            except ValueError:
                pass
        else:
            pass
    return pos_dict


class HWChecker(Checker):

    def __init__(self, sid):

        self.project = "pickling"
        self.modules = ["pickles"]
        with open("tags.pickle", 'rb') as f:
            self.model = pickle.load(f)

        super().__init__(sid)

    def script_checker(self):
        """
        checks that the printed model is the one that should have been printed
        :return:
        """

        # run pickler -- should write a pickle
        print("writing a pickle")
        command = f"python {self.module_file_name(0)} --pickle {self.sid}.pickle"
        try:
            subprocess.run(command.split(), check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            last_part_of_error = e.stderr.decode("utf-8").split("\n")[-2]
            self.lower_score(5, "command '{}' threw error (code {}): {}".format(command, e.returncode, last_part_of_error))
        except subprocess.TimeoutExpired:
            self.lower_score(5, f"timed out running with --pickle")
        except Exception as e:
            self.lower_score(5, f"running script with --pickle threw error: {e}")

        print("reading a pickle")
        # run unpickler -- should pipe output to the variable as a string
        command = f"python {self.module_file_name(0)} --unpickle {self.sid}.pickle"
        try:
            student_counts_string = subprocess.check_output(command.split(), timeout=10, stderr=subprocess.PIPE).decode("utf-8")
            try:
                student_counts = string2tag_types(student_counts_string)
                try:
                    if student_counts != self.model.counts:
                        self.lower_score(1, f"printed TagTypes model incorrect")
                except Exception as e:
                    self.lower_score(2, f"comparing printed TagTypes model to original threw error: {e}")

            except Exception as e:
                self.lower_score(2,
                                 f"reading in printed TagTypes model threw error: {e}")

        except subprocess.CalledProcessError as e:
            last_part_of_error = e.stderr.decode("utf-8").split("\n")[-2]
            self.lower_score(5, "command '{}' threw error (code {}): {}".format(command, e.returncode, last_part_of_error))
        except subprocess.TimeoutExpired:
            self.lower_score(5, f"timed out running with --unpickle")
        except Exception as e:
            self.lower_score(5, f"running script with --unpickle threw error: {e}")

    def module_output_checker(self):
        pass

    def module_checker(self):
        with redirect_stdout(io.StringIO()) as f:
            try:
                pickles = importlib.import_module(self.module_name())
            except ModuleNotFoundError:
                self.lower_score(5, f"couldn't import {self.modules[0]}. Misnamed file?")
                self.unusable = True
            except Exception as err:
                self.lower_score(5, f"importing {self.modules[0]} threw error: {err}")
                self.unusable = True
            if len(f.getvalue()) > 0:
                print(f"printed {f.getvalue()} on import", file=sys.stderr)
        if self.unusable:  # give up if we couldn't import it
            return

        # check variables etc
        try:
            pickles.make_and_pickle(conll2000, f"{self.sid}.pickle", tagset='universal')
            try:
                with redirect_stdout(io.StringIO()) as f:
                    with open(f"{self.sid}.pickle", 'rb') as p:
                        reread_tag_types = pickle.load(p)
                        if reread_tag_types != self.model:
                            self.lower_score(1, "make_and_pickle either didn't build the right TagTypes or didn't pickle it right")
            except Exception as e:
                self.lower_score(2, f"error when loading pickle stored by make_and_pickle: {e}")

            try:
                with redirect_stdout(io.StringIO()) as f:
                    student_tag_types = pickles.unpickle("tags.pickle")
                    if len(f.getvalue()) > 0:
                        self.lower_score(2, f"unpickle shouldn't print but it printed {trunc(f.getvalue())}")
                try:
                    if student_tag_types != self.model:
                        self.lower_score(1, "unpickle didn't load my pickled model correctly")
                except Exception as e:
                    self.lower_score(2, f"comparing models threw error {e}")

            except Exception as e:
                self.lower_score(2, f"unpickle of your pickle failed with exception {e}")

        except Exception as e:
            self.lower_score(3, f"make_and_pickle failed with exception '{e}'")


if __name__ == "__main__":
    student_id = sys.argv[1]
    checker = HWChecker(student_id)
    checker.check()

