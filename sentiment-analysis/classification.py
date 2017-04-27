import nltk
from nltk.classify.naivebayes import NaiveBayesClassifier

def get_words_in_entries(entries):
    all_words = []
    for (words, sentiment) in entries:
      all_words.extend(words)
    return all_words


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


def read_entries(fname, t_type):
    entries = []
    f = open(fname, 'r')
    line = f.readline()
    while line != '':
        entries.append([line, t_type])
        line = f.readline()
    f.close()
    return entries


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
    
    return features


def classify_tweet(tweet):
    return \
        classifier.classify(extract_features(nltk.word_tokenize(tweet)))


# read in postive and negative training entries
pos_entries = read_entries('positives.txt', 'positive')
neg_entries = read_entries('negatives.txt', 'negative')

# filter away words that are less than 3 letters to form the training data
entries = []
for (words, sentiment) in pos_entries + neg_entries:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    entries.append((words_filtered, sentiment))


# extract the word features out from the training data
word_features = get_word_features(\
                    get_words_in_entries(entries))

#print(extract_features)
# get the training set and train the Naive Bayes Classifier
training_set = nltk.classify.util.apply_features(extract_features, entries)
classifier = NaiveBayesClassifier.train(training_set)


# read in the test entries and check accuracy
# to add your own test entries, add them in the respective files
test_entries = read_entries('positives_test.txt', 'positive')
test_entries.extend(read_entries('negatives_test.txt', 'negative'))
total = accuracy = float(len(test_entries))

for tweet in test_entries:
    if classify_tweet(tweet[0]) != tweet[1]:
        accuracy -= 1

print('Total accuracy: %f%% (%d/4).' % (accuracy / total * 100, accuracy))

print('bugün harika bir gün => ' + classify_tweet('bugün harika bir gün'))
print('hayatımda bu kadar rezalet bir etkinlik görmedim => ' + classify_tweet('hayatımda bu kadar rezalet bir etkinlik görmedim'))
