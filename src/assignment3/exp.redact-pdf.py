#!/usr/bin/env python
# coding: utf-8

# to run, navigate to the directory where the file lives and run `python ./exp.redact-pdf.py`

# This script is modified by Brad Payne from the original
# Original is licensed with an MIT license, copyright Microsoft Corporation
# Path to original: [https://www.github.com/microsoft/presidio/blob/main/docs/samples/python/example_pdf_annotation.ipynb](https://www.github.com/microsoft/presidio/blob/main/docs/samples/python/example_pdf_annotation.ipynb)

# # Annotating PII in a PDF
#
# This sample takes a PDF as an input, extracts the text, identifies PII using Presidio and annotates the PII using highlight annotations.
#
# ## Prerequisites
# Before getting started, make sure the following packages are installed. For detailed documentation, see the [installation docs](https://microsoft.github.io/presidio/installation).
#
# Install from PyPI:

# !pip install presidio_analyzer
# !pip install presidio_anonymizer
# !python -m spacy download en_core_web_lg
# !pip install pdfminer.six
# !pip install pikepdf
# !pip install os

import os
from os.path import exists

# For Presidio
from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# For console output
from pprint import pprint

# For extracting text
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine

# For updating the PDF
from pikepdf import Pdf, AttachedFileSpec, Name, Dictionary, Array

# ## Analyze the text in the PDF
#
# To extract the text from the PDF, we use the pdf miner library. We extract the text from the PDF at the text container level. This is roughly equivalent to a paragraph.
#
# We then use Presidio Analyzer to identify the PII and it's location in the text.
#
# The Presidio analyzer is using pre-defined entity recognizers, and offers the option to create custom recognizers.
#


for i in range(1, 98):
    if os.path.exists(f"../../data/original-cvs/c{i}.pdf"):
        analyzer = AnalyzerEngine()
        analyzed_character_sets = []
        for page_layout in extract_pages(f"../../data/original-cvs/c{i}.pdf"):
            for text_container in page_layout:
                if isinstance(text_container, LTTextContainer):

                    # The element is a LTTextContainer, containing a paragraph of text.
                    text_to_anonymize = text_container.get_text()

                    # Analyze the text using the analyzer engine
                    analyzer_results = analyzer.analyze(text=text_to_anonymize, language='en')

                    if text_to_anonymize.isspace() == False:
                        #print(text_to_anonymize)
                        print(analyzer_results)

                    characters = list([])

                    # Grab the characters from the PDF
                    for text_line in filter(lambda t: isinstance(t, LTTextLine), text_container):
                        for character in filter(lambda t: isinstance(t, LTChar), text_line):
                            characters.append(character)

                    # Slice out the characters that match the analyzer results.
                    for result in analyzer_results:
                        start = result.start
                        end = result.end
                        analyzed_character_sets.append({"characters": characters[start:end], "result": result})


        # ## Create phrase bounding boxes
        #
        # The next task is to take the character data, and inflate it into full phrase bounding boxes.
        #
        # For example, for an email address, we'll turn the bounding boxes for each character in the email address into one single bounding box.

        # Combine the bounding boxes into a single bounding box.
        def combine_rect(rectA, rectB):
            a, b = rectA, rectB
            startX = min(a[0], b[0])
            startY = min(a[1], b[1])
            endX = max(a[2], b[2])
            endY = max(a[3], b[3])
            return (startX, startY, endX, endY)


        analyzed_bounding_boxes = []

        # For each character set, combine the bounding boxes into a single bounding box.
        for analyzed_character_set in analyzed_character_sets:
            # if isinstance(analyzed_character_set["characters"], list) and 0 < len(analyzed_character_set["characters"]):
            if len(analyzed_character_set["characters"]) == 0:
                continue
            completeBoundingBox = analyzed_character_set["characters"][0].bbox

            for character in analyzed_character_set["characters"]:
                completeBoundingBox = combine_rect(completeBoundingBox, character.bbox)

            analyzed_bounding_boxes.append({"boundingBox": completeBoundingBox, "result": analyzed_character_set["result"]})

        # ## Add highlight annotations
        #
        # We finally iterate through all the analyzed bounding boxes and create highlight annotations for all of them.

        pdf = Pdf.open(f"../../data/original-cvs/c{i}.pdf")

        annotations = []

        # Create a highlight annotation for each bounding box.
        for analyzed_bounding_box in analyzed_bounding_boxes:
            boundingBox = analyzed_bounding_box["boundingBox"]

            # Create the annotation.
            # We could also create a redaction annotation if the ongoing workflows supports them.
            highlight = Dictionary(
                Type=Name.Annot,
                Subtype=Name.Highlight,
                QuadPoints=[boundingBox[0], boundingBox[3],
                            boundingBox[2], boundingBox[3],
                            boundingBox[0], boundingBox[1],
                            boundingBox[2], boundingBox[1]],
                Rect=[boundingBox[0], boundingBox[1], boundingBox[2], boundingBox[3]],
                C=[1, 0, 0],
                CA=0.5,
                T=analyzed_bounding_box["result"].entity_type,
            )

            annotations.append(highlight)

        # Add the annotations to the PDF.
        # for page in range(len(pdf.pages)):
        pdf.pages[0].Annots = pdf.make_indirect(annotations)

        # And save.

        pdf.save(f"../../data/redacted-cvs/c{i}.pdf")

        # delete variables so the loop doesn't take on a cumulative effect
        del analyzed_bounding_box, analyzed_bounding_boxes, analyzed_character_set, analyzed_character_sets, analyzer, analyzer_results, annotations, boundingBox, character, characters, combine_rect, completeBoundingBox, end, highlight, page_layout, pdf, result, start, text_container, text_line, text_to_anonymize

# ## Result
#
# The output from the samples above creates a new PDF. This contains the original content, with text highlight annotations where the PII has been found.
#
# Each text annotation contains the name of the entity found.
#
# ## Note
#
# Before relying on this methodology to detect or markup PII from a PDF, please be aware of the following:
#
# ### Text extraction
#
# We purposely use a different library specifically for extracting text from the PDF. This is because text extraction is hard to get right, and it's worth using a library specifically developed with the purpose in mind.
#
# For more details, see:
#
# [https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html](https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html)
#
# That said, even with a purpose built library, there may be occasions where PII is present and visible in a PDF, but it is not detected by the sample code.
#
# This includes, but is not limited to:
#
# - Text that cannot be reliable extracted to be analyzed. (e.g. incorrect spacing, wrong reading order)
# - Text present in previous iterations of the PDF which is hidden from text extraction. (See incremental editing)
# - Text present in images. (requires OCRing)
# - Text present in annotations.



