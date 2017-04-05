"""
Features from: 

@inproceedings{dalip2013exploiting,
  title={Exploiting user feedback to learn to rank answers in q\&a forums: a case study with stack overflow},
  author={Dalip, Daniel Hasan and Gon{\c{c}}alves, Marcos Andr{\'e} and Cristo, Marco and Calado, Pavel},
  booktitle={Proceedings of the 36th international ACM SIGIR conference on Research and development in information retrieval},
  pages={543--552},
  year={2013},
  organization={ACM}
}
"""

import re
from nltk.tokenize import sent_tokenize

def ty_cpc(text):
    """Return the number of words capitalized in @text"""
    regex = r"\b[A-Z]\S+"
    matches = re.findall(regex, text)
    result = len(matches)
    return result


def ty_cpe(text):
    """Return the number of capitalization errors in @text. 
    First letter of a sentence not capitalized"""
    result = 0
    for sent in sent_tokenize(text):
        if len(sent) > 0:
            if not sent[0].isupper():
                result = result + 1
    return result


def ty_poc(text):
    """Return excessive punctuation count.
    Repeated ellipsis, repeated question marks, repeated spacing (irregular).
    """
    result = 0
    # ellipsis
    regex = r"[.]{3}[.]+"
    result = result + len(re.findall(regex, text))
    # repeated question marks
    regex = r"[?]{1}[?]+"
    result = result + len(re.findall(regex, text))
    # irregular spacing
    regex = r"[ ]{1}[ ]+"
    result = result + len(re.findall(regex, text))
    return result

def ty_pde(text):
    """Return punctuation density (percent of all characters)"""
    regex = r"[^a-zA-Z ]"
    result = len(re.findall(regex, text)) / float(len(text))
    return result

def ty_sde(text):
    """Return spacing density (percent of all characters)"""
    regex = r"[ ]"
    result = len(re.findall(regex, text)) / float(len(text))
    return result

def ty_wse(text):
    """Return entropy of the text word sizes (character-level entropy of the text).
    """
    result = 0
    
    return result


def ty_inn(text):
    """
    returns: information to noise
    """
    return 0

def ty_nwnt(text):
    """
    returns: number of words not in WordNet
    """
    return 0

def ty_typo(text):
    """
    returns: number of typo
    """
    return 0

def ty_slp(text):
    """
    returns: size of largest phrase
    """
    return 0

def ty_lpr(text):
    """
    returns: %p where (length - avg. length) >= 10 words
    """
    return 0

def ty_spr(text):
    """
    returns: %p where (avg. length - length) >= 5 words
    """
    return 0

def ty_avc(text):
    """
    returns: number of auxiliary verbs
    """
    return 0

def ty_qc(text):
    """
    returns: number of questions
    """
    return 0

def ty_pc(text):
    """
    returns: number of pronouns
    """
    return 0

def ty_pvc(text):
    """
    returns: numbre of passive voice sentences
    """
    return 0

def ty_cjr(text):
    """
    returns: number of words that are conjunctions
    """
    return 0

def ty_nr(text):
    """
    returns: number of nominalizations
    """
    return 0

def ty_rpr(text):
    """
    returns: number of prepositions
    """
    return 0

def ty_ber(text):
    """
    returns: number of uses of verb "to be"
    """
    return 0

def ty_sp(text):
    """
    returns: #p starting with a pronoun
    """
    return 0

def ty_sa(text):
    """
    returns: #starting with an article
    """
    return 0

def ty_scc(text):
    """
    returns: #starting with a conjunction
    """
    return 0

def ty_sscc(text):
    """
    returns: #p starting with a subordinating conjunction
    """
    return 0

def ty_sipc(text):
    """
    returns: #p starting with an interrogative pronoun
    """
    return 0

def ty_spr(text):
    """
    returns: #p starting with a preposition
    """
    return 0

def ty_klg(text):
    """
    returns: KLD(good answers)
    """
    return 0

def ty_klt(text):
    """
    returns: KLD(good answers of same category)
    """
    return 0

def ty_klwid(text):
    """
    returns: KLD(Wikipedia discussion pages)
    """
    return 0

def ty_klwi(text):
    """
    returns: KLD(Wikipedia pages classified as "Good"
    """
    return 0