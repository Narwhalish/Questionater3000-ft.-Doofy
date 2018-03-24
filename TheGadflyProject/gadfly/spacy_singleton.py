"""
This module is to helps us manage our memory resources because it provides
a singleton wrapper around the Spacy English object to prevent it from
being instantiated over and over again. You can access the spacy english
object by calling the function like so:

 spacy_singleton.spacy_en()(self._source_text)

"""
import sputnik
import spacy
import os

data_path = os.path.join(os.path.dirname(spacy.__file__), 'en', 'data')
if not os.path.isdir(data_path):
    print("Need to download Spacy data. Starting download now")
    sputnik.install('spacy', spacy.about.__version__,
                    'en_default', data_path=data_path)


def _spacy_en():
    yield None
    try:
        spacyen = spacy.load('en_default', via=data_path)
    except RuntimeError as e:
        if e.message == "Model not installed. Please run 'python -m spacy.en.download' to install latest compatible model.":
            print("Need to download Spacy data. Starting download now")
            sputnik.install('spacy', spacy.about.__version__,
                            'en_default', data_path=data_path)
            spacyen = spacy.load('en_default', via=data_path)
        else:
            raise
    while True:
        yield spacyen

_SPACY_EN = _spacy_en()


def spacy_en():
    """
    """
    spacyen = next(_SPACY_EN)
    if spacyen:
        return spacyen
    else:
        return spacy_en()
