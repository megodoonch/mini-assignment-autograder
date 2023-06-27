import re, random
from collections import Counter
from nltk.corpus import gutenberg


if __name__ == "__main__":
    words = gutenberg.words("carroll-alice.txt")
    words = [w.lower() for w in words if re.search(r'\w', w)] # 0 correct
    #words = [w for w in words if re.search(r'\w', w)]         # 1 no lower

    # 2 removed punct too late
    # words = [w.lower() for w in words]
    #successors = [words[i+1] for i, w in enumerate(words) if w.lower() == "alice" and re.search(r'\w', words[i+1])]

    # for cases 0,1,3
    successors = [words[i + 1] for i, w in enumerate(words) if w.lower() == "alice"]
    #successors = [words[i + 1].lower() for i, w in enumerate(words) if w == "Alice"]
    #successors = [words[i + 1] for i, w in enumerate(words) if w == "Alice"]

    # make a counter with these words
    counts = Counter(successors)

    to_print = counts.most_common(10)
    #print(to_print)

    # random.shuffle(to_print)
    for word, count in to_print[:5]:
        print(word, count)
    # print("Hi", 20)
    # print("there", 17)
    # print("Teddy", 16)
    # print("Bear", 12)
    # print("!", 12)

