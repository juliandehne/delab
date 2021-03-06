import json

from delab.corpus.download_conversations_proxy import download_conversations
from delab.delab_enums import LANGUAGE, PLATFORM
from delab.tw_connection_util import TwitterStreamConnector

""" This is a django runscript, it can be started in the django home directory with
    $ python manage.py runscript [filename_no_ending]    
"""


def run():
    download_conversations('Klimawandel', "Klimawandel OR (Klima Wandel) OR (Erderwärmung)",
                           language=LANGUAGE.GERMAN)
    download_conversations('Klimawandel', "(climate change) OR (earth warming)",
                           language=LANGUAGE.ENGLISH)
    # download_conversations('Klimawandel', "Klimawandel OR (Klima Wandel) OR (Erderwärmung)",
    # language=LANGUAGE.GERMAN, platform=PLATFORM.REDDIT)
    # download_conversations('Klimawandel', "(climate change) OR (earth warming)",
    #    language=LANGUAGE.ENGLISH, platform=PLATFORM.REDDIT)


def delete_rules_tests():
    connector = TwitterStreamConnector()
    existing_rules = connector.get_rules()
    connector.delete_all_rules(existing_rules)


def pretty_print_stream(json_response):
    print(json.dumps(json_response, indent=4, sort_keys=True))
    return False


def run_demo():
    connector = TwitterStreamConnector()
    sample_rules = [
        {"value": "dog has:images", "tag": "dog pictures"},

    ]
    connector.delete_all_rules(sample_rules)
    sample_rules = [
        {"value": "#covid #vaccination lang:en"}
    ]
    connector.set_rules(sample_rules)
    query = {"tweet.fields": "created_at,", "expansions": "author_id", "user.fields": "created_at"}
    connector.get_stream(query, pretty_print_stream)
