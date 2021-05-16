


from src.nlp.util import * ; import src.nlp.util as util
from src.nlp.pipeline import pipeline, stopwords

import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


classifiers = {}
def register(f):
    classifiers[f.__name__] = f
    return f


@register
def all_yes(text, metadata):
    return {
        'relevant': True,
        'score': '1',
    }

@register
def all_no(text, metadata):
    return {
        'relevant': False,
        'score': '0',
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


@register
def tfidf(text, metadata):
    doc = pipeline(text)
    lemmas = [
        lem
        for lem in [tok.lemma_.lower() for tok in doc]
        if lem and lem.isalpha() and lem not in stopwords
    ]
    x = _tfidf_pipe.transform([' '.join(lemmas),])
    prob = _tfidf_model.predict_proba(x)[0,1]
    return {
        'relevant': bool(prob>0.5),
        'score': str(int(prob*100)),
    }
_tfidf_pipe = load('./src/nlp/tfidf/pipe.pkl')
_tfidf_model = load('./src/nlp/tfidf/model.pkl')



