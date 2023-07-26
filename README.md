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

### PDF redaction 
slightly modified script `src/assignment3/redact-pdf.py` from the original to loop over more than one PDF and deal with multiple paged PDFs.
Original is licensed with an MIT licensed, copyright Microsoft Corporation 
ref: https://github.com/microsoft/presidio/blob/main/docs/samples/python/example_pdf_annotation.ipynb
