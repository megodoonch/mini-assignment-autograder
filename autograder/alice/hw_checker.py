from autograder.bases.checker import *
from collections import defaultdict


# Solutions:
# w.lower() == "alice"
correct = {
    20: {'and'},
    17: {'was'},
    16: {'i'},
    12: {'thought', 's'},
}

# only Alice (not ALICE) and lower-casing
correct_Alice = {
    20: {'and'},
    17: {'was'},
    16: {'i'},
    12: {'thought'},
    11: {'had', 'as', 'said', 'could'}
}

# Alice and ALICE but no lowercasing
no_lower = {
    17: {'was', 'and'},
    16: {'i'},
    12: {'thought'},
    11: {'had', 'as', 'said', 'could'}
}

late_punctuation_removal = {
    17: {'was'},
    12: {'thought'},
    11: {'had', 'said', 'could'}
}

kept_punctuation = {
    76: ',',
    54: '.',
    17: 'was',
    16: ';',
    13: "'"
}

possibles = [correct, no_lower, late_punctuation_removal, kept_punctuation, correct_Alice]


def check_solution(student_dict, solution_dict):
    # get the keys in descending order because
    # only the last one might be missing members
    correct_keys = sorted(solution_dict.keys(), reverse=True)

    if solution_dict.keys() != student_dict.keys():
        # print("wrong keys")
        return False
    else:
        for k in correct_keys[:-1]:  # check all but the last one
            if student_dict[k] != solution_dict[k]:
                # print("not this one:", solution_dict[k], student_dict[k])
                return False
        # for the last one it just has to be a subset
        last = correct_keys[-1]
        if not student_dict[last].issubset(solution_dict[last]):
            return False
            # print("not this one:", solution_dict[last], student_dict[last])

    return True


class HWChecker(Checker):

    def __init__(self, sid):
        super().__init__(sid)

        # give the list of modules to import here
        self.modules = ["alice"]
        self.project = "alice"
        self.module_import_path = f'{self.project}.marking.{self.sid}.{self.module_name(0)}'


    def script_checker(self):
        """
        should print:
        and 20
        was 17
        i 16
        s 12
        thought 12
        """

        try:
            output = subprocess.check_output(["python", self.module_file_path()]).decode("utf-8")
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            self.lower_score(4, f"running {self.module_name()} as a script fails with error {grepexc.returncode}: {grepexc.output}")
            return

        raw_text = output.strip("\n")
        if len(raw_text) == 0:
            self.lower_score(10, "no output")
        else:
            student_counts = defaultdict(set)
            text = raw_text.split("\n")
            type_errors = False
            len_errors = False
            other_errors = False
            # check length
            length = 5
            if len(text) > 5:
                self.lower_score(2, "more than 5 lines printed")
            elif len(text) < 5:
                self.lower_score(2, "fewer than 5 lines printed")
                length = len(text)

            # get the data from the printed text
            for line in text[:length]:
                line = line.split()
                if len(line) == 2:
                    word = line[0]
                    number = None
                    try:
                        number = int(line[1])
                    except ValueError:
                        type_errors = True
                        try:
                            # maybe they printed them in the wrong order
                            number = int(line[0])
                            word = line[1]
                        except Exception:
                            other_errors = True
                    # if all went well, add it to the dict
                    if number:
                        student_counts[number].add(word.lower())
                else:
                    len_errors = True
            if type_errors:
                self.lower_score(2,
                                 "should print 'word count' but count isn't an int. Trying 'count word'.")
            if other_errors:
                self.lower_score(2,
                                 "tried switching word and count, but that didn't work either")
            if len_errors:
                self.lower_score(
                    2, f"should print a word and a count separated by a space, but printed {trunc(raw_text)}")

            # find out if they got it right or made an known error
            best_version = None
            for i, counts in enumerate(possibles):
                if check_solution(student_counts, counts):
                    # print(i, student_counts, counts)
                    best_version = i
                    break

            # inspect the best match:
            if best_version is not None:
                # 0 and 4 are correct
                if best_version == 1:
                    self.lower_score(2, "It looks like you used a case-sensitive word counter")
                elif best_version == 2:
                    self.lower_score(2, "It looks like you forgot to skip over punctuation when counting successors")
                elif best_version == 3:
                    self.lower_score(3, "It looks like you forgot to remove punctuation")
            else:  # other error
                self.lower_score(4, "Your printed counts are incorrect")


if __name__ == "__main__":
    checker = HWChecker(sys.argv[1])
    checker.check()
