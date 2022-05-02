import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from nltk.stem import WordNetLemmatizer


wordnet_lemmatizer = WordNetLemmatizer()
punctuations = "?:!.,;"


def output_tf_idf(text_list):
    vectorizer = TfidfVectorizer(smooth_idf=False, use_idf=True, sublinear_tf=False)
    vectors = vectorizer.fit_transform(text_list)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)
    df.index.name = "Review #"
    df.to_csv('tf_idf_output.csv')
    print(df)


def compute_tf(token):
    num_of_words = len(token)

    freq = {}
    tf = {}
    for word in token:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1

    for value in freq:
        tf[value] = freq[value] / num_of_words

    return tf, freq


def compute_idf(doc_list):
    import math
    idf_dict = {}
    N = len(doc_list)

    for doc in doc_list:
        for word, val in doc.items():
            if val > 0:
                if idf_dict.get(word):
                    idf_dict[word] += val
                else:
                    idf_dict[word] = val

    for word, val in idf_dict.items():
        idf_dict[word] = math.log(N / float(val))

    return idf_dict


def compute_tf_idf(tf_list, idf):
    for doc in tf_list:
        for word, val in doc.items():
            doc[word] = doc[word] * idf[word]
    return tf_list


def output_to_csv(file_name, data_list, review_df=None):
    df = pd.DataFrame(data_list)
    df = df.fillna(0)
    df.index.name = "Review #"
    if review_df is not None:
        df['body'] = review_df['body']
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]
    df.to_csv(file_name)


def main():

    reviews_df = pd.read_csv("D:/Data.csv")

    texts_list = reviews_df['body'].tolist()

    for i in range(len(texts_list)):
        texts_list[i] = texts_list[i].lower()
        texts_list[i] = re.sub(r'\W', ' ', texts_list[i])
        texts_list[i] = re.sub(r'\s+', ' ', texts_list[i])

    all_tfs = []
    all_freqs = []
    for text in texts_list:
        token = nltk.word_tokenize(text)
        # Remove Punctuation
        for word in token:
            if word in punctuations:
                token.remove(word)

        # Lemmatization
        for i in range(len(token)):
            token[i] = wordnet_lemmatizer.lemmatize(token[i], pos="v")
        tf, freq = compute_tf(token)
        all_tfs.append(tf)
        all_freqs.append(freq)

    idf = compute_idf(all_freqs)
    tfs_final = compute_tf_idf(all_tfs, idf)
    output_to_csv('tf_idf_output.csv', tfs_final, reviews_df)


if __name__ == '__main__':
    main()
