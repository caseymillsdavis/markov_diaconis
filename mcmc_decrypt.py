import sys
import numpy as np
import string
import re
import random

test_f = 'n ahobryufgklxqmwcipsejztvd'

np.set_printoptions(threshold=sys.maxsize)

char_white_list = string.ascii_lowercase +  ' '
#char_white_list = string.ascii_lowercase + \
#        string.digits + string.punctuation + ' '

def clean_text(text):
    text = text.lower()
    text = re.sub('[^' + char_white_list + ']', ' ', text)
    text = re.sub('[ ]{2,}', ' ', text)
    return text

def build_ascii_perm():
    l = list(char_white_list)
    cl = list(l)
    #permute
    for i in range(len(l)):
        r = random.randrange(len(l) - i)
        tmp = l[r]
        l[r] = l[i]
        l[i] = tmp
    return ''.join(l)

def pl(tm, f, data):
    res = 0.0
    for i in range(len(data)-1):
        ic0 = char_white_list.find(f[char_white_list.find(data[i])])
        ic1 = char_white_list.find(f[char_white_list.find(data[i+1])])
        v = tm[ic0][ic1]
        if v > 0.0:
            res += np.log(v)
        else:
            res += -20.0
    return res

def pli(tm, f, data):
    res = 0.0
    fi = list(f)
    for i, c in enumerate(f):
        fi[char_white_list.find(c)] = char_white_list[i]
    fi = ''.join(fi)
    print(f)
    print(char_white_list)
    print(fi)
    for i in range(len(data)-1):
        ic0 = char_white_list.find(fi[char_white_list.find(data[i])])
        ic1 = char_white_list.find(fi[char_white_list.find(data[i+1])])
        v = tm[ic0][ic1]
        if v > 0.0:
            res += np.log(v)
        else:
            res += -20.0
    return res

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(0)

    f_in = open(sys.argv[1], mode='r')
    in_stream = str(f_in.read())
    f_in.close()
    in_stream = clean_text(in_stream)

    with open(sys.argv[2], 'rb') as f:
        trans_mat = np.load(f)

    #print(trans_mat)
    print(trans_mat.sum(axis=0))

    f = str(char_white_list)
    #f = build_ascii_perm()
    plf = pl(trans_mat, f, in_stream)
    plft = pli(trans_mat, test_f, in_stream)
    for i in range(100000):

        #update permutation
        fs = list(f)
        r0 = random.randrange(len(fs))
        r1 = random.randrange(len(fs))
        tmp = fs[r0]
        fs[r0] = fs[r1]
        fs[r1] = tmp
        fs = ''.join(fs)

        plfs = pl(trans_mat, fs, in_stream)
        if (plfs > plf):
            f = fs
            plf = plfs
        elif (random.random() < np.exp(plfs - plf)):
            f = fs
            plf = plfs

        #print('{:d}, {:f}'.format(i, plf))
        if (i+1) % 50 == 0:
            print('pl(test_f): {:f} pl(f): {:f}'.format(plft, plf))
            print(f)
            #print('{:5d} '.format(i+1) + ''.join([char_white_list[test_f.find(c)] for c in in_stream]))
            print('{:5d} '.format(i+1) + ''.join([f[char_white_list.find(c)] for c in in_stream]))
