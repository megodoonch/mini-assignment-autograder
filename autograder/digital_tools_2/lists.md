File name: **lists.py**

Make a python file that does the following:

1. Stores the string `"I love Lucy"` in a variable called `sentence`
2. Splits `sentence` using the `split` method for strings, and stores the resulting list of words in the variable `words_1`
3. Does (2) again, but this time stores the result in `words_2`
4. Sets `words_3` equal to `words_1` using `words_3 = words_1`
5. Uses the `append` method for lists to append `"very"` and `"much"` to `words_1`
6. Checks whether `words_1` and `words_2` are equal, storing the result in `equal_1_2`. (So the value of `equal_1_2` should be either `True` or `False`.)
7. Does the same for `words_1` and `words_3`, storing the result in `equal_1_3`

See if you can reason through the result you got. Python can be a bit weird with the way it stores things in variables, and this can lead to errors. (You don't need to write anything in the assignment about this; the autograder won't see it.)

Make sure you do steps (3) and (4) differently. Steps (2) and (3) should look almost the same, and (4) totally different.

Don't print anything in the version you hand in. It should just do the splitting and appending and checking. However, you'll probably want to print things out while you're working on the code. Just don't include that part in the code you hand in.

Remember to name everything exactly as requested. I suggest you copy and paste from this assignment.

If you want, you can use this code to help you get started.

```python
sentence = # this should be the "I love Lucy" string

# get the words
words_1 =  # this should be a list of strings
words_2 =  # ditto
words_3 =  # ditto

# now append to words_1

# check equality
# you might want to use if/then statements, but there are other ways too.

equal_1_2 =  # this should end up being True or False, but don't just write True or False! 

equal_1_3 =  # ditto
```

Remember to export your Jupyter Notebook to a Python file (use Download as...) or copy and paste into a python file in Spyder or VSCode or something similar. Don't hand in a Jupyter Notebook; it's the wrong kind of file. Name the file `lists.py`.