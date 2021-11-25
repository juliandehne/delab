import logging

from delab.models import Tweet, PLATFORM
from delab.tw_connection_util import send_tweet

logger = logging.getLogger(__name__)


def publish_moderation(instance):
    delab_admission = " (This was automatically send by the deliberation app)"
    text = instance.text + delab_admission
    parent_tweet = Tweet.objects.filter(twitter_id=instance.tn_parent_id).get()
    if parent_tweet.platform == PLATFORM.TWITTER:
        reply_to_id = parent_tweet.twitter_id
        response = send_tweet(text, tweet_id=reply_to_id)
        logger.info(response)
        logger.info("send tweet {}".format(instance))
