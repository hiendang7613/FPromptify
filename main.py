import os
import fitz  
import json
import argparse
from promptify import NERLabeler, find_substrings
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor



class LabelerPipeline:
    def __init__(self, labler, labels, domain='CV', file_type='pdf'):
        self.labler = labler
        self.labels = labels
        self.domain = domain
        self.file_type = file_type

    def read_pdf(path):
        pdf_document = fitz.open(path)
        text = ' '.join([ ' '.join(page.get_text().splitlines()) for page in pdf_document ])
        return text
    def read_txt(path):
        f = open(path, 'r', encoding='utf-8' )
        text = f.read()
        f.close()
        return text

    def process_file(self, file_name):
        other_error_files = []
        new_file_name = os.path.join(self.out_dir, os.path.splitext(file_name)[0] + ".txt")
        in_file_path = os.path.join(self.in_dir, file_name)
        if os.path.exists(new_file_name):
            print(f"File '{new_file_name}' already exists. Skipping...")
            return

        # read input file
        try:
            if self.file_type == 'pdf':
                text = LabelerPipeline.read_pdf(in_file_path)
            elif self.file_type == 'txt':
                text = LabelerPipeline.read_txt(in_file_path)
            else:
                raise 'Error file_type ' + self.file_type
        except Exception as e:
            print(f"Error reading PDF '{in_file_path}': {e}\n")
        
        if len(text) < 5:
            print(f"Text too short in {in_file_path}")
            return

        # Labeling
        loop = True
        while loop:
            try:
                output_json = asyncio.run(self.labler.request(text=text))
                loop = False
            except Exception as e:
                print(f"Error labeling text in '{in_file_path}': {e}\n")
                if 'Rate limit reached' in str(e):
                    loop = True
                    time.sleep(0.5)
                else:
                    other_error_files.append(in_file_path)
                    return

        # write to file
        f_write = open(new_file_name, 'w', encoding='utf-8')
        f_write.write(output_json)
        f_write.close()


    def run(self, in_dir, out_dir):
        self.in_dir = in_dir
        self.out_dir = out_dir

        files = os.listdir(in_dir)
        files = [ file for file in files if file.lower().endswith('.'+self.file_type)]

        with ThreadPoolExecutor() as executor:
            list(tqdm(executor.map(self.process_file, files), total=len(files)))
        # self.process_file(files[0])
        # return


if __name__ == '__main__':

    in_dir='/Users/apple/FPromptify/CV_txt/English'
    out_dir='/Users/apple/FPromptify/CV_txt_labeled/English'
    labels_json_path = '/Users/apple/FPromptify/labels.json'
    os.makedirs(out_dir, exist_ok=True)

    api_key="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"
    model="gpt-3.5-turbo"
    domain='CV'
    mode='NER_cv_eng'
    file_type='txt' 

    with open(labels_json_path) as f:
        labels = json.load(f)
    labler = NERLabeler(api_key, labels, model=model, mode=mode)
    pipeline = LabelerPipeline(labler, labels, file_type=file_type)
    pipeline.run(in_dir, out_dir)
