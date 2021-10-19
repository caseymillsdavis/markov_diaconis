import sys
import numpy as np
import string
import re
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

char_white_list = string.ascii_lowercase +  ' '
#char_white_list = string.ascii_lowercase + \
#        string.digits + string.punctuation + ' '

def clean_text(text):
    text = text.lower()
    text = re.sub('[^' + char_white_list + ']', ' ', text)
    text = re.sub('[ ]{2,}', ' ', text)
    return text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(0)

    f_in = open(sys.argv[1], mode='r')
    in_stream = str(f_in.read())
    f_in.close()
    in_stream = clean_text(in_stream)

    num_chars = len(char_white_list)
    trans_mat = np.zeros((num_chars, num_chars))
    for i in range(len(in_stream)-1):
        ic0 = char_white_list.find(in_stream[i])
        ic1 = char_white_list.find(in_stream[i+1])
        trans_mat[ic0][ic1] += 1.0

    row_sums = trans_mat.sum(axis=1)
    trans_mat = trans_mat / row_sums[:, np.newaxis]
    #row_sums[row_sums == 0] = 1
    #trans_mat = trans_mat / np.sum(trans_mat)
    #print(trans_mat)
    #plt.plot(trans_mat)
    #plt.imshow(trans_mat)
    #plt.show()

    np.savetxt(sys.argv[2] + '.csv', trans_mat, delimiter=",")

    with open(sys.argv[2], 'wb') as f:
        np.save(f, trans_mat)
