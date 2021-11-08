import json
import logging
import os
import re
import sqlite3

import numpy as np
from django.db.models import Q
from django_pandas.io import read_frame

from delab.models import Timeline, Tweet
from bertopic import BERTopic
import random

import fasttext.util

from util import TVocabulary

from delab.models import TopicDictionary

BERTOPIC_MODEL_LOCATION = "BERTopic"

logger = logging.getLogger(__name__)


def train_topic_model_from_db(lang="en", store_vectors=True, store_topics=True, update_topics=True,
                              number_of_batchs=-1):
    """
    :param lang:
    :param store_vectors: Stores the embedding vectors from fasttext in a table for quick access for each word in the tweets
    :param store_topics: Boolean store the BERTTopic id as a column for each tweet in order to compare them quickly
    :param update_topics: Only store the berttopic id for the tweets that do not have one, this should to be set to True
                          If the BertTopic Model is re-trained, can be set to False during development for incremental updates of the table
    :param number_of_batchs: The number of tweets used for training the model (should be the all of them if there is time)
    :return:
    """
    logger.debug("starting to train the topic model")
    corpus_for_fitting_sentences = get_train_corpus_for_sentences(lang, max_size=number_of_batchs)

    # os.environ["TOKENIZERS_PARALLELISM"] = "false"
    topic_model_2 = BERTopic(embedding_model="sentence-transformers/all-mpnet-base-v2", verbose=True)
    topics, probs = topic_model_2.fit_transform(corpus_for_fitting_sentences)

    if store_vectors or store_topics:
        vocab = create_vocabulary(corpus_for_fitting_sentences)
        if store_vectors:
            store_embedding_vectors(topic_model_2, vocab, lang)

        if store_topics:
            store_topic_id_tweets(topic_model_2, lang, update_topics, vocab)

    topic_model_2.save(BERTOPIC_MODEL_LOCATION)
    logger.debug("finished training the topic model")
    return BERTOPIC_MODEL_LOCATION


def filter_bad_topics(bertopic_model, vocab):
    bad_topics = get_bad_topics(vocab, bertopic_model)
    topic_info = bertopic_model.get_topic_info()
    # topic_info["Topic"]
    mask = topic_info["Topic"].isin(bad_topics)
    mask = mask[mask == True]
    topic_info.drop(index=mask.index, inplace=True)
    return topic_info


def store_embedding_vectors(bertopic_model, vocab, lang):
    """
    This calculates the words that are in the topics, finds fasttext vectors for these words
    and stores them in the database for the distance measuring later on.
    :param bertopic_model:
    :param vocab:
    :param lang:
    :return:
    """
    # fasttext.load_model('cc.en.300.bin') # comment this in instead of the next line, if you are not Julian
    # ft = fasttext.load_model('/home/dehne/nltk_data/fasttext/cc.{}.300.bin'.format(lang))

    fasttext.util.download_model('en', if_exists='ignore')  # English
    ft = fasttext.load_model('cc.en.300.bin')
    # dim = ft.get_dimension()

    # filter topics
    topic_info = filter_bad_topics(bertopic_model, vocab)

    n_words_nin_voc = 0
    n_words_in_voc = 0
    for topic_id in topic_info.Topic:
        topic_model = bertopic_model.get_topic(topic_id)
        for t_word in topic_model:
            str_w = t_word[0]
            if str_w not in ft.words:
                n_words_nin_voc += 1
            else:
                n_words_in_voc += 1
                ft_vector = ft.get_word_vector(str_w)
                TopicDictionary.objects.get_or_create(word=str_w, ft_vector=json.dumps(ft_vector, cls=NumpyEncoder))
    print("saved ft_vectors. The hit rate was: {}".format(n_words_in_voc / (n_words_in_voc + n_words_nin_voc)))


def get_bad_topics(vocab, topic_model_2):
    """
    Tests if the words in the topic are actual words in the vocabulary
    :param vocab: the vocabulary created from allt he tweets in the database
    :param topic_model_2: the topic model trained on the tweets
    :return:
    """
    topic_info = topic_model_2.get_topic_info()
    topic_info_no_outlier = topic_info.drop(index=0)

    topic_quality = {}
    # topic_info.drop(index=[0], inplace=True)  # dropping the undefined topic
    for topic_id in topic_info_no_outlier.Topic:
        topic_model = topic_model_2.get_topic(topic_id)
        number_example_words = len(topic_model)
        # print(number_example_words)
        missing_words = 0
        # print(topic_model)
        for t_word in topic_model:
            str_w = t_word[0]
            # print(str_w)
            if not vocab.is_in(str_w):
                # print(str_w)
                missing_words += 1
        topic_quality[topic_id] = (number_example_words - missing_words) / number_example_words
    bad_topics = []
    for topic_id, quality_value in topic_quality.items():
        if quality_value <= 0.7:
            bad_topics.append(topic_id)

    bad_topics.append(-1)
    return bad_topics


def get_train_corpus_for_sentences(lang, max_size=-1):
    """
    This constructs the training corpus for the topic analysis.
    :param lang:
    :param max_size: in order to improve testing, it is possible to set max_size > 0 to just train on a subset of the data
    :return: list[str] a list of tweets
    """
    author_tweets_texts, logger = load_author_tweets(lang)
    conversation_tweets_texts = load_conversation_tweets(lang, logger)
    corpus_for_fitting_sentences = create_tweet_corpus_for_bertopic(author_tweets_texts, conversation_tweets_texts)
    if max_size < 0:
        return corpus_for_fitting_sentences
    corpus = random.sample(corpus_for_fitting_sentences, max_size)
    return corpus


def create_tweet_corpus_for_bertopic(author_tweets_texts, conversation_tweets_texts):
    """
    This flattens the tweets to a big set of sentences for the topic training.
    :param author_tweets_texts:
    :param conversation_tweets_texts:
    :return: list[str] a list of sentences for training
    """
    corpus_for_fitting = author_tweets_texts + conversation_tweets_texts
    # corpus_for_fitting = author_tweets_texts
    corpus_for_fitting_sentences = []
    for tweet in corpus_for_fitting:
        for sentence in tweet.split("."):
            corpus_for_fitting_sentences.append(sentence)
    corpus_for_fitting_sentences = clean_corpus(corpus_for_fitting_sentences)
    return corpus_for_fitting_sentences


def clean_corpus(corpus_for_fitting_sentences):
    """
    This is typical preprocessing in order to improve on the outcome of the topic analysis
    :param corpus_for_fitting_sentences:
    :return:
    """
    result = []
    for temp in corpus_for_fitting_sentences:
        # removing hashtags
        temp = re.sub("@[A-Za-z0-9_]+", "", temp)
        temp = re.sub("#[A-Za-z0-9_]+", "", temp)
        # removing links
        temp = re.sub(r"http\S+", "", temp)
        temp = re.sub(r"www.\S+", "", temp)
        # removing punctuation
        temp = re.sub('[()!?]', ' ', temp)
        temp = re.sub('\[.*?\]', ' ', temp)
        # alphanumeric
        temp = re.sub("[^a-z0-9A-Z]", " ", temp)
        temp = re.sub("RT", "", temp)
        temp = temp.strip()

        number_of_words = len(temp.split(" ")) > 3
        if len(temp) > 1 and number_of_words:
            result.append(temp)
    return result


def store_topic_id_tweets(bertopic_model, lang, update_topics, vocab):
    # load tweets
    topic_info = filter_bad_topics(bertopic_model, vocab)
    if update_topics:
        conversation_tweets = Tweet.objects.filter(Q(language=lang))
    else:
        conversation_tweets = Tweet.objects.filter(Q(language=lang) & Q(bertopic_id__isnull=True))

    conversation_texts = list(conversation_tweets.values_list("text", flat=True))
    suggested_topics = bertopic_model.transform(conversation_texts)[0]
    index = 0
    conversation_tweet_objs = conversation_tweets.all()
    for conversation_tweet in conversation_tweet_objs:
        if suggested_topics[index] in topic_info.Topic:
            conversation_tweet.bertopic_id = suggested_topics[index]
        else:
            conversation_tweet.bertopic_id = -2
        index += 1

    number_before = Tweet.objects.filter(Q(language=lang) & Q(bertopic_id__isnull=True)).count()
    Tweet.objects.bulk_update(conversation_tweet_objs, ["bertopic_id"])
    number_after = Tweet.objects.filter(Q(language=lang) & Q(bertopic_id__isnull=True)).count()
    print("Updated {} tweets with topic_ids".format(number_before - number_after))


def load_conversation_tweets(lang, logger):
    conversation_tweets = Tweet.objects.filter(Q(language=lang)).all()
    df_conversations = read_frame(conversation_tweets, fieldnames=["id",
                                                                   "author_id",
                                                                   "text",
                                                                   ])
    logger.info("loaded the timeline from the database")
    conversation_tweets_texts = list(df_conversations.text)
    return conversation_tweets_texts


def load_author_tweets(lang):
    tweets = Timeline.objects.filter(Q(lang=lang)).all()
    df = read_frame(tweets, fieldnames=["id",
                                        "author_id",
                                        "text",
                                        "conversation_id",
                                        "created_at",
                                        ])
    logger.info("loaded the timeline from the database")
    author_tweets_texts = list(df.text)
    return author_tweets_texts, logger


def create_vocabulary(corpus_for_fitting_sentences):
    vocab = TVocabulary()
    for corpus_for_fitting_sentence in corpus_for_fitting_sentences:
        vocab.add_sentence(corpus_for_fitting_sentence)
    return vocab


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
