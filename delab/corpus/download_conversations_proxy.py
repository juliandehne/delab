import logging

from delab.delab_enums import PLATFORM, LANGUAGE
from .download_conversations_reddit import search_r_all
from .download_conversations_twitter import download_conversations_tw

logger = logging.getLogger(__name__)


def download_conversations(topic_string, query_string, request_id=-1, language=LANGUAGE.ENGLISH, max_data=False,
                           fast_mode=False, conversation_filter=None, tweet_filter=None, platform=PLATFORM.TWITTER,
                           recent=True):
    """
    This is a proxy to download conversations from twitter, reddit respectively with the same interface
    :param topic_string:
    :param query_string:
    :param request_id:
    :param language:
    :param max_data:
    :param fast_mode:
    :param conversation_filter:
    :param tweet_filter:
    :param platform:
    :param recent:
    :return:
    """
    if fast_mode:
        max_number_of_candidates = 100
        min_conversation_length = 3
        max_conversation_length = 100
        if platform == PLATFORM.TWITTER:
            download_conversations_tw(topic_string, query_string, request_id, language, max_data,
                                      fast_mode, conversation_filter, tweet_filter, platform,
                                      recent, min_conversation_length=min_conversation_length,
                                      max_conversation_length=max_conversation_length,
                                      max_number_of_candidates=max_number_of_candidates)
        else:
            search_r_all(query_string, request_id, topic_string, min_conversation_length=min_conversation_length,
                         max_conversation_length=max_conversation_length,
                         max_number_of_candidates=max_number_of_candidates, tweet_filter=tweet_filter, recent=recent)

    if platform == PLATFORM.TWITTER:
        download_conversations_tw(topic_string, query_string, request_id, language, max_data,
                                  fast_mode, conversation_filter, tweet_filter, platform,
                                  recent)
    else:
        search_r_all(query_string, request_id, topic_string, tweet_filter=tweet_filter)
