from delab.corpus.download_author_information import create_climate_authors
import yaml
from yaml.loader import SafeLoader
from delab.delab_enums import LANGUAGE


def run():
    create_climate_authors(read_yaml('en'), LANGUAGE.ENGLISH)
    create_climate_authors(read_yaml('ger'), LANGUAGE.GERMAN)

def read_yaml(lang):
    if lang == 'ger':
        with open('twitter/strategic_communication/climate_change.yaml') as file:
            data = yaml.load(file, Loader=SafeLoader)

    else:
        with open('twitter/strategic_communication/climate_change_en.yaml') as file:
            data = yaml.load(file, Loader=SafeLoader)

    return data

