#!/usr/bin/python3

__author__ = "Author"
__copyright__ = "Copyright 2016, Author"
__license__ = "TODO"


CIPHERTEXT = 'HOOJILEQKCYJN'


def main():

    l = len(CIPHERTEXT)
    w = []

    with open("/home/christoph/Downloads/german.dic", encoding="ISO-8859-1") as f:
        content = f.readlines()

    for o in content:
        # newline is counted!
        if len(o) < l:
            w.append(o)

    with open("/home/christoph/workspace/words.dic", 'w') as outfile:
        for word in w:
            outfile.write("%s" % word)

if __name__ == "__main__":
    main()



