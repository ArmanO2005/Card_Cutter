from sentence_transformers import SentenceTransformer, util
import itertools
from docx import Document
import openai
import json
import spacy
from spacy.cli import download


with open('secrets.json') as f:
    creds = json.load(f)


openai.api_key = creds["apikey"]
download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")



class vectorizer:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, sentence):
        return self.model.encode(sentence, convert_to_tensor=True)
    
    def similarity(self, vector, prompt_vec):
        return util.pytorch_cos_sim(vector, prompt_vec).item()


#todo create subsets of a certain length or less
def ordered_combinations(iterable, length):
    items = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(items, r) for r in range(1, length+1)
    )


def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return "\n".join(full_text)


def llmd_prompt(prompt, article):
    full_prompt = "in 7-10 words, restate the prompt as best you can only using words from the article. Your response should should not include uncertain language. Your response should be no longer than 15 words: " + prompt + "\n\nArticle:\n" + article
    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[
            {"role": "system", "content": "You summarize and synthesize articles in a decisive and argumentative manner in 15 words or less."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()


def clause_seperator(text):
    doc = nlp(text)
    clauses = []
    clause = []

    for token in doc:
        clause.append(token.text)
        if token.dep_ in ("ccomp", "advcl", "relcl", "conj") and token.head.dep_ != "ROOT":
            clauses.append(" ".join(clause).strip())
            clause = []
    if clause:
        clauses.append(" ".join(clause).strip())
    return clauses
