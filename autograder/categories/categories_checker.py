from checker import *
from collections import Counter, defaultdict
import nltk


def get_counts(word, lower=True):
    if lower:
        word = word.lower()
    counts = Counter()
    brown = nltk.corpus.brown
    for w, tag in brown.tagged_words(tagset="universal"):
        if lower:
            w = w.lower()
        if w == word:
            counts.update(tag)
    return counts


def get_all_counts(words, lower=True):
    all_counts = []
    for w in words:
        if lower:
            w = w.lower()
        all_counts.append((w, get_counts(w, lower)))

    return all_counts


class HWChecker(Checker):

    def __init__(self, sid):

        # give the list of modules to import here
        self.modules = ["categories"]
        self.project = "categories"
        super().__init__(sid)

    def script_checker(self):
        """
        to check the output
        make this pass if we didn't print anything by calling the script(s) from
        the command line
        :return:
        """
        terms = ["delight", "murder", "Jump"]
        # correct = get_all_counts(terms, True)
        # not_lowered = get_all_counts(terms, False)
        correct = [('delight', Counter({'NOUN': 27, 'VERB': 2})),
                   ('murder', Counter({'NOUN': 71, 'VERB': 4})),
                   ('jump', Counter({'VERB': 15, 'NOUN': 9}))]
        not_lowered = [('delight', Counter({'NOUN': 27, 'VERB': 2})),
                       ('murder', Counter({'NOUN': 68, 'VERB': 4})),
                       ('jump', Counter({'NOUN': 1}))]
        wrong_tagset = [('delight', Counter({'NN': 27, 'VB': 2})),
                        ('murder', Counter({'NN': 70, 'VB': 4, 'NN-TL': 1})),
                        ('jump', Counter({'VB': 15, 'NN': 9}))]
        wrong_tagset_not_lowered = [('delight', Counter({'NN': 27, 'VB': 2})),
                                    ('murder', Counter({'NN': 68, 'VB': 4})),
                                    ('Jump', Counter({'NN': 1}))]

        correct_sorted = sorted(correct, key=lambda item: item[0])
        not_lowered_sorted = sorted(not_lowered, key=lambda item: item[0])
        wrong_tagset_sorted = sorted(wrong_tagset,
                                                     key=lambda item: item[0])
        wrong_tagset_not_lowered_sorted = sorted(wrong_tagset_not_lowered,
                                                      key=lambda item: item[0])
        # print(correct)
        # print(not_lowered)
        student_output = subprocess.check_output(
            ["python", self.module_file_name(0), "delight", "murder", "Jump"], timeout=100).decode("utf-8")
        student_outputs = []
        lines = student_output.strip().split("\n")

        if len(lines) > 3:
            self.lower_score(2, f"should only print 3 lines, but printed {len(lines)}")
            lines = lines[:4]  # only look at the first 3 lines
        elif len(lines) < 3:
            self.lower_score(2, f"should print 3 lines, but printed {len(lines)}")

        # read in student counts
        for line in lines:
            student_dict = defaultdict(int)
            parts = line.split()
            # print(parts)
            if len(parts) > 0:
                # should look like word tag1 count1 tag2 count2 ...
                word = parts[0].lower()  # in case they counted and printed differently
                tags = parts[1::2]
                counts = parts[2::2]

                for i, s in enumerate(tags):
                    tag = s
                    try:
                        n = counts[i]
                        n = int(n)
                        student_dict[tag] = n

                    except ValueError:
                        self.lower_score(0.5, f"first word of {trunc(line)} should be an int")

                    except Exception:
                        self.lower_score(2, f"can't interpret line {trunc(line)} of output")

                if len(student_dict) > 0:
                    student_outputs.append((word, student_dict))

        # sort the lists so we can be sure we're comparing the same things
        student_outputs_sorted = sorted(student_outputs, key=lambda item: item[0])
        # for pair in student_outputs_sorted:
        #     print(pair[0])
        #     print(pair[1])
        #     print()

        if student_outputs_sorted == not_lowered_sorted:
            self.lower_score(2, "it looks like you forgot to lower case")
        elif student_outputs_sorted == wrong_tagset_sorted:
            self.lower_score(3, "it looks like you used the default tagset")
        elif student_outputs_sorted == wrong_tagset_not_lowered_sorted:
            self.lower_score(4, "it looks like you used the default tagset and forgot to lower case")
        elif student_outputs_sorted != correct_sorted:
            self.lower_score(4, "printed output is incorrect")
        else:
            pass


if __name__ == "__main__":
    student_id = sys.argv[1]
    checker = HWChecker(student_id)
    checker.check()
