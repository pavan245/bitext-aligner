import six
from google.cloud import translate_v2 as translate

""" text - text to Translate
      target_lang - Target Language Code (ISO Standard)
"""


def translate_text(text, target_lang):

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    result = translate_client.translate(text, target_language=target_lang, model='nmt')
    print("Translated Text :: ", result['translatedText'])

    return result['translatedText']
