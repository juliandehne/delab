from delab.nce.download_intolerant_tweets import download_terrible_tweets


def run():
    download = False
    link = True
    download_terrible_tweets(False, False, download_right_wing=True)

