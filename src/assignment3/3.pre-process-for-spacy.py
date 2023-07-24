#!/usr/bin/env python
# coding: utf-8
# modified from the original: Brad Payne, in order to create Spacy binary files
# original file https://github.com/NorskRegnesentral/text-anonymization-benchmark/blob/master/longformer_experiments/data_manipulation.py
# original author: Norsk Regnesentral
# license: MIT

import spacy
from spacy.tokens import DocBin
import json

with open('../../data/annotated/train_data.json', "r", encoding="utf-8") as f1, open('../../data/annotated/test_data.json', "r", encoding="utf-8") as f3:

    train = json.load(f1)
    test = json.load(f3)

    # TEST, aka DEV in Spacy-land
    nlp = spacy.blank("en")
    db = DocBin()
    for data in test:
        doc = nlp(data['full_text'])
        ents = []
        for annotation in data['spans']:
            span = doc.char_span(annotation['start_position'], annotation['end_position'], label=annotation['entity_type'], alignment_mode="contract")
            if span is not None:
                ents.append(span)
        if ents is not None:
            doc.ents = spacy.util.filter_spans(ents)
        db.add(doc)

    db.to_disk("../../data/annotated/dev.spacy")
    del db, nlp

    # TRAIN
    nlp = spacy.blank("en")
    db = DocBin()
    for data in train:
        doc = nlp(data['full_text'])
        ents = []
        for annotation in data['spans']:
            span = doc.char_span(annotation['start_position'], annotation['end_position'], label=annotation['entity_type'], alignment_mode="contract")
            if span is not None:
                ents.append(span)
        if ents is not None:
            doc.ents = spacy.util.filter_spans(ents)
        db.add(doc)

    db.to_disk("../../data/annotated/train.spacy")
