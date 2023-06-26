from checker import *


class HWChecker(Checker):

    def __init__(self, sid):
        super().__init__(sid)

        # give the list of modules to import here
        self.modules = ["nth"]
        self.project = "nth"

    def module_checker(self):

        mod = importlib.import_module(f"{self.sid}-{self.modules[0]}")

        # check variables etc
        try:
            u = mod.nth_char(2, "squidgy")
            if u != "u":
                self.lower_score(1, f"nth_char(2, 'squidgy') should be 'u' but it is '{trunc(u)}'")

        except Exception as e:

            self.lower_score(2,
                             "nth_char(2, 'squidgy') failed with exception '{}'".format(e))

        try:
            none = mod.nth_char(10, "squidgy")
            if none is not None:
                self.lower_score(1, f"nth_char(10, 'squidgy') should be None but it is '{none}'")

        except Exception as e:

            self.lower_score(2,
                             "nth_char(10, 'squidgy') failed with exception '{}'".format(e))

        try:
            so = mod.nth_word(1, "That's so silly!")
            if so != "so":
                self.lower_score(1, f"nth_word(1, 'That's so silly!') should be 'so' but it is '{trunc(so)}'")

        except Exception as e:

            self.lower_score(2,
                             "nth_word(1, 'That's so silly!') failed with exception '{}'".format(e))

        try:
            none = mod.nth_word(10, "That's so silly!")
            if none is not None:
                self.lower_score(1, f"nth_word(10, 'That's so silly!') should be None but it is '{none}'")

        except Exception as e:

            self.lower_score(2,
                             "nth_word(10, 'That's so silly!') failed with exception '{}'".format(e))

        # if function prints to sout, redirect it to the output file.

        try:
            # direct stout to a file
            output = open(self.out_file, 'w')
            orig_stdout = sys.stdout
            sys.stdout = output

            # run the function that will print
            mod.nth_of_mth(2, 2, "That's so silly!")
            mod.nth_of_mth(3, 2, "That's so silly!")

            # put stout back to normal
            sys.stdout = orig_stdout
            output.close()

            # read file back in and check it's right

            with open(self.out_file, 'r') as f:
                l = f.readline().strip("\n")
                if l != "Character 2 of word 2 is l" and l != "Character 2 of word 2 is \'l\'" \
                        and l != "Character 2 of word 2 is \"l\"":
                    self.lower_score(1,
                                     "should print Character 2 of word 2 is l, but printed {}".
                                     format(l))
                l = f.readline().strip("\n")
                if l != "Character 3 of word 2 is l" and l != "Character 3 of word 2 is \'l\'"\
                        and l != "Character 3 of word 2 is \"l\"":
                    self.lower_score(1,
                                     f"should print 'Character 3 of word 2 is l', but printed '{l}'")

        except Exception as e:
            self.lower_score(2,
                             "nth_of_mth failed with exception '{}'".format(e))

        # print "Oops!"
        try:
            # direct stout to a file
            output = open(self.out_file, 'w')
            orig_stdout = sys.stdout
            sys.stdout = output

            # run the function that will print
            mod.nth_of_mth(12, 2, "That's so silly!")
            mod.nth_of_mth(2, 12, "That's so silly!")
            mod.nth_of_mth(12, 12, "That's so silly!")

            # put stout back to normal
            sys.stdout = orig_stdout
            output.close()

            # read file back in and check it's right

            with open(self.out_file, 'r') as f:
                l = f.readline().strip("\n")
                l = trunc(l)
                if l == "oops" or l == "Oops" or l == "oops!":
                    self.lower_score(0.5,
                                     f"nth_of_mth(12, 2, 'That's so silly!') should print 'Oops!', but printed '{l}'")
                elif l != "Oops!":
                    self.lower_score(1,
                                     f"nth_of_mth(12, 2, 'That's so silly!') should print 'Oops!', but printed '{l}'")

                l = f.readline().strip("\n")
                l = trunc(l)
                if l == "oops" or l == "Oops" or l == "oops!":
                    self.lower_score(0.5,
                                     f"nth_of_mth(2, 12, 'That's so silly!') should print 'Oops!', but printed '{l}'")
                elif l != "Oops!":
                    self.lower_score(1,
                                     f"nth_of_mth(2, 12, 'That's so silly!') should print 'Oops!', but printed '{l}'")

                l = f.readline().strip("\n")
                l = trunc(l)
                if l == "oops" or l == "Oops" or l == "oops!":
                    self.lower_score(0.5,
                                     f"nth_of_mth(12, 12, 'That's so silly!') should print 'Oops!', but printed '{l}'")
                elif l != "Oops!":
                    self.lower_score(1,
                                     f"nth_of_mth(12, 12, 'That's so silly!') should print 'Oops!', but printed '{l}'")

        except Exception as e:
            self.lower_score(2,
                             "nth_of_mth failed with exception '{}'".format(e))


if __name__ == "__main__":
    sid = sys.argv[1]
    checker = HWChecker(sid)
    checker.check()
