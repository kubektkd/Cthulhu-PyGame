import json
import utils.config as config

def read_locale_file(lang):
    with open(f'assets/lang/{lang}.json', encoding='utf-8') as f:
        config.locale = json.load(f)


def _(translate_key):
    key_list = translate_key.split('.')

    def json_extract(data, lists):
        if len(lists) > 1:
            return json_extract(data[lists[0]], lists[1:])
        return data[lists[0]]

    return json_extract(config.locale, key_list)
