import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()
punctuations = "?:!.,;"

def stopword_removal(token):
    tokens_without_sw = [word for word in token if not word in stopwords.words()]
    return tokens_without_sw

def lemmitization(token):
    token = wordnet_lemmatizer.lemmatize(token, pos="v")
    return token

def output_to_csv(file_name, data_list, review_df):
    df = pd.DataFrame(data_list)
    df = df.fillna(0)
    df.index.name = "Review #"
    df['body'] = review_df['body']
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df.to_csv(file_name)


def Bagofwords():
    Review_df = pd.read_csv("D:/Data.csv")
    texts_list = Review_df['body'].tolist()
    # texts_list[0] = "Playing...."
    for i in range(len(texts_list)):
        texts_list[i] = texts_list[i].lower()
        # Return a match at every NON word character (characters NOT between a and Z. Like "!", "?" white-space etc.)
        texts_list[i] = re.sub(r'\W', ' ', texts_list[i])
        # Replace all white-space characters with ""
        texts_list[i] = re.sub(r'\s+', ' ', texts_list[i])
        # TODO Number remove

    bag_of_words_list = []
    count = 0

    for sentence in texts_list:
        wordfreq = {}
        tokens = nltk.word_tokenize(sentence)
        #stopwords
        ftoken=stopword_removal(tokens)

        for token in ftoken:
            token=lemmitization(token)
            if token not in wordfreq.keys():
                wordfreq[token] = 1
            else:
                wordfreq[token] += 1

        count += 1
        bag_of_words_list.append(wordfreq)

    output_to_csv('Bagofwords_output.csv', bag_of_words_list, Review_df)

Bagofwords()
