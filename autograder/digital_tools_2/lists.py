sentence = "I love Lucy"

words_1 = sentence.split()
words_2 = sentence.split()
words_3 = words_1

words_1.append("very")
words_1.append("much")

equal_1_2 = words_1 == words_2
equal_1_3 = words_1 == words_3

print(equal_1_2)
print(equal_1_3)
