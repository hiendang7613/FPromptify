import os
import re
from PyPDF2 import PdfReader
from tqdm.contrib.concurrent import process_map
from functools import partial
from multiprocessing import cpu_count

import json
import time
from collections import defaultdict
import random
import argparse

from promptify import OpenAI
from promptify import Prompter

# read parameters
parser = argparse.ArgumentParser()
parser.add_argument('--directory_path', default='/content/CV/English/')
parser.add_argument('--mode',  default='ner', help='ner or JD') 
parser.add_argument('--model_name',  default='gpt-3.5-turbo') 
parser.add_argument('--api_key',  default='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') 
args = parser.parse_args()
directory_path = args.directory_path #''

mode = args.mode
# ocr_files = []
# other_error_files = []
model_name = args.model_name
api_key = args.api_key
labels = ', '.join([])


try:
    model = OpenAI(api_key, model=model_name)
except Exception as e:
    print("Error initializing OpenAI:", e)


def Labeling(
    text_input,
    labels,
):
  nlp_prompter = Prompter(model)
  result = nlp_prompter.fit(mode+'.jinja',
              text_input  = text_input,
              labels      = labels,
              # groups      = groups,
              domain      = 'curriculum vitae')
  return result['text']

def get_new_path(path):
  paths = path.split('/')
  paths[-2] = paths[-2] + '_labeled'
  if mode=='ner':
    paths[-1] = paths[-1].replace('.pdf','.txt')
  return '/'.join(paths)


def read_pdf(path):
    reader = PdfReader(path)
    text = ' '.join([page.extract_text() for page in reader.pages])
    return text


def process_file(labels, file_path):
    global ocr_files
    global other_error_files

    output_path = get_new_path(file_path)
    dirname = os.path.dirname(output_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if os.path.exists(output_path):
        return
    try:
        if mode=='ner':
          text = read_pdf(file_path)
        else:
          with open(file_path, 'r') as file:
            text = file.read()
    except Exception as e:
        print(f"Error reading PDF '{file_path}': {e}\n")
        return
    if len(text) < 10:
        print(f"Text too short in '{file_path}'\n")
        ocr_files.append(file_path)
        return
    # Labeling
    loop = True
    while loop:
      try:
          text_ner = Labeling(text, labels)
          loop = False
      except Exception as e:
          print(f"Error labeling text in '{file_path}': {e}\n")
          if 'Rate limit reached' in str(e):
            loop = True
            time.sleep(0.5)
          else:
            other_error_files.append(file_path)
            return
    # write to file
    with open(output_path, 'w') as f:
        f.write(text_ner)

def process_files_in_directory(directory_path):
    list_pdf_paths = []
    for root, _, files in os.walk(directory_path):
        if mode=='ner':
          list_pdf_paths.extend([os.path.join(root, filename) for filename in files if filename.endswith('.pdf')])
        else:
          list_pdf_paths.extend([os.path.join(root, filename) for filename in files if filename.endswith('.txt')])
    process_file_partial = partial(process_file, labels)
    process_map(process_file_partial, list_pdf_paths)

if __name__ == '__main__':

    ocr_files = []  # Declare as global variable
    other_error_files = []  # Declare as global variable
    process_files_in_directory(directory_path)
