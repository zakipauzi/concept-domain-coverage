import test_extract as te
import code_extract as ce
import pandas as pd
import numpy as np
import os
import logging
import spacy
from pathlib import Path

def run(root):
    # get all the folders in repo - 50 open source Github projects
    dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]
    test_list = []
    code_list = []

    # kw = generate_kw()

    nlp = spacy.load('en_core_web_md')
    nlp.max_length = 4000000

    counter = 1

    for dir in dirlist:
        print('[{}/{}] Extracting {}...'.format(counter, len(dirlist),dir))

        # create output dir
        Path("output_v2/" + dir).mkdir(parents=True, exist_ok=True)

        # extract from test
        test_extracted = te.extract_from_test(root + '\\' + dir + '\\', nlp)
        out_test_file = "output_v2/{}/{}_test.txt".format(dir, dir)

        if test_extracted is not np.nan:
            with open(out_test_file, "w", encoding='utf-8') as text_file:
                text_file.write(test_extracted)

            test_list.append('Test extracted at {}'.format(out_test_file))
        else:
            test_list.append(np.nan)

        # Because there are multiple code files, we do not try catch here.
        code_extracted = ce.extract_from_code(root + '\\' + dir + '\\', nlp)
        out_code_file = "output_v2/{}/{}_code.txt".format(dir,dir)

        if code_extracted is not np.nan:
            with open(out_code_file, "w", encoding='utf-8') as text_file:
                text_file.write(code_extracted)
            code_list.append('Code extracted at {}'.format(out_code_file))
        else:
            code_list.append(np.nan)

        counter+=1


    df_test = pd.DataFrame(list(zip(dirlist,test_list)), columns=['Repo','Test Extraction Status'])
    df_test = df_test.dropna() # remove empty rows

    df_code = pd.DataFrame(list(zip(dirlist,code_list)), columns=['Repo','Code Extraction Status'])
    df_code = df_code.dropna() # remove empty rows

    print('Code and Test extraction completed successfully!')

    return df_code, df_test
