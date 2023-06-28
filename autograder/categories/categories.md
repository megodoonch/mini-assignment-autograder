# Mini-assignment 5

**Filename:** `categories.py`

Use the NLTK Brown tagged corpus (as in the Tagged Corpora practicum) for this assignment. The task is to write a script that, **only when run as a script**, takes a list of words from the command line, and prints the frequencies of their tags from the `universal` tagset. 

Specifically:

* treat all words as case-insensitive (use `.lower()` everywhere)

* use the `universal` tagset (specify `tagset="universal"`; this isn't the default tagset)

* the script takes one or more command-line arguments. Each argument is a word. You should be able to run it like this:

```
python categories.py run diet kiss
```

* For each word, on its own line, print the word followed by each tag and its count. Separate the tags and counts with a space, just like in the following example:


```

run VERB 157 NOUN 55 
diet NOUN 21 
kiss NOUN 8 VERB 9 
```

These are correct counts; you can compare them with your output. It doesn't matter what order the lines or categories come out
in, but make sure you print word followed by each category followed by its count, as shown. e.g. this is fine too:

```

diet NOUN 21 
kiss NOUN 8 VERB 9 
run  NOUN 55 VERB 157
```





You can expect your code to take a few seconds to finish.

 (Hint 1: you might use `Counter()` from `collections`)
 
(Hint 2: you can get the command line arguments as a list of strings with `sys.argv[1:]`)

