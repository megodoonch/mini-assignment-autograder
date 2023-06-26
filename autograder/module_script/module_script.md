# Mini-Assignment 3

**File name:** Save your code in a file called `module_script.py` and upload it. 

If you haven't successfully submitted a mini-assignment before, you may also want to watch Mini-Lecture 1, but keep in mind you'll probably find it easier just to work straight from Spyder now that you're familiar with it.

Remember to name and print everything exactly as instructed, including case.

Write python code that does the following things:

1. Stores the string `"hello world!"` in variable `message`
2. Prints the exact contents of `message` if and only if the file is run as a script
3. Doesn't do anything (except provide the definition of `message`) when imported as a module

This means you need to protect your print statement with an `if __name__ == "__main__"`. If you run your script from the command line, it should print `hello world!`: 

```bash 

$ python module_script.py
hello world!
```

and if you import it into another python file or in an IPython console in Spyder, it shouldn't print anything:

```python 

import module_script
```

Save your code in a file called `module_script.py` and upload it. 