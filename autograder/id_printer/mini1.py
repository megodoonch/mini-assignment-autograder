from checker import *
import sys

csv = "mini1.csv"

class HW1(Checker):

    def __init__(self, sid):
        """

        :param sid: string of student ID
        """
        super().__init__(sid)
        self.modules = ["id_printer"]

    def script_checker(self):
        """
        to check the output
        make this pass if we didn't print anything by calling the module(s) from
        the command line
        :return:
        """
        with open(self.out_file, 'r') as output:
            line = output.readline()
            if not line.lower().startswith("my student number is {}".format(self.sid)):
                self.grade -= 1
                self.add_comment(
                    "(-1) should print 'my student number is {}', but instead it prints {}".
                        format(self.sid, line.strip()))

            line = output.readline().strip('\n')
            if not (line == str(self.sid[4]) or line == str(self.sid[3])):
                self.grade -= 1
                self.add_comment("(-1) should print {} but printed {}".format(self.sid[4], line))

            line = output.readline()
            if not (line is None or line.strip() == ""):
                self.add_comment("(-1) extra line of print")
                self.grade -= 1

            # line = output.readline()
            # id_string = str(self.sid)
            # fourth = id_string[3]
            # if not line.lower().startswith('the fourth digit of my student number is {}'.format(fourth)):
            #     self.grade -= 2
            #     self.add_comment(
            #         "should print 'the fourth digit of my student number is {}', but instead it prints {}".
            #             format(fourth, line.strip()))

    def module_output_checker(self):
        """
        make sure it prints nothing when imported
        :return:
        """
        with open(self.module_out_file, 'r') as output:
            text = output.read().strip("\n").strip()
            if not (text is None or len(text) == 0):
                self.lower_score(2, "importing module shouldn't print anything but it prints {}".format(text))

    def module_checker(self):
        """
        checks id_printer
        :return:
        """

        for m in self.modules:
            f = "{}-{}".format(self.sid, m)
            if m == "id_printer":

                # import sid-id_printer.py
                id_printer = importlib.import_module(f)

                # check variables etc
                try:
                    id = id_printer.my_id
                    if id == str(self.sid):
                        self.grade -= 1
                        self.add_comment("(-1) my_id should be of type int but it is of type str")
                    elif id == int(self.sid):
                        pass
                    else:
                        self.grade -= 2
                        self.add_comment(
                            "(-2) my_id should be {} of type int but it is {} of type {}".format(self.sid, id, type(id)))

                except Exception as e:
                    self.grade -= 3  # lose 3 for not useable
                    self.add_comment(
                        "(-3) my_id failed with exception '{}'".format(e))

                try:
                    if id_printer.nth(0, int(self.sid)) == str(self.sid)[0]:
                        self.grade -= 1
                        self.add_comment("(-1) close: nth returns a string but should return an int")

                    elif id_printer.nth(0, int(self.sid)) == int(str(self.sid)[0]):
                        pass

                    else:
                        self.grade -= 2
                        print("Here!")
                        self.add_comment("(-2) nth(0, {}) should return {} but returns {} instead".format(
                            self.sid,
                            str(self.sid)[0],
                            id_printer.nth(0, self.sid)))


                except Exception as e:
                    self.grade -= 3  # lose 3 for not useable
                    self.add_comment(
                        "(-3) nth() failed with exception '{}'".format(e))



if __name__ == "__main__":
    sid = sys.argv[1]
    checker = HW1(sid)
    checker.check()
    print(sid, checker.grade, checker.comments)
    with open(csv, 'a') as csv:
        # print results to csv
        csv.write("{},{},{}\n".format(sid, checker.grade, checker.comments))

