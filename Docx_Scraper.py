import zipfile
import xml.etree.ElementTree as ET

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
TEXT = WORD_NAMESPACE + 't'
RUN = WORD_NAMESPACE + 'r'
RUN_PROPS = WORD_NAMESPACE + 'rPr'
UNDERLINE = WORD_NAMESPACE + 'u'

with zipfile.ZipFile('article_annotated.docx') as docx:
    tree = ET.XML(docx.read('word/document.xml'))

for run in tree.iter(RUN):
    text_elem = run.find(TEXT)
    if text_elem is not None:
        text = text_elem.text
        rPr = run.find(RUN_PROPS)
        is_underlined = rPr is not None and rPr.find(UNDERLINE) is not None
        if is_underlined:
            print(text)

