import sys
import random
import string
import re

char_white_list = string.ascii_lowercase +  ' '
#char_white_list = string.ascii_lowercase + \
#        string.digits +  string.punctuation + ' '

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
        tmp = l[i+r]
        l[i+r] = l[i]
        l[i] = tmp
    return ''.join(l)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(0)
    f_in = open(sys.argv[1], mode='r')
    in_stream = str(f_in.read())
    f_in.close()
    in_stream = clean_text(in_stream)
    s = build_ascii_perm()
    print(in_stream)
    print(char_white_list)
    print(s)
    out_stream = [s[char_white_list.find(i)] for i in in_stream]
    f_out = open(sys.argv[2], mode='w')
    f_out.write(''.join(out_stream))
    f_out.close()
