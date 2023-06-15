import datetime
import random

from django.contrib.auth.models import User

from delab_trees.recursive_tree.recursive_tree import TreeNode
from delab.corpus.download_conversations_twitter import save_tree_to_db
from delab.models import Tweet, TwTopic, SimpleRequest, TWCandidateIntolerance, TWIntoleranceRating
from delab.delab_enums import PLATFORM, LANGUAGE
from delab.nce.download_intolerant_tweets import download_terrible_tweets

"""
The idea is that this script provides a fake conversation to test the labeling pipeline
"""


def test_labeling_constraints():
    clean = True  # delete old fake data
    create = True  # create new fake data
    rank_them = True  # non-fake data to make it clearer
    topic_string = "fake_conversations"
    # create the topic and save it to the db
    topic, created = TwTopic.objects.get_or_create(
        title=topic_string
    )
    simple_request, created = SimpleRequest.objects.get_or_create(
        title="creating faking conversations",
        topic=topic
    )
    if clean:
        TWCandidateIntolerance.objects.filter(tweet__topic__title=topic_string).delete()
        Tweet.objects.filter(topic__title=topic_string).delete()
        Tweet.objects.filter(topic__title=topic_string).delete()
    if create:
        tree = create_conversation(lang=LANGUAGE.GERMAN)
        # print(tree.to_string())
        tree_en = create_conversation(lang=LANGUAGE.ENGLISH)
        # print(tree.to_string())
        save_tree_to_db(tree_en, topic, simple_request, 1, platform=PLATFORM.DELAB)
        save_tree_to_db(tree, topic, simple_request, 2, platform=PLATFORM.DELAB)
        download_terrible_tweets(False, True)
        # this ranks existing candidates as intolerant in order to have a clear view on the fake ones
    if rank_them:
        rank_them_others()


def rank_them_others():
    candidates = TWCandidateIntolerance.objects.filter(tweet__platform=PLATFORM.TWITTER).all()
    for candidate in candidates:
        TWIntoleranceRating.objects.get_or_create(
            u_person_hate=False,
            candidate=candidate,
            coder=User.objects.filter(username="dehne").get()
        )
        TWIntoleranceRating.objects.create(
            u_person_hate=False,
            candidate=candidate,
            coder=User.objects.filter(username="delab").get()
        )

