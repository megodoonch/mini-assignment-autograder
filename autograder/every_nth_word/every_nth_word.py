from checker import *
import sys

csv_file = "every_nth_word.csv"

d = """DENNIS: Listen -- strange women lying in 
    ponds distributin' swords is no basis for a system of
    government.  Supreme executive power derives from a mandate 
    from the masses, not from some farcical aquatic ceremony.

ARTHUR: Be quiet!

DENNIS: Well you can't expect to wield supreme executive power
    just 'cause some watery tart threw a sword at you!

ARTHUR: Shut up! 
DENNIS: HELP! HELP! I'm being repressed!"""


def every_nth(s, n=1):
    """
    given a string, returns a string made up of every nth word, separated by a space
    splits the original string along any whitespace
    :param s: string
    :param n: int, default 1
    :return: string
    """
    return " ".join(s.split()[::n])


def chars():
    dennis = []
    arthur = []
    other = []
    speaker = other
    for w in d.split():
        if w == "DENNIS:":
            speaker = dennis
        elif w == "ARTHUR:":
            speaker = arthur
        else:
            speaker.append(w)

    return " ".join(arthur), " ".join(dennis)



class HW2(Checker):

    def __init__(self, sid):
        super().__init__(sid)

        # give the list of modules to import here
        self.modules = ["dialog"]

    def module_output_checker(self):
        pass

    def script_checker(self):
        """
        to check the output
        make this pass if we didn't print anything by calling the module(s) from
        the command line
        :return:
        """
        with open(self.out_file, 'r') as output:
            line = output.readline().strip('\n')
            if line != d.split()[10]:
                self.grade -= 1
                self.add_comment(
                    "should print {}, but instead it prints {}".format(
                        d.split()[10], line))
            line = output.readline().strip('\n')
            if line != d[10]:
                self.grade -= 1
                self.add_comment(
                    "should print {}, but instead it prints {}".format(d[10],
                                                                       line))
            line = output.readline()
            if not (line == "" or line is None):
                self.grade -= 1
                self.add_comment("(-1) extra line printed")

    def module_checker(self):
        for m in self.modules:
            f = "{}-{}".format(self.sid, m)
            if m == "dialog":

                # import sid-dialog
                dialog = importlib.import_module(f)

                # check variables etc
                try:
                    strings = ["hello world!", """Hello world!
                    hello     hello    hello!""", d]
                    print(strings)
                    for s in strings:
                        print(s)
                        l = dialog.every_nth(s, 2)
                        print(l)
                        if l != every_nth(s, 2):
                            self.grade -= 1
                            self.add_comment("(-1) every_nth('{}', 2) should be {}, but it is {}".format(s, every_nth(s, 2), l))


                except Exception as e:
                    self.grade -= 3  # lose 3 for not useable
                    self.add_comment(
                        "(-3) every_nth failed with exception '{}'".format(e))

                # if function prints to sout, redirect it to the output file.
                try:
                    # direct stout to a file
                    output = open(self.out_file, 'w')
                    orig_stdout = sys.stdout
                    sys.stdout = output

                    # run the function that will print
                    dialog.characters("A")

                    # put stout back to normal
                    sys.stdout = orig_stdout
                    output.close()

                    # read file back in and check it's right

                    with open(self.out_file, 'r') as f:
                        l = f.read().replace("\n", " ")
                        if l.split() != chars()[0].split():
                            self.add_comment(
                                "(-1) characters('A') should print {}, but printed {}".
                                    format(chars()[0], l))

                            self.grade -= 1

                except Exception as e:
                    self.grade -= 3  # lose 3 for not useable
                    self.add_comment(
                        "(-3) characters('A') failed with exception '{}'".format(e))

                try:
                    # direct stout to a file
                    output = open(self.out_file, 'w')
                    orig_stdout = sys.stdout
                    sys.stdout = output

                    # run the function that will print
                    dialog.characters("D")

                    # put stout back to normal
                    sys.stdout = orig_stdout
                    output.close()

                    # read file back in and check it's right

                    with open(self.out_file, 'r') as f:
                        l = f.read().replace("\n", " ")
                        if l.split() != chars()[1].split():
                            self.add_comment(
                                "(-1) characters('D') should print {}, but printed {}".
                                    format(chars()[1], l))

                            self.grade -= 1

                except Exception as e:
                    self.grade -= 3  # lose 3 for not useable
                    self.add_comment(
                        "(-3) characters('D') failed with exception '{}'".format(e))


if __name__ == "__main__":
    import csv
    sid = sys.argv[1]
    checker = HW2(sid)
    checker.check()
    with open(csv_file, 'a') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerow([sid, checker.grade, checker.comments])