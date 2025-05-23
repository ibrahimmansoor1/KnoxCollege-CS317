#Muhammad Ibrahim Mansoor


import random
import glob
import sys
import traceback

"""
Markov Babbler

After being trained on text from various authors, it will
'babble' (generate random walks) and produce text that
vaguely sounds like the author of the training texts.

run as: python3 babbler.py 
or optioanlly with parameters: python3 babbler.py 2 tests/test1.txt 5 
"""

# ------------------- Implementation Details: -------------------------------
# Our entire graph is a dictionary
#   - keys/states are ngrams represented (could have been tuple, CANNOT be a list,
#       because we need to use states as dictionary keys, and lists are not hashable)
#   - values are either lists or Bags
# Starter states are a list of words (could have been a Bag; either an ordered or unordered collection, with duplicates allowed)
# When we pick a word, we transition to a new state
# e.g. suppose we are using bigrams and are at the state ‘the dog’ and we pick the word ‘runs’. 
# Our new state is ‘dog runs’, so we look up that state in our dictionary, and then get the next word, and so on…
# Ending states can generate a special "stop" symbol; we will use ‘EOL’.
#   If we generate the word ‘EOL’, then the sentence is over. Since all words are lower-case, this won’t be confused for a legitimate word

# --------------------- Tasks --------------------------------
# class Babbler:
    # def __init__(self, n, seed=None)      # already completed with initial data structures
    # def add_file(self, filename)          # already completed; calls add_sentence(), so go there next, read comments, and plan out your steps
    # def add_sentence(self, sentence)      # implement this
    # def get_starters(self)                # implement this
    # def get_stoppers(self)                # implement this
    # def get_successors(self, ngram)       # implement this
    # def get_all_ngrams(self)              # implement this
    # def has_successor(self, ngram)        # implement this
    # def get_random_successor(self, ngram) # implement this
    # def babble(self)                      # implement this

# ------------------- Tips ----------------------------------
# read through all the comments in the below functions before beginning to code
# remember that our states are n-grams, so whatever the n value is, that's how many words per state (including starters and stoppers)
# our successors (the value for each key in our dictionary) are strings representing words (not states, since n-gram states could be of multiple words)
# since we will represent your n-grams as strings, remember to separate words with a space 
# when updating your state, make sure you don't end up with extra spaces or you won't find it in the dictionary
# add print statements while debugging to ensure is step in your process is working as intended

debugging = False

class Babbler:
    # nothing to change here; read, understand, move along
    #1
    def __init__(self, n, seed=None):
        """
        n: length of an n-gram for state
        seed: seed for a random number generation (None by default)
        """
        self.n = n #size of our n-grams (i.e. our brain graph states will be strings of n space-separated strings)
        if seed != None: #seed:  
            random.seed(seed)

        # need to store our sparce graph as a dictionary 
        # need to store keys/states (as hashables, so strings or tuples, not list)
        # need to store values (lists or bag; both allow duplicates, one is ordered, the other is not)
            # graph = {
            #     "I think": ["therefore", this", "you", "you"],   #list of words that we've seen follow this key (preserving multiplicity)      
            # }
        # state used as keys are strings with spaces between words; values are lists of words that could follow the keys.
        # value list can have repeated entries to preserve probability


        self.brainGraph = {}  # note that we need to be able to quickly find options for current state (so we use it for indexing, i.e. as our key)

        self.starters = [] # let's track starting states as a list of strings (could have made them part of dictionary but let's have a list for debugging/testing purposes )
        # we cannot store these as part of our brain graph 
        # consider using "" as an empty state, indicating the start of a sentence
        # the list of successors would need to be entire state strings rather than just word strings as for the other states
        # this inconsistency would require special handling of the "" key in our dictionary
        # having a separate special list is a more explicit way of signaling/handling this special case

        self.stoppers = [] # let's also track ending states as a list of strings (don't really need it; only for debugging/testing purposes)
    
    #2
    def add_file(self, filename):

        """
        This method is already done for you. 
        It processes information from all sentences in your input file, by calling add_sentence() for each line,
        after removing trailing spaces and making it lower case.
        We are assuming input data has already been pre-processed so that each sentence is on a separate line.
        """

        print("Reading from your file...")
        for line in [line.rstrip().lower() for line in open(filename, errors='ignore').readlines()]:
            self.add_sentence(line)
        print("Done reading from your file.")
        print("\n---------resulting graph: --------")
        print(self.brainGraph)
        print("----------------------------------\n")
    
    #3
    def add_sentence(self, sentence):

        #Process the given sentence (a string separated by spaces): 
        #Break the sentence into words using split(); 

        words = sentence.split()
        if len(words) < self.n: #This step is to break the method if the number of words in the sentence are less than the n-gram provided
            return

        # starter n program
        starter_ngram = ' '.join(words[:self.n]) 
        #wrods[:self.n] is used for extracting the first n words form the sentence
        #''.join combines the words into a string, then the n gram is added to self.starters
        self.starters.append(starter_ngram)

        # Process n-grams
        for i in range(len(words) - self.n + 1):
            ngram = ' '.join(words[i:i + self.n])
            if i + self.n < len(words):
                successor = words[i + self.n]
                if ngram not in self.brainGraph:
                    self.brainGraph[ngram] = []
                self.brainGraph[ngram].append(successor)
                #if n gram is not in self.braingraph then its added with an empty list as its value
            else:
                # Add stopper n-gram
                self.stoppers.append(ngram)
                if ngram not in self.brainGraph:
                    self.brainGraph[ngram] = [] #if n gram not already in self.braingraph tehn its added as empty list as its value again
                    #special symbol 'EOL' in the state transition table. 'EOL' is short for 'end of line'; since it is capitalized and all our input texts are lower-case, it will be unambiguous.
                self.brainGraph[ngram].append('EOL')

     
    #4
    def get_starters(self):
        return self.starters
    
    #5
    def get_stoppers(self):
        return self.stoppers
    
    #6
    def get_successors(self, ngram):
        return self.brainGraph.get(ngram, [])
        #If the ngram exists, returns its list of successors.
        #If the ngram does not exist, returns an empty list.

    #7
    def get_all_ngrams(self):
        return list(self.brainGraph.keys())
    
    #8
    def has_successor(self, ngram):
        return ngram in self.brainGraph and len(self.brainGraph[ngram]) > 0
    
    #9
    def get_random_successor(self, ngram):
        successors = self.get_successors(ngram)
        if not successors:
            return None
        return random.choice(successors)
    
    #10
    def babble(self):
        if not self.starters:
            return ""

        current_ngram = random.choice(self.starters) #random generation
        sentence = current_ngram

        while True:
            successor = self.get_random_successor(current_ngram)
            if successor == 'EOL' or successor is None: #breaking the program if the successor is End of line
                break
            sentence += ' ' + successor
            current_ngram = ' '.join(sentence.split()[-self.n:])

        return sentence
            

# nothing to change here; read, understand, move along
def main(n=3, filename='tests/test1.txt', num_sentences=5):
    """
    Simple test driver.
    """
    
    print('Currently running on ',filename)
    babbler = Babbler(n)
    babbler.add_file(filename)

    try:
        print(f'num starters {len(babbler.get_starters())}')
        print("\t",babbler.get_starters())
        print(f'num ngrams {len(babbler.get_all_ngrams())}')
        print(f'num stoppers {len(babbler.get_stoppers())}')
        print("\t",babbler.get_stoppers())
        print("------------------------------\nPreparing to drop some bars...\n")
        for _ in range(num_sentences):
            print(babbler.babble())
    except Exception as e:
        print("This code crashed... QQ\n"+
            " - make sure you have implemented all of the above methods\n"+
            " - review the crash report below\n"+
            " - add lots of print statements to your methods to ensure they are working as you intended\n")
        print("--------------------------Crash Report:--------------------------")
        traceback.print_exc() 

# nothing to change here; read, understand, move along
# to execute this script, in a terminal nagivate to your cs317/markov folder, unless already there
# enter the following terminal command: python3 babbler.py
# default values below will be used; alternatively you can provide up to 3 arguments (n, filename, num_sentences), for example: python3 babbler.py 2 tests/test2.txt 10
if __name__ == '__main__': 
    print("Entered arguments: ",sys.argv)
    sys.argv.pop(0) # remove the first parameter, which should be babbler.py, the name of the script
    # -------default values -----------
    n = 3
    filename = 'tests/test1.txt'
    num_sentences = 5
    #----------------------------------
    if len(sys.argv) > 0: # if any argumetns are passed, first is assumed to be n
        n = int(sys.argv.pop(0))
    if len(sys.argv) > 0: # if any more were passed, the next is assumed to be the filename
        filename = sys.argv.pop(0)
    if len(sys.argv) > 0: # if any more were passed, the next is assumed to be number of sentences to be generated 
        num_sentences = int(sys.argv.pop(0))
    main(n, filename, num_sentences) # now we call main with all the actual or default arguments