


from src.nlp.util import * ; import src.nlp.util as util
from src.nlp.pipeline import pipeline

classifiers = {}
def register(f):
    classifiers[f.__name__] = f
    return f


@register
def all_yes(text, metadata):
    return {
        'relevant': True,
        'score': 'yes',
    }

@register
def all_no(text, metadata):
    return {
        'relevant': False,
        'score': 'no',
    }

@register
def has_police(text, metadata):
    doc = pipeline(text)
    lemmas = [token.lemma_ for token in doc]
    count = sum([1 for l in lemmas if l.lower()=='police'])
    return {
        'relevant': count>0,
        'score': str(count),
    }

