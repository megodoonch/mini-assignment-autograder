def nth_char(n, string):
    """
    :param n: int: which character to return (0-indexed)
    :param string: str the string to return a character from
    :return str: the nth character of string
    """
    if len(string) <= n:
        return None
    else:
        return string[n]  # replace pass with your code


def nth_word(n, string):
    """
    splits string into words on whitespace and returns the nth word
    :param n: int: which word to return (0-indexed)
    :param string: str the string to return a character from
    :return str: the nth word of string
    """
    as_list = string.split()
    if len(as_list) > n:
        return as_list[n]  # replace pass with your code


def nth_of_mth(n, m, string):
    """
    Prints "Character n of word m is c" where c is the nth character of the mth word of string
    :param n : int : which character to print
    :param m : word: which word to print a character from
    :param string: str : the string to print from
    """
    # get the mth word
    word = nth_word(m, string)
    if word is not None:  # if there is an mth word, find the nth char
        char = nth_char(n, word)
        if char is not None:
            print(f"Character {n} of word {m} is {char}")
        else:
            print("Oops!")
    else:
        print("Oops!")


# print(len("hello"))
# print(nth_char(4, "hello"))
# print(nth_word(3, "Hi there, Jonas"))
# nth_of_mth(1,2,"Hi there, Jonas")
# nth_of_mth(2,3,"That's     some bad hat, Harry")
# nth_of_mth(2,5,"That's some bad hat, Harry")
# print(nth_char(2, "hat"))
