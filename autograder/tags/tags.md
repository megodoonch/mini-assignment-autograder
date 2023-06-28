# Mini-Assignment 6

**Filename:** `tag_types.py`

Complete the following class `TagTypes` by implementing the descriptions in the docstrings. Feel free to update the docstrings if you want to.  Save the code in a **Python** file called `tag_types.py`

When the file is called as a script -- but not when it is imported as a module -- it should also do the following.

1. Create an instance of a the TagTypes class with corpus `nltk.corpus.brown` and tagset `"universal"`
2. The Universal tagset is small. Make two lists of pos tags, `lexical` and `functional` out of the Universal tag set. **Do not** include `x` or `.` or `NUM` in your lists. Use what you have learned about linguistics to correctly categorise the tags. You can ask your classmates for help if this is unfamiliar.
3. Print out the mean frequencies of your lexical and functional sets. For example, if the means of both sets were 200.0, you would print:

		lexical: 200.0
		functional: 200.0
	
You should actually find a large difference, which, using your knowledge of linguistics, should help you figure out if you divided the tags up right. (Food for thought: which is NUM most similar to? Does that help you decide how if would be classified if you were to include it?)




		class TagTokens:
		    """
		    Given an NLTK tagged corpus, and optionally a tagset such as "universal",
		     stores a dict of tags and the words with those tags.
		
		    Contains methods to return token-based frequencies of pos tags, means, of same, 
		    and to return words of a given tag
		
		    Attributes:
		        pos_dict: a dict from str (pos tags) to sets of strings (words)
		    """
		    def __init__(self, corpus, tagset=None):
		        """
		        Given an nltk tagged corpus, builds a dict of pos tags and set of words
		        with those tags, storing it as pos_dict.
		        If a tagset is given, uses it as the optional `tagset` parameter for
		        the corpus's method tagged_words. Otherwise it uses the default tagset.
		        
		        Optional: raise an error if the corpus isn't tagged, or if the tagset 
		        isn't a tagset of the corpus.
		        
		        @param
		        corpus: nltk tagged corpus such as nltk.corpus.brown
		        tagset: str (a special tagset) default None (meaning the default tagset)
		        """
		        # TODO
		        pass
		            
		    def pos_tag_freq(self, tag):
		        """
		        Returns the token frequency of a pos tag in the corpus
		        @param
		        tag: str, a pos tag such as "VERB"
		        @return int
		        """
		        # TODO
		        pass
		        
		        
		    def average(self, tag_list):
		        """
		        Given a list of tags in the tagset, return the average token frequencies
		        of those tags
		        
		        @param
		        tag_list: str list
		        @return float
		        """
		        # TODO
		        pass
		    
		    def examples(self, tag, n=1):
		        """
		        Return a list of n arbitrary words with the given tag. 
		        You can choose those n words any way you want.
		        
		        @param
		        tag: str
		        n: int, default 1
		        """
		        # TODO
		        pass
	
	    