## Mini-assignment

**Filename** `alice.py`

Write a script that will use NLTK's Gutenberg plaintext corpus `"carroll-alice.txt"` to find the five most common words that directly follow the word `"Alice"` in Alice in Wonderland. 

When run as a script, it should print, in decreasing order of frequency, each word and its count on its own line, separated by a space, like this:

	
	laughed 29
	sang 24
	i 10
	slept 2
	spoke 2
	

If two words have the same frequency, either order is fine.

Use the `words()` method of the NLTK corpus. This will get you an iterable over words in the text that crosses sentence boundaries, so if a sentence ends with `Alice`, the first word of the next sentence counts as a word that follows `Alice`. 

Treat words as case-**in**sensitive. That is, `The`, `THE`, and `the` count as the same word, and same with `ALICE`, `Alice`, etc.

Skip over words that consist entirely of punctuation marks, so in `Alice, the hare, and the hatter`, `the` follows `Alice`, even though there's an intervening comma. I recommend a list comprehension with regular expressions to remove all punctuation from the corpus, e.g.:

`words = [w.lower() for w in words if re.search(r'\w', w)]`


If imported as a module, your script shouldn't print anything or read or write any files. It may import modules, or define functions or classes, but not run them.


Save it as `alice.py`.
