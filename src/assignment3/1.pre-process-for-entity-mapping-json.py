#!/usr/bin/env python
# coding: utf-8
# modified from original: Brad Payne
# original file: https://github.com/NorskRegnesentral/text-anonymization-benchmark/blob/master/longformer_experiments/data_manipulation.py
# original author: Norsk Regnesentral
# license: MIT
import json
from itertools import count
from sys import getsizeof
from typing import Dict

"""
Modify the json files so as to be used easier with the data_handling script
We collapse all annotators decisions, and consider them all as equally correct training examples
"""

"""
Spacy: 
PERSON:      People, including fictional.
NORP:        Nationalities or religious or political groups.
FAC:         Buildings, airports, highways, bridges, etc.
ORG:         Companies, agencies, institutions, etc.
GPE:         Countries, cities, states.
LOC:         Non-GPE locations, mountain ranges, bodies of water.
PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
EVENT:       Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART: Titles of books, songs, etc.
LAW:         Named documents made into laws.
LANGUAGE:    Any named language.
DATE:        Absolute or relative dates or periods.
TIME:        Times smaller than a day.
PERCENT:     Percentage, including ”%“.
MONEY:       Monetary values, including unit.
QUANTITY:    Measurements, as of weight or distance.
ORDINAL:     “first”, “second”, etc.
CARDINAL:    Numerals that do not fall under another type.

Text Anonymization Benchmark:
PERSON:	    Names of people, including nicknames/aliases, usernames and initials
CODE:	    Numbers and codes that identify something, such as SSN, phone number, passport number, license plate
LOC:	    Places and locations, such as: Cities, areas, countries, etc. Addresses Named infrastructures (bus stops, bridges, etc.)
ORG:	    Names of organisations, such as: public and private companies schools, universities, public institutions, prisons, healthcare institutions non-governmental organisations, churches, etc.
DEM:	    Demographic attribute of a person, such as: Native language, descent, heritage, ethnicity Job titles, ranks, education Physical descriptions, diagnosis, birthmarks, ages
DATETIME:	Description of a specific date (e.g. October 3, 2018), time (e.g. 9:48 AM) or duration (e.g. 18 years).
QUANTITY:	Description of a meaningful quantity, e.g. percentages or monetary values.
MISC:	    Every other type of information that describes an individual and that does not belong to the categories above

{"Tab": "Spacy"}
"""
translator = {
    "LOC": "GPE",
    "DATETIME": "DATE",
}
def update_entity_types(swap:str, entity_mapping:Dict[str,str]):
    """Replace entity types using a translator dictionary."""
    if swap in entity_mapping.keys():
        return entity_mapping[swap]
    else:
        return swap

def de_dupe(duplicated_list:list):
    deduplicated_list = list()
    for item in duplicated_list:
        if item not in deduplicated_list:
            deduplicated_list.append(item)
    return deduplicated_list

with open('../../data/annotated/echr_train.json', "r", encoding="utf-8") as f1, open('../../data/annotated/echr_dev.json', "r", encoding="utf-8") as f2, open('../../data/annotated/echr_test.json', "r", encoding="utf-8") as f3:

    train = json.load(f1)
    dev = json.load(f2)
    test = json.load(f3)

    training_raw = []
    dev_raw = []
    test_raw = []

    # the following entities overlap with entities in the pretrained Spacy model
    overlap = ['QUANTITY', 'MISC', 'CODE']

    for ann_data in train:
        dct = {}
        for annotator in ann_data['annotations']:
            dct['full_text'] = ann_data['text']
            annotations = []
            for annotation in ann_data['annotations'][annotator]['entity_mentions']:
                span = {
                    'entity_type': update_entity_types(annotation['entity_type'], translator),
                    'entity_value': annotation['span_text'],
                    'start_position': annotation['start_offset'],
                    'end_position': annotation['end_offset']
                }
                if span['entity_type'] not in overlap:
                    annotations.append(span)
            dct['spans'] = annotations
            training_raw.append(dct)
    print("TR", len(training_raw))
    # merging 'dev' into 'training dataset' is intentional, as Spacy doesn't require a dev dataset
    for ann_data in dev:
        dct = {}
        for annotator in ann_data['annotations']:
            dct['full_text'] = ann_data['text']
            annotations = []
            for annotation in ann_data['annotations'][annotator]['entity_mentions']:
                span= {
                    'entity_type': update_entity_types(annotation['entity_type'], translator),
                    'entity_value': annotation['span_text'],
                    'start_position': annotation['start_offset'],
                    'end_position': annotation['end_offset']
                }
                if span['entity_type'] not in overlap:
                    annotations.append(span)
            dct['spans'] = annotations
            training_raw.append(dct)
    print("TR2", len(training_raw))
    for ann_data in test:
        dct = {}
        for annotator in ann_data['annotations']:
            dct['full_text'] = ann_data['text']
            annotations = []
            for annotation in ann_data['annotations'][annotator]['entity_mentions']:
                span= {
                    'entity_type': update_entity_types(annotation['entity_type'], translator),
                    'entity_value': annotation['span_text'],
                    'start_position': annotation['start_offset'],
                    'end_position': annotation['end_offset']
                }
                if span['entity_type'] not in overlap:
                    annotations.append(span)
            dct['spans'] = annotations
            test_raw.append(dct)
    print("TE", len(test_raw))
de_duped_training = de_dupe(training_raw)
de_duped_test = de_dupe(test_raw)
print("TR-dd", len(de_duped_training))
print("TE-dd", len(de_duped_test))

with open('../../data/annotated/train_data.json', 'w', encoding='utf-8') as f1:
    json.dump(de_duped_training, f1, ensure_ascii=False, indent=4)
with open('../../data/annotated/test_data.json', 'w', encoding='utf-8') as f3:
    json.dump(de_duped_test, f3, ensure_ascii=False, indent=4)
