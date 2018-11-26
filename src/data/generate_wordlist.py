import os, sys, pickle, glob
from tqdm import tqdm
PROJ_PATH = open('/tmp/PROJ_PATH.txt', 'r').read().strip()
sys.path.append(PROJ_PATH+'/src/')
from data.n2c2_utils import n2c2Parser

def parse_file(file_number, has_gold):
    raw_file = PROJ_PATH + '/data/n2c2/raw/{0}.txt'.format(file_number)
    ann_file = PROJ_PATH + '/data/n2c2/raw/{0}.ann'.format(file_number)
    clamp_file = PROJ_PATH + '/data/n2c2/clamp/{0}.xmi'.format(file_number)

    parser = n2c2Parser(raw_file)
    parser.parse_file(clamp_file)
    parser.tag_gold_tokens(ann_file)

    word_list = parser.tokens
    with open(PROJ_PATH+'/data/n2c2/interim/{0}.ser'.format(file_number),
              'wb') as f:
        pickle.dump(parser.tokens, f)

def parse_all_files(directory=None, has_gold=True):
    if directory == None:
        directory = PROJ_PATH + '/data/n2c2/raw/'
    for f in tqdm(glob.glob(directory+'/*.txt'), 'Intermediate processing'):
        parse_file(f[len(directory):-4], has_gold)

if __name__ == '__main__':
    parse_all_files()
