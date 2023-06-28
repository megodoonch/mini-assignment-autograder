from collections import Counter
import sys
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
            counts.update([tag])
    return counts


def get_all_counts(words, lower=True):
    all_counts = []
    for w in words:
        if lower:
            w = w.lower()
        all_counts.append((w, get_counts(w, lower)))

    return all_counts


if __name__ ==  "__main__":
    terms = sys.argv[1:]
    counts = get_all_counts(terms, True)
    #print(counts)
    for w, tags in counts:
        print(w, end=" ")
        for tag in tags:
            print(tag, tags[tag], end=" ")
        print()


print("hello world!")