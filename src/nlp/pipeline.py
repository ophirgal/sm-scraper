

import spacy
from src.nlp.util import * ; import src.nlp.util as util
pipeline = spacy.load('en_core_web_sm')


# accepts lower-cased queries, returns lower-case 2-letter state abbreviation
def state_dict():
    fn_sd = './src/nlp/state_dict.txt'
    txt = read(fn_sd).split('\n')
    abbr = {
        line.split('  ')[0]: line[len(line.split('  ')[0]):].lstrip().split(' ')[0]
        for line in txt
    }
    short = list(abbr.values())
    for s in short:
        abbr[f'{s[0]}.{s[1]}.'] = s
        abbr[f'{s[0]}{s[1]}.'] = s
    for line in txt:
        abbr[line.split(' ')[-1]] = line[len(line.split('  ')[0]):].lstrip().split(' ')[0]
    for v in list(abbr.values()):
        abbr[v] = v
    abbr = {k.lower(): v.lower() for k,v in abbr.items()}
    return abbr
state_dict = state_dict()


# stopwords
stopwords = {
    line.lower() for line in read('./src/nlp/stopwords.txt').split('\n')
    if line and line[0]!='#'
}


