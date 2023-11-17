import markdown
import logging
import re
import string
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

logging.basicConfig(level=logging.DEBUG)

stop_words = set(stopwords.words('english'))

html_re = re.compile('<.*?>')
code_re = re.compile('<code>.*?</code>', flags=re.DOTALL)
alpha_re = re.compile('[^a-zA-Z ]+')

def extract_from_doc(folder, project_name, nlp):

    filename1 = folder + 'README.md'
    filename2 = folder + 'README.txt'

    try:
        f = open(filename1, 'r', encoding='utf-8')
    except:
        f = open(filename2, 'r', encoding='utf-8')
        text_md = clean(f.read(), project_name, nlp)
        text_md_len = len(text_md)
        text_md = ' '.join(text_md)

        return text_md, text_md_len

    try:
        text_md = markdown.markdown(f.read())
        text_md = clean(text_md, project_name, nlp)
        text_md_len = len(text_md)
        text_md = ' '.join(text_md)
        f.close()
    except:
        logging.debug('Error occurred when reading README of {}'.format(folder))
        f.close()
        return np.nan

    return text_md, text_md_len


def clean(text, project_name, nlp):
    text = re.sub(code_re, '', text)
    text = re.sub(html_re, '', text)

    # removing non-English characters
    text = re.sub("([^\x00-\x7F])+"," ",text)

    # convert to list for further cleaning
    doc_text = text.split('\n')
    doc_text = [x.strip() for x in doc_text]

    # remove extra code denoted by ```
    doc_text = remove_code_blocks(doc_text)

    # cleaning of punct & lower
    doc_text = [x.lower() for x in doc_text]

    doc_text = [re.sub(alpha_re, '', x) for x in doc_text]

    doc_text = ' '.join(doc_text)

    # nltk word word_tokenize
    doc_text = word_tokenize(doc_text)

    doc_text = [word for word in doc_text if (len(word)>2 and word not in stop_words and word not in project_name)]

    doc_text = [x.lemma_ for x in nlp(' '.join(doc_text))]

    return doc_text


def remove_code_blocks(old_text):
    start = True
    cont = False

    new_text = []

    for x in old_text:
        if x.startswith('```'):
            if start:
                start = False
                cont = True
            else:
                start = True
                cont = False
        else:
            if not cont:
                new_text.append(x)

    return new_text

def isEnglish(s):
    s.isascii()

def isOnlyEnglish(s):
    char_set = string.ascii_letters
    return all((True if x in char_set else False for x in s))
