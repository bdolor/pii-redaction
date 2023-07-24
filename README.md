# Virtual Environment Setup

```bash
python -m venv ./venv
source venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

## Copyright Notices
### ECHR datasets:
Annotated datasets (`data/annoated/echr*`) are released under an MIT license. Copyright (C) 2021-2026 Norsk Regnesentral
https://github.com/NorskRegnesentral/text-anonymization-benchmark

### CVs 
PDF versions located in `data/original-cvs`
ref: https://github.com/warynice/Resume-Classifier/

### Resume Data
JSON version located at `data/anotated/resumedata.json`
ref: https://www.kaggle.com/datasets/dataturks/resume-entities-for-ner

### Fake Name Generator
CSV located at `data/FakeNameGenerator.com_July_2023.csv`
Fake Name Generator identities by the Fake Name Generator are licensed under a Creative Commons Attribution-Share Alike 3.0 United States License. Fake Name Generator and the Fake Name Generator logo are trademarks of Corban Works, LLC.

### Longformer
Longformer is released under an Apache 2.0 license. Copyright Allen Institute for AI.
ref: https://github.com/allenai/longformer
```
@article{Beltagy2020Longformer,
  title={Longformer: The Long-Document Transformer},
  author={Iz Beltagy and Matthew E. Peters and Arman Cohan},
  journal={arXiv:2004.05150},
  year={2020},
}
```
