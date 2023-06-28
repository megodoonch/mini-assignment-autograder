import nltk
from collections import defaultdict


class TagTypes:
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

        Bonus: raise an error if the corpus isn't tagged, or if the tagset
        isn't a tagset of the corpus.

        @param
        corpus: nltk tagged corpus such as nltk.corpus.brown
        """

        if tagset is not None:

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
        @return float
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


if __name__ == "__main__":
    universal_tokens = TagTypes(nltk.corpus.brown, "universal")
    lexical = ["NOUN", "VERB", "ADJ", "ADV"]
    functional = ["PRT", "ADP", "PRON", "DET", "CONJ"]

    lex = universal_tokens.average(lexical)
    fun = universal_tokens.average(functional)

    print("lexical:", lex)
    print("functional:", fun)
    # print("NUM:", universal_tokens.pos_tag_freq("NUM"))

    lex = universal_tokens.average(lexical, True)
    fun = universal_tokens.average(functional, True)

    print("lexical:", lex)
    print("functional:", fun)
    # print("NUM:", universal_tokens.pos_tag_freq("NUM", True))

    # pickle.dump(TagTokens(nltk.corpus.brown, "universal"), open("universal_brown.pickle", "wb"))

