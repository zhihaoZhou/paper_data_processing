from collections import defaultdict


borrowed_ngram_set_sys = set()
borrowed_ngram_set_human = set()
new_ngram_hum = set()


def get_ngrams(word_list, all_ngrams, n):
    for i in range(len(word_list) - n + 1):
        n_gram = []
        for j in range(n):
            n_gram.append(word_list[i+j])
        n_gram = tuple(n_gram)
        all_ngrams[n_gram] += 1


def get_ngrams_from_file(f_name, n):
    all_ngrams = defaultdict(int)
    f = open(f_name)
    i = 0
    for line in f:
        if i % 3 == 1:
            line_list = line.split()
            get_ngrams(line_list, all_ngrams, n)
        i += 1
    f.close()
    return all_ngrams


def percent_overlap(ngrams, ref_ngrams):
    count = 0
    for ngram in ngrams.keys():
        if ngram in ref_ngrams:
            count += 1
    return float(count)/len(ngrams)


def percent_overlap_running(ngrams, ref_ngrams, is_sys):
    total_running = 0
    for ngram in ngrams.keys():
        total_running += ngrams[ngram]
    borrowed_running = 0
    for ngram in ngrams.keys():
        for i in range(ngrams[ngram]):
            if ngram in ref_ngrams:
                if is_sys:
                    borrowed_ngram_set_sys.add(ngram)
                else:
                    borrowed_ngram_set_human.add(ngram)
                borrowed_running += 1
            else:
                if not is_sys:
                    new_ngram_hum.add(ngram)

    return float(borrowed_running)/total_running


def n_gram_stats(n):
    ref_f = "train.dat"
    ref_ngrams = get_ngrams_from_file(ref_f, n)
    print("training contains %d unique %d-grams" % (len(ref_ngrams), n))

    sys_f = "fake2.dat"
    sys_ngrams = get_ngrams_from_file(sys_f, n)
    print("sys contains %d unique %d-grams" % (len(sys_ngrams), n))

    test_f = "dev.dat"
    test_ngrams = get_ngrams_from_file(test_f, n)
    print("human contains %d unique %d-grams" % (len(test_ngrams), n))

    perc = percent_overlap_running(sys_ngrams, ref_ngrams, True)
    print("sys uses %f percent %d-grams from training" % (perc * 100, n))

    perc = percent_overlap_running(test_ngrams, ref_ngrams, False)
    print("human uses %f percent %d-grams from training" % (perc * 100, n))
    print("~"*40)


if __name__ == "__main__":
    for i in range(1, 7):
        n_gram_stats(i)




    # n_gram_stats(1)
    # # print(len(borrowed_ngram_set_sys))
    # # print(len(borrowed_ngram_set_human))
    # both_sys_and_hum = borrowed_ngram_set_sys & borrowed_ngram_set_human
    # # print(len(both_sys_and_hum))
    #
    # # for ngram in both_sys_and_hum:
    # #     my_str = ''
    # #     for i in range(len(ngram)):
    # #         my_str += ngram[i] + ' '
    # #     print(my_str)
    #
    # print(len(new_ngram_hum))
    # for ngram in new_ngram_hum:
    #     my_str = ''
    #     for i in range(len(ngram)):
    #         my_str += ngram[i] + ' '
    #     print(my_str)
