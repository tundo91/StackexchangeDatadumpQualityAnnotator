# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.feats_extract_binaryBestAnswer

This script reads a src file containing threads with accepted answers.
Each datapoint is flagged with 1 if it's a best/accepted answer, 0 otherwise.
Output datapoints are grouped by thread.
"""

import json
import glob
import os
import logging

from bs4 import BeautifulSoup
import nltk
import dask.bag as db
import dask.multiprocessing

from Analysis.Features import text_style
from Utils import settings_binaryBestAnswer as settings

logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)
nltk.data.path.append('venv/nltk_data')
dask.set_options(get=dask.multiprocessing.get)

# TODO add other funcs
UNARY_FUNCS = [text_style.ty_cpc,
               text_style.ty_cpe,
               text_style.ty_poc,
               text_style.ty_pde,
               text_style.ty_sde,
               text_style.ty_nwnt,
               text_style.ty_typo,
               text_style.ty_slp,
               text_style.ty_avc,
               text_style.ty_pc,
               text_style.ty_pvc,
               text_style.ty_cjr,
               text_style.ty_nr,
               text_style.ty_pr,
               text_style.ty_ber,
               text_style.ty_sp,
               text_style.ty_sa,
               text_style.ty_scc,
               text_style.ty_sscc,
               text_style.ty_sipc,
               text_style.ty_spr,
               ]


#TODO add other funcs + call them in thread_extract()
BINARY_FUNCS = []


def load(thread):
    # read question
    question_body = thread['question']['body']
    question_body_stripped = BeautifulSoup(question_body, "html5lib").get_text()

    # read accepted_answer
    accepted_answer_body = thread['accepted_answer']['body']
    accepted_answer_body_stripped = BeautifulSoup(accepted_answer_body, "html5lib").get_text()

    # read other_answers
    other_answers_body = [answer['body'] for answer in thread['other_answers']]
    other_answers_body_stripped = [BeautifulSoup(answer_body, "html5lib").get_text()
                                   for answer_body in other_answers_body]

    return {
        'thread_id': thread['thread_id'],
        'question_body': question_body,
        'question_body_stripped': question_body_stripped,
        'accepted_answer_body': accepted_answer_body,
        'accepted_answer_body_stripped': accepted_answer_body_stripped,
        'other_answers_body': other_answers_body,
        'other_answers_body_stripped': other_answers_body_stripped
    }


def thread_extract(thread):
    thread_dataset = []

    # extract accepted_answer feats
    datapoint = dict()
    for f in UNARY_FUNCS:
        datapoint[f.__name__] = f(thread['accepted_answer_body_stripped'])
    datapoint['best_answer'] = 1
    datapoint['thread_id'] = thread['thread_id']
    thread_dataset.append(datapoint)

    # extract other_answers feats
    for answer in thread['other_answers_body_stripped']:
        datapoint = dict()
        for f in UNARY_FUNCS:
            datapoint[f.__name__] = f(answer)
        datapoint['best_answer'] = 0
        datapoint['thread_id'] = thread['thread_id']
        thread_dataset.append(datapoint)
    return thread_dataset


def main():
    logging.info('Features extraction: started.')

    # list of delayed values
    bag = db.read_text(settings.SRC_FILE_PATH).map(json.loads, encoding=settings.ENCODING)

    # bag has just one item!
    for data_list in bag:

        if settings.DRAFT_MODE:
            logging.info('Draft mode enabled, using just a sampled dataset.')
            data_list = data_list[:10]
        else:
            logging.info('Draft mode disabled, using whole datasource.')
            logging.debug(len(data_list))

        threads = db.from_sequence(data_list, npartitions=settings.N_PARTITIONS)

        # extract text without html tags
        processed_threads = threads.map(load)

        # extract features, flatten result
        dataset = processed_threads.map(thread_extract).concat()  # dask.bag.core.Bag

        # create output directory
        if not os.path.exists(settings.OUTPUT_PATH_DIR):
            logging.info('Creating output directory in {}.'.format(settings.OUTPUT_PATH_DIR))
            os.makedirs(settings.OUTPUT_PATH_DIR)

        # clear output folder first
        filelist = glob.glob(settings.OUTPUT_PATH_DIR + "*.csv")
        for f in filelist:
            logging.info('Clearing output directory: {}.'.format(f))
            os.remove(f)

        df = dataset.to_dataframe()

        # TODO: make sure divisions/partitions take thread_id into account! Might need switching to PARQUET files
        ##df = df.set_index('thread_id')

        # always use utf-8
        df.to_csv(settings.OUTPUT_PATH_DIR + '*.csv', encoding=settings.ENCODING)

    logging.info('Features extraction: completed.')
if __name__ == "__main__":
    main()