dialog = """DENNIS: [interrupting] Listen -- strange women lying in 
        ponds distributin' swords is no basis for a system of
        government.  Supreme executive power derives from a mandate 
        from the masses, not from some farcical aquatic ceremony.
        
        
ARTHUR: Be quiet!
DENNIS: Well you can't expect to wield supreme executive power
        just 'cause some watery tart threw a sword at you!
ARTHUR: Shut up! 
        [...]
DENNIS: HELP! HELP! I'm being repressed!"""

strings = ["hello world!", """Hello world!
                    hello     hello    hello!""", dialog]

print(dialog[10])

def every_nth(s, n=1):
    """
    given a string, returns a string made up of every nth word, separated by a space
    splits the original string along any whitespace
    :param s: string
    :param n: int, default 1
    :return: string
    """
    return " ".join(s.split()[::n])

print(every_nth(dialog, 10))

d = dialog.split()

print(d[10])

dennis = []
arthur = []
other = []
speaker = other
for w in d:
    if w == "DENNIS:":
        speaker = dennis
    elif w == "ARTHUR:":
        speaker = arthur
    else:
        speaker.append(w)

print(" ".join(arthur))
print(" ".join(dennis))

