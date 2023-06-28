# Mini-Assignment 6

**Filename:** `pickles.py`

In this assignment you will pickle and unpickle an instance of a `TagTypes` object. The module `type_counter` that provides the `TagTypes` class is given in the attached file, `type_counter.py`. Do not modify it or hand it in; just hand in `pickles.py`.

`TagTypes` finds the type-based frequencies of tags in a tagged corpus and stores them in a dict. Because it can take a while to build such a dict from a large corpus, it can be helpful to build it once and then pickle it for later use. In this assignment, you'll write code that pickles and unpickles a `TagTypes` object.

Specifically, you will write a second module, `pickles`, which imports `TagTypes` and provides two functions and a script section as follows:

1. function `make_and_pickle` takes two required and one optional argument, in this order:
   
    a. A tagged NLTK corpus such as `nltk.corpus.brown` or `nltk.corpus.conll2000`
   
    b. The path to the file you'll store the pickle in, e.g. `"my_pickle.pickle"` (type `str`)

    c. Optional argument called `tagset`: the name of the tagset to pass to the `TagTypes` initialiser. Its default value should be `None`.
 
    `make_and_pickle` initialises a `TagTypes` object with the given corpus and tagset, pickles it, and stores the pickle as the filename given.

    For example,

   ```python
   make_and_pickle(nltk.corpus.brown, "my_pickle.pickle", tagset="universal")
   ``` 

    creates an instance of `TagTypes` with `nltk.corpus.brown` and optional argument `tagset="universal"` and stores the pickle in `my_pickle.pickle`. 

2. function `unpickle` takes one argument, the path to the pickle to be loaded.  It loads the given pickle and `return`s (not prints!) the unpickled `TagTypes` object.

3. **Only** when run as a script, the module should use its command line arguments to pickle or unpickle a `TagTypes` object. Specifically:

```commandline
python pickles.py --unpickle path/to/picklefile.pickle
```

uses `unpickle` to load the pickle in the path given, and print it. `TagTypes` has a `__repr__` method, so you should just print the object directly.

```commandline
python pickles.py --pickle path/to/picklefile.pickle
```
uses `make_and_pickle` to initialise a `TagTypes` object with `nltk.corpus.conll2000` as the corpus and `tagset="universal"`. It stores the pickle in the path given.

If the wrong number of command line arguments are given, it should print a message.

For reference, here is the contents of `type_counter.py`:

```python
from collections import defaultdict, Counter


class TagTypes:
    """
    Given an NLTK tagged corpus, and optionally a tagset such as "universal"
     for Brown, stores a dict of tags and the words with those tags.

    Attributes:
        pos_dict: a dict from str (pos tags) to sets of strings (words)
        counts: a counter for the pos tags
    """

    def __init__(self, corpus, tagset=None):
        """
        Given an nltk tagged corpus, builds a dict of pos tags and set of words
        with those tags, storing it as pos_dict.
        If a tagset is given, uses it as the optional `tagset` parameter for
        the corpus's method tagged_words.

        :param corpus: nltk tagged corpus such as nltk.corpus.brown
        :param tagset: str: Optional. The name of the tagset; if None,
         the default is used.
        """
        if tagset is not None:
            tagged_words = corpus.tagged_words(tagset=tagset)
        else:
            tagged_words = corpus.tagged_words()

        # we use a set because we want types, not tokens (no duplicates!)
        self.pos_dict = defaultdict(set)
        for word, tag in tagged_words:
            word = word.lower()
            self.pos_dict[tag].add(word)  # case insensitive

        # store the counts too
        self.counts = Counter(dict([(k, len(self.pos_dict[k]))
                                    for k in self.pos_dict]))

    def __repr__(self):
        """
        catgories and their raw frequencies in alphabetical order
        :return string representation of the object
        """
        return "\n".join([f"{tag} {self.counts[tag]} types"
                          for tag in sorted(self.counts)])

    def __eq__(self, other):
        """
        equality for two TagTypes object because pickle doesn't think
         the round trip should work
        :param other: TagTypes
        :return: bool
        """
        return self.pos_dict == other.pos_dict and self.counts == other.counts

    def examples(self, tag, n=1):
        """
        Return a list of n words with the given tag.
        :param tag: str
        :param n: int, default 1
        :return string list
        """
        return list(self.pos_dict[tag])[:n]

```