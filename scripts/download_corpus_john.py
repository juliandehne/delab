import logging
from functools import partial
from typing import List

from django.db import IntegrityError

from delab.TwConversationTree import TreeNode
from delab.corpus.download_conversations_twitter import download_conversation_as_tree, save_tree_to_db, \
    get_priority_parent_from_references, store_tree_data
from delab.corpus.download_conversations_util import set_up_topic_and_simple_request, apply_tweet_filter
from delab.delab_enums import PLATFORM
from delab.models import TweetSequence, Tweet, MissingTweets
from delab.tw_connection_util import DelabTwarc

topic = "culturalscripts"

# create an artificial topic and query
simple_request, tw_topic = set_up_topic_and_simple_request("john twitter corpus 09_08_22", -1, topic)

logger = logging.getLogger(__name__)


def run():
    group_dict = read_in_john_urls()

    twarc = DelabTwarc()
    # key is the grouping for the partial conversation, value ist the list or twitter urls for the tweets
    for key, value in group_dict.items():
        # select the id at the end of the url
        candidate_id = value[0].split("/")[-1]
        # download the conversation tweet
        tweet = next(twarc.tweet_lookup([candidate_id]))
        if "data" in tweet:
            tweet_data = tweet["data"][0]
            conversation_id = int(tweet_data["conversation_id"])
            sequence_ids = []
            for post in value:
                twitter_post_id = post.split("/")[-1].strip()
                if len(twitter_post_id) == 0:
                    continue
                sequence_id = int(twitter_post_id)
                sequence_ids.append(sequence_id)
            download_conversation_of_interest(conversation_id, key, sequence_ids, twarc)
        else:
            logger.debug("could not find conversation for tweet with url {}. Storing in missing_tweets".format(value))
            MissingTweets.objects.create(
                twitter_id=candidate_id,
                platform=PLATFORM.TWITTER,
                error_message=tweet.get("error", "custom message: conversation id not found during lookup"),
                simple_request=simple_request,
                topic=tw_topic
            )


def read_in_john_urls():
    f = open('/home/dehne/ownCloud/delab/corpus/version1/twitter_urls.txt', 'r')
    content = f.read()
    content = content.replace("\n", "")
    content = content + "  504"
    groups = content.split(". ")[1:]
    group_dict = {}
    for group in groups:
        group_id = group[-3:]
        if group_id in group_dict:
            print("wtf")
        group = group[:-3]
        group = group.strip()
        group_members = group.split(",")
        group_dict[group_id] = group_members
    return group_dict


def download_conversation_of_interest(conversation_id, key, sequence_ids, twarc):
    # create a tweet filter that adds the tweets to a common sequence
    sequence_tweet_filter = partial(tweet_filter, sequence_ids, str(key) + "_twitter_09_08_22")
    # only download the conversation if it does not already exist
    if not Tweet.objects.filter(conversation_id=conversation_id).exists():
        # attempt the basic conversation download
        downloaded_tree = download_conversation_as_tree(twarc, conversation_id, -1)
        save_tree_to_db(downloaded_tree, tw_topic, simple_request, conversation_id, PLATFORM.TWITTER,
                        tweet_filter=sequence_tweet_filter)
    # in any case check if all the elements of the sequence where downloaded or correct it
    check_downloaded_sequences(conversation_id, sequence_ids, sequence_tweet_filter, twarc)


def check_downloaded_sequences(conversation_id, sequence_ids, sequence_tweet_filter, twarc):
    downloaded_tweets = Tweet.objects.filter(twitter_id__in=sequence_ids)
    downloaded_count = downloaded_tweets.count()
    sequence_ids_set = set(sequence_ids)
    # assert that all the elements of the sequence where downloaded previously
    assertion = downloaded_count == len(sequence_ids_set)
    if not assertion:
        # if the assertion does not hold, we assume there a members of the sequence set that are not in the downloaded
        downloaded_ids = set(downloaded_tweets.values_list("twitter_id", flat=True))
        assert len(sequence_ids_set) > len(downloaded_ids)
        missing_sequence = sequence_ids_set - downloaded_ids
        logger.debug("only {}/{} of sequence are downloaded".format(downloaded_count, len(sequence_ids)))
        assert len(missing_sequence) > 0
        # download the missing elements
        missing_tweets_data = next(twarc.tweet_lookup(missing_sequence))
        if "data" in missing_tweets_data:
            missing_tweets = missing_tweets_data["data"]
            not_found_tweets = process_not_found_tweets(missing_sequence, missing_tweets)
            logger.debug(
                "only {}/{} of missing_tweets could be found and the rest will be stored in missing tweets table".format(
                    len(missing_sequence) - len(not_found_tweets), len(missing_sequence)))
            # restore the tree structure in the database with the newly downloaded elements
            solve_missing_tweets(missing_tweets=missing_tweets,
                                 sequence_ids=sequence_ids,
                                 conversation_id=conversation_id,
                                 sequence_tweet_filter=sequence_tweet_filter,
                                 twarc=twarc)


def process_not_found_tweets(missing_sequence, missing_tweets):
    not_found_tweets = []
    if len(missing_tweets) != len(missing_sequence):
        found_online = set([int(tweet_data["id"]) for tweet_data in missing_tweets])
        not_found_in_sequence = missing_sequence - found_online
        print("missing from the sequence are: {}".format(not_found_in_sequence))
        for missing_tweet in missing_tweets:
            tweet_id = missing_tweet["id"]
            if tweet_id in not_found_in_sequence:
                MissingTweets.objects.create(
                    twitter_id=tweet_id,
                    platform=PLATFORM.TWITTER,
                    error_message="custom message: not found with lookup"
                )
                not_found_tweets.append(missing_tweet)
                logger.debug("stored tweet with id as missing {}".format(tweet_id))

    return not_found_tweets


def solve_missing_tweets(missing_tweets: List,
                         sequence_ids: List,
                         conversation_id: int,
                         sequence_tweet_filter,
                         twarc):
    """
    :param sequence_tweet_filter:
    :param missing_tweets:
    :param sequence_ids:
    :param conversation_id:
    :param twarc: TODO use this to download missing parents eventually
    :return:
    """
    """
    the algorithm works as follows:
    - a) see if tweet has parent in the db and store it
    - b) if it has no parent, make root parent and add field tn_original_parent for transparency
    - c) if it has a parent in the current sequence, sort by creation date and store them in that order 
        - case a or case b should have stored the parent
        - if the parent is in the current sequence, the sorting should work as replies are always after the parent  
    """
    missing_tweets_ids = [tweet["id"] for tweet in missing_tweets]
    assert conversation_id not in missing_tweets_ids
    downloaded_twitter_ids = list(
        Tweet.objects.filter(conversation_id=conversation_id).values_list("twitter_id", flat=True))
    orphans = []
    for missing_tweet in missing_tweets:
        assert int(missing_tweet["conversation_id"]) == conversation_id
        if "referenced_tweets" not in missing_tweet:
            print(conversation_id)
        assert "referenced_tweets" in missing_tweet, missing_tweet
        parent_id, parent_type = get_priority_parent_from_references(missing_tweet["referenced_tweets"])
        missing_node = TreeNode(missing_tweet, missing_tweet["id"], parent_id)
        if parent_id in downloaded_twitter_ids:
            store_tree_data(conversation_id, PLATFORM.TWITTER, missing_node, simple_request,
                            tw_topic, sequence_tweet_filter)
        else:
            if parent_id in sequence_ids:
                orphans.append(missing_tweet)
            else:
                store_node_as_fake_root_child(conversation_id, missing_node, sequence_tweet_filter)
    store_in_sequence_orphans(conversation_id, orphans, sequence_tweet_filter)


def store_in_sequence_orphans(conversation_id, orphans, sequence_tweet_filter):
    """
    Sorts the missing in-sequence elements and stores them one after another in order to assert the correct structure in
    the db
    :param conversation_id:
    :param orphans:
    :param sequence_tweet_filter:
    :return:
    """
    orphans.sort(key=lambda x: x["created_at"], reverse=False)
    for orphan in orphans:
        parent_id, parent_type = get_priority_parent_from_references(orphan["referenced_tweets"])
        missing_node = TreeNode(orphan, orphan["id"], parent_id)
        store_tree_data(conversation_id, PLATFORM.TWITTER, missing_node, simple_request,
                        tw_topic, sequence_tweet_filter)


def store_node_as_fake_root_child(conversation_id, missing_node, sequence_tweet_filter):
    """
    create an artificial parent relationship with the root of the conversation
    :param conversation_id:
    :param missing_node:
    :param sequence_tweet_filter:
    :param simple_request:
    :param tw_topic:
    :return:
    """
    tweet = Tweet(topic=tw_topic,
                  text=missing_node.data["text"],
                  simple_request=simple_request,
                  twitter_id=missing_node.data["id"],
                  author_id=missing_node.data["author_id"],
                  conversation_id=conversation_id,
                  created_at=missing_node.data["created_at"],
                  in_reply_to_user_id=missing_node.data.get("in_reply_to_user_id", None),
                  in_reply_to_status_id=missing_node.data.get("in_reply_to_status_id", None),
                  platform=PLATFORM.TWITTER,
                  tn_original_parent=missing_node.parent_id,
                  tn_parent_id=conversation_id,
                  tn_parent_type=missing_node.parent_type,
                  # tn_priority=priority,
                  language=missing_node.data["lang"])
    try:
        apply_tweet_filter(tweet, sequence_tweet_filter)
    except IntegrityError:
        pass


def download_all_missing_parents(parent_id, existing_tree_ids, twarc) -> List:
    """
    downloads parents recursively until an existing id is found (currently not used)
    :param parent_id:
    :param existing_tree_ids:
    :param twarc:
    :return:
    """
    parent = next(twarc.tweet_lookup(tweet_ids=[parent_id]))
    if "data" not in parent:
        return []
    # assert "data" in parent, parent
    parent_data = parent["data"][0]
    grand_parent_id, grant_parent_type = get_priority_parent_from_references(parent_data["referenced_tweets"])
    if grand_parent_id in existing_tree_ids:
        return [parent_data]
    found_parents = download_all_missing_parents(grand_parent_id, existing_tree_ids, twarc)
    partial_tree_data = [parent_data] + found_parents
    return partial_tree_data


def tweet_filter(sequence_ids, sequence_name, tweet):
    """
    this tweet_filter makes sure that the elements of the sequence are linked to the existing sequence
    :param sequence_ids:
    :param sequence_name:
    :param tweet:
    :return:
    """
    if Tweet.objects.filter(twitter_id=tweet.twitter_id).exists():
        tweet = Tweet.objects.filter(twitter_id=tweet.twitter_id).first()
    else:
        tweet.save()

    if tweet.twitter_id in sequence_ids:
        if TweetSequence.objects.filter(name=sequence_name).exists():
            sequence = TweetSequence.objects.filter(name=sequence_name).get()
        else:
            sequence = TweetSequence.objects.create(name=sequence_name)
        sequence.tweets.add(tweet)
    return tweet
