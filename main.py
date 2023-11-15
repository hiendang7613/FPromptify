%cd /content/FPromptify

import os
import re
import fitz  

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
parser.add_argument('--directory_path', default = 'data_dir/CV')
parser.add_argument('--mode',  default = 'CV', help='CV or JD or ER')
parser.add_argument('--model_name',  default = 'gpt-3.5-turbo')
parser.add_argument('--api_key',  default = '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')
parser.add_argument('--is_continue',  default = True, help = 'continue to label the dataset that not finished')
args = parser.parse_args()
directory_path = args.directory_path
is_continue = args.is_continue


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




def Labeling(text_input, labels):
  nlp_prompter = Prompter(model)
  result = nlp_prompter.fit(mode + '.jinja',
              text_input  = text_input,
              labels      = labels,
              # groups      = groups,
              domain      = 'curriculum vitae')
  return result['text']



def new(path):

  new_path = os.path.join(path, os.path.splitext(file)[0] + ".txt")


  paths = path.split('/')
  # paths[-2] = paths[-2] + '_[labeled]'
  paths[-3] = 'labeled'
  if mode == 'CV':
    paths[-1] = paths[-1].replace('.pdf','.txt')
  return '/'.join(paths)



def read_pdf(path):
    pdf_document = fitz.open(path)
    text = ' '.join([ ' '.join(page.get_text().splitlines()) for page in pdf_document ])
    return text




def process_file(file_name):
    global ocr_files
    global other_error_files

    new_file_name = os.path.splitext(file_name)[0] + ".txt"

    if process_file.file_type == 'pdf':
      text = read_pdf(os.path.join(process_file.in_dir, file_name))
    elif process_file.file_type == 'txt':
    
    else:
      raise 
    


    
    try:
        if mode=='CV':
        else:
          f_open = open(file_path, 'r', encoding='utf-8')
          text = f_open.read()
          f_open.close()
    except Exception as e:
        print(f"Error reading PDF '{file_path}': {e}\n")
        return
    if len(text) < 2:
        print(f"Text too short in '{file_path}'\n")
        ocr_files.append(file_path)
        return

    # Labeling
    loop = True
    while loop:
      try:
          output_text = Labeling(text, labels)
          loop = False
      except Exception as e:
          print(f"Error labeling text in '{file_path}': {e}\n")
          # if 'Rate limit reached' in str(e):
          loop = True
          time.sleep(0.5)
          # else:
          #   other_error_files.append(file_path)
          #   return
    # write to file
    f_write = open(output_path, 'w', encoding='utf-8')
    f_write.write(output_text)
    f_write.close()



def process_files_in_directory(in_dir, out_dir, labels, domain='CV', file_type='pdf' ):
    files = os.listdir(in_dir)
    files = [ file for file in files if file.lower().endswith('.'+file_type)]
    process_file.labels = labels
    process_file.in_dir = in_dir
    process_file.out_dir = out_dir
    process_file.domain = domain
    process_file.file_type = file_type
    with ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(process_file, files), total=len(files)))


if __name__ == '__main__':

    ocr_files = []  # Declare as global variable
    other_error_files = []  # Declare as global variable

    process_files_in_directory(directory_path)
