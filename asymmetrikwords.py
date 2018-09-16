import re

# Class to hold a tree of letters that represent all of the paths words can take
class WordTree():
    def __init__(self, letter):
        # The letter at this node. Not actually necessary but nice to have
        self.letter = letter

        # A dictionary (effectively a hash) of all of the subtrees, indexed by
        # the letter that they represent
        self.children = {}

    # Base method that gets the recursive agorithm to the correct starting point
    def getWords(self, fragment):
        cur = self

        # Iterate through the tree to make cur the end of the fragment
        for c in fragment:
            if c not in cur.children:
                return []
            else:
                cur = cur.children[c]

        # Begin a chain of recursive calls from the end of the fragment
        candidates = cur.getWordsRec(fragment)

        return candidates

    # Recursive helper method for the algorithm to find all words
    def getWordsRec(self, fragment):
        candidates = []

        # If "count" is in the dict, this word is a complete word.
        # As such, add it into the array
        if "count" in self.children:
            candidates.append(Candidate(fragment, self.children["count"]))

        # Even if this word is already a complete word, it could build into more words
        # e.g. "can" is a word, but so is "cannery"
        # Calls the recursive function on all letters
        for k in self.children:
            if k != "count":
                candidates.extend(self.children[k].getWordsRec(fragment + k))

        return candidates

# Candidate class to hold information about each discovered word
class Candidate():
    def __init__(self, word, confidence):
        self.word = word
        self.confidence = confidence

    # A getter for the candidate's word
    def getWord(self):
        return self.word

    # A getter for the candidate's confidence
    def getConfidence(self):
        return self.confidence

# Database, which is one big tree with special methods for dealing with trees
class Database():
    def __init__(self):
        self.root = WordTree("start")

    # Adds a word into the database and increases its count
    def addWord(self, word):
        cur = self.root

        # Iterate through the tree to the end of the word
        for char in word:
            # If this is a new word, at some point the tree will need to make
            # more subtrees with the new paths from the new letters
            if char not in cur.children:
                cur.children[char] = WordTree(char)

            cur = cur.children[char]

        # If "count" is not a key, then this is a new word.
        # Start the total occurrences of this word at 1
        if "count" not in cur.children:
            cur.children["count"] = 1
        # Otherwise, add 1 to the occurrences of this word.
        else:
            cur.children["count"] += 1

    # Trains the algorithm by adding each word into the Database
    def train(self, sentence):
        # Convert the sentence to lowercase
        refined = sentence.lower()

        # Remove anything that is not a letter or a space using regex
        regex = re.compile('[^a-z ]')
        refined = regex.sub('', refined)

        # Split the sentence into a list delimited by spaces, then add each
        # value of that list into the database
        for word in refined.split(" "):
            self.addWord(word)

    # Returns the sorted array of anything that begins with the fragment
    def getWords(self, fragment):
        return sorted(self.root.getWords(fragment), key=lambda x: x.confidence, reverse = True)

    # Prints the array from getWords in a nice human-readable format
    def printWords(self, fragment):
        finalString = "\"" + fragment + "\" --> "

        candidates = self.getWords(fragment)

        for i, candidate in enumerate(candidates):
            if i != 0:
                finalString += ", "

            finalString += "\"" + candidate.getWord() + "\" "
            finalString += "(" + str(candidate.getConfidence()) + ")"

        print finalString

        return

# Beginning of example code, you can run the required methods as seen below.
root = Database()

# Given example from the prompt
root.train("The third thing that I need to tell you is that this thing does not think thoroughly.")
root.printWords("thi")
root.printWords("nee")
root.printWords("th")

# Another example to show the database can be updated
root.train("The thing that I like to think on Thursdays is that Threshes thoroughly thrash themselves.")
root.printWords("th")
