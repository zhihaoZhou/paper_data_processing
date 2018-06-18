import numpy as np


if __name__ == "__main__":
    len_list = []
    ref_f = "train.dat"
    f = open(ref_f)
    i = 0
    for line in f:
        i += 1
        if i % 3 == 1:
            print(line)
            len_list.append(len(line.split()))
    len_list = np.array(len_list)
    print(np.average(len_list))
