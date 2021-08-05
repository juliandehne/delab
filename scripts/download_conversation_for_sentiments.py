from delab.download_conversations import *
from twitter.tw_connection_util import TwitterStreamConnector


def run():
    download_conversations("Vaccination", ["covid_19", "vaccine", "delta", "getvaccienated", "vaccination"])
    # download_conversations("Migration", ["migration", "UNHCR"])
    # download_conversations("Impfung", ["rki_de"])
    # run_demo()
    # delete_rules_tests()


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
