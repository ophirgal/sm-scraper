

import requests, json
text = 'Police say John Doe was seen doing a thing in Elizabeth, New Jersey on May 32, 1999.'
print(f'INPUT: {text}')

# get relevance classifiers
response = requests.get(
    url='http://localhost:9001/get-relevance-classifiers',
    params={},
)
print(response.json())

# get relevance
response = requests.get(
    url='http://localhost:9001/get-relevance',
    params={
        'text': text,
        'classifier': 'has_police',
        'metadata': json.dumps({}),
    },
)
print(response.json())

# get entities
response = requests.get(
    url='http://localhost:9001/get-entities',
    params={
        'text': text,
    },
)
print(response.json())

# get lemmatization
response = requests.get(
    url='http://localhost:9001/get-lemma',
    params={
        'text': text,
    },
)
print(response.json())

# get state abbrevitaions
response = requests.get(
    url='http://localhost:9001/convert-state-abbreviation',
    params={
        'queries': json.dumps(['MiNneapolis', 'New York', 'CA']),
    },
)
print(response.json())



