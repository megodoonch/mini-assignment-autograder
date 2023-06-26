import nltk
from collections import Counter, defaultdict

from nltk.corpus import gutenberg

from string import punctuation


def after_alice(better, lower, lower_alice):
    words = gutenberg.words("carroll-alice.txt")
    if better:
        words = [word for word in words if not all(i in punctuation for i in word)]
    if lower:
        new_words = []
        for w in words:
            if w.lower() == "alice":
                new_words.append(w)
            else:
                new_words.append(w.lower())
        words = new_words
    if lower_alice:
        new_words = []
        for w in words:
            if w.lower() != "alice":
                new_words.append(w)
            else:
                new_words.append(w.lower())
        words = new_words
        alice = "alice"
    else:
        alice = "Alice"
    if len(words) == 0:
        print("uh oh! words", better, lower, lower_alice)
    nexts = [words[i+1] for i, w in enumerate(words) if i < len(words) - 1 and w == alice] # and not all(letter in punctuation for letter in words[i+1])]
    if len(nexts) == 0:
        print("uh oh! nexts", better, lower, lower_alice)
    return Counter(nexts)


def make_all_solutions():
    # make all solutions, modulo ordering, cutting off at 5, and printing
    lijstje = []
    for b in [True, False]:
        for l in [True, False]:
            for la in [True, False]:
                lijstje.append(([b, l, la], after_alice(b, l, la)))

    # keep all dicts we've made in these different ways
    all_dicts = []
    for features, d in lijstje:
        # make a dict from count to sets of words with that count
        d_inverse = defaultdict(set)
        for w, c in d.most_common(10):
            d_inverse[c].add(w)

        # cut it off when we've got enough sets of words to get to 5 words
        out_dict = defaultdict(set)
        for n in d_inverse:
            if sum([len(out_dict[k]) for k in out_dict]) < 5:
                out_dict[n] = d_inverse[n]

        # some of them have the same results
        if out_dict not in all_dicts:
            all_dicts.append(out_dict)

    print("All Dicts")
    for d in all_dicts:
        print(d)
    return all_dicts


if __name__ == "__main__":
    results = after_alice(True, True, False)
    results = results.most_common(10)
    # results.reverse()
    for w, count in results:
        print(w, count)




"""
and 20
was 17
i 16
s 12
thought 12
had 11
as 11
said 11
could 11
did 10
"""


