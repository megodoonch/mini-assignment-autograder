from checker import *
import sys
import nltk
import pickling


csv_file = "../mini6.csv"

class TagTokens:
    """
    Given an NLTK tagged corpus, and optionally a tagset such as "universal" for Brown,
    stores a dict of tags and the words with those tags.

    Contains methods to return token-based frequencies of pos tags, means, of same,
    and to return words of a given tag

    Attributes:
        pos_dict: a dict from str (pos tags) to sets of strings (words)
    """

    def __init__(self, corpus, tagset=None):
        """
        Given an nltk tagged corpus, builds a dict of pos tags and set of words
        with those tags, storing it as pos_dict.
        If a tagset is given, uses it as the optional `tagset` parameter for
        the corpus's method tagged_words.

        Optional: raise an error if the corpus isn't tagged, or if the tagset
        isn't a tagset of the corpus.

        @param
        corpus: nltk tagged corpus such as nltk.corpus.brown
        """

        if tagset != None:
            tagged_words = corpus.tagged_words(tagset=tagset)
        else:
            tagged_words = corpus.tagged_words()

        self.pos_dict = {}
        for word, tag in tagged_words:
            words = self.pos_dict.get(tag, set())
            words.add(word)
            self.pos_dict[tag] = words

        self.vocab_size = 0
        for tag in self.pos_dict:
            self.vocab_size += len(self.pos_dict[tag])

    def pos_tag_freq(self, tag, rate=False):
        """
        Returns the token frequency of a pos tag in the corpus
        @param
        tag: str, a pos tag such as "VERB"
        @return int
        """
        if rate:
            denominator = self.vocab_size
        else:
            denominator = 1
        if tag in self.pos_dict:
            return len(self.pos_dict[tag]) / denominator
        else:
            return 0

    def average(self, tag_list, rate=False):
        """
        Given a list of tags in the tagset, return the average token frequencies
        of those tags

        @param
        tag_list: str list
        @return
        """
        sum_freqs = 0
        for tag in tag_list:
            sum_freqs += self.pos_tag_freq(tag, rate)

        return sum_freqs / len(tag_list)

    def examples(self, tag, n=1):
        """
        Return a list of n arbitrary words with the given tag.
        You can choose those n words any way you want.

        @param
        tag: str
        n: int, default 1
        """
        return list(self.pos_dict[tag])[:n]



class HW6Checker(Checker):

    def __init__(self, sid):
        super().__init__(sid)

        # give the list of modules to import here
        self.modules = ["tagtypes"]
        self.tokens = pickling.load(open("../universal_brown.pickle", "rb"))

    def script_checker(self):
        """
        to check the output
        make this pass if we didn't print anything by calling the script(s) from
        the command line
        :return:
        """
        with open(self.out_file, 'r') as output:
            line1 = output.readline().strip("\n")
            if not (line1.lower().startswith("lexical: 14168") or
                    line1.lower().startswith("lexical: 0.2362")):

                self.lower_score(1,
                    "should print 'lexical: 14168' or lexical: 0.2362, but instead it prints {}".format(
                        line1))
            line2 = output.readline().strip("\n")
            if not (line2.lower().startswith("functional: 0.0028") or
                    line2.lower().startswith("functional: 170")):
                self.lower_score(1,
                                 "should print 'functional: 170' or functional: 0.0028, but instead it prints {}".format(
                                     line2))

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
        for m in self.modules:
            f = "{}-{}".format(self.sid, m)
            if m == "tagtypes":

                # import sid-hello.py
                mod = importlib.import_module(f)

                try:
                    brown_universal = mod.TagTypes(nltk.corpus.brown, "universal")
                    try:
                        if not type(brown_universal.pos_dict) == dict:
                            self.lower_score(1,
                                             "self.pos_dict should be a dict but is a {}".format(
                                                 type(brown_universal.pos_dict)))
                    except Exception as e:

                        self.lower_score(2,
                                         "self.pos_dict failed with exception '{}'".format(
                                             e))
                    try:
                        if not (brown_universal.pos_tag_freq("VERB") == self.tokens.pos_tag_freq("VERB") or
                        brown_universal.pos_tag_freq("VERB") == self.tokens.pos_tag_freq("VERB", True)):
                            self.lower_score(1, "pos tag freq of VERB should be {} or {} but is {}".format(
                                self.tokens.pos_tag_freq("VERB"),
                            self.tokens.pos_tag_freq("VERB", True),
                            brown_universal.pos_tag_freq("VERB")))
                    except Exception as e:
                        self.lower_score(2,
                                         "self.pos_tag_freq('VERB') failed with exception '{}'".format(
                                             e))

                    try:
                        tags = ["VERB", "NOUN"]
                        av = brown_universal.average(tags)
                        if not (av == self.tokens.average(tags)
                                or av == self.tokens.average(tags, True)):
                            self.lower_score(1,
                                             "average([VERB, NOUN]) should be {} or {} but is {}".format(
                                                 self.tokens.average(tags),
                                                 self.tokens.average(tags, True),
                                                 av ))
                    except Exception as e:
                        self.lower_score(2, "average failed with exception {}".format(e))

                    try:
                        if not (type(brown_universal.examples("NOUN", 2) == list or type(brown_universal.examples("NOUN")[0] == str))):
                            self.lower_score(1, "examples should return list of strings")
                    except Exception as e:
                        self.lower_score(2, "examples('NOUN', 2) failed with exception {}".format(e))


                except Exception as e:
                    self.lower_score(5, "instantiating TagTypes failed with exception {}".format(e))

                try:
                    brown_default = mod.TagTypes(nltk.corpus.brown)
                except Exception as e:
                    self.lower_score(2, "TagTypes(nltk.corpus.brown) failed with exception {}".format(e))



if __name__ == "__main__":
    import csv
    sid = sys.argv[1]
    checker = HW6Checker(sid)
    checker.check()
    print(sid, checker.grade, checker.comments)
    with open(csv_file, 'a') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerow([sid, checker.grade, checker.comments])