
**File name:** Save your code in a file called `nth.py` and upload it. 

If you haven't successfully submitted a mini-assignment before, please see the instructions in the first post under Assignments. You may also want to watch Mini-Lecture 1.

Write python code that does the following three things:

1. Write a function called `nth_char` that returns (not prints!) the nth character of a string (counting from 0). It should take two arguments, an `int` and a `str`, in that order, and return a single character. If there is no such character, return `None`
For example, `nth_char(2, "hat")` should return `'t'` and `nth_char(3, "hat")` should return `None`

2. Write a function called `nth_word` that returns (not prints!) the nth word of a string (counting from 0). Words are defined as being separated by whitespace, so you can use `.split()`. If there is no such word, return `None`. For example, `nth_word(3,"That's some bad hat, Harry")` should return `"hat,"`.

3. Write a function called `nth_of_mth` that takes three arguments (`int`, `int`, and `str` in that order). It prints (not returns!) `Character <n> of word <m> is <c>` where `<n>` is the first argument, `<m>` is the second argument, and `<c>` is the nth character of the mth word of the third argument.  
If any string is too short, it prints instead `Oops!`. You can use your `nth_char` and `nth_word` functions inside the function.
   
For example, `nth_of_mth(2, 3, "That's some bad hat, Harry")` should print `Character 2 of word 3 is t`.

`nth_of_mth(2, 5, "That's some bad hat, Harry")` should print `Oops!`

You can use the following template to help if you like. Replace `pass` or `None` with your code as needed.

```python

def nth_char(n, string):
    """
    :param n: int: which character to return (0-indexed)
    :param string: str the string to return a character from
    :return str: the nth character of string, or None if there is no such character
    """
    if len(string) > n:     
        pass  # replace pass with your code
        
	
def nth_word(n, string):
    """
    splits string into words on whitespace and returns the nth word
    :param n: int: which word to return (0-indexed)
    :param string: str the string to return a character from
    :return str: the nth word of string, or None if there is no such word
    """
    pass  # replace pass with your code


def nth_of_mth(n, m, string):
    """
    Prints "Character n of word m is c" where c is the nth character of the mth word of string
    :param n : int : which character to print
    :param m : word: which word to print a character from
    :param string: str : the string to print from
    """
    # get the mth word
    word = None  # replace this None with your code
    if word is not None:  # nth_word returns None if there is no such word. 
        # if there is an mth word, find the nth char
        pass  # replace this pass with your code
    else:
        print("Oops!")

```
