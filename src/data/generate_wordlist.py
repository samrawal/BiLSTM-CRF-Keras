import os, sys, pickle, glob
from tqdm import tqdm
PROJ_PATH = open('/tmp/PROJ_PATH.txt', 'r').read().strip()
sys.path.append(PROJ_PATH+'/src/')
from data.n2c2_utils import n2c2Parser

def parse_file(raw_dir, interim_dir, file_number, has_gold):
    raw_file = PROJ_PATH + '/' + raw_dir + '/{0}.txt'.format(file_number)
    ann_file = PROJ_PATH + '/' + raw_dir + '/{0}.ann'.format(file_number)
    clamp_file = PROJ_PATH + '/' + raw_dir + '/../clamp/{0}.xmi'.format(file_number)

    parser = n2c2Parser(raw_file)
    parser.parse_file(clamp_file)
    if has_gold: parser.tag_gold_tokens(ann_file)

    word_list = parser.tokens
    with open(PROJ_PATH + '/' + interim_dir + '/{0}.ser'.format(file_number),
              'wb') as f:
        pickle.dump(parser.tokens, f)

def parse_all_files(raw_dir=None, interim_dir=None, has_gold=True):
    if raw_dir == None:
        raw_dir = PROJ_PATH + '/data/n2c2/train/raw/'
    for f in tqdm(glob.glob(raw_dir+'/*.txt'), 'Intermediate processing'):
        parse_file(raw_dir, interim_dir, f[len(raw_dir):-4], has_gold)

if __name__ == '__main__':
    parse_all_files()
