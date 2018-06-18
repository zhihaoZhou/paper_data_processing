def is_cont(prev, cur):
    if len(cur) < 3 or len(prev) < 3 or len(cur) != len(prev):
        return False
    if cur[2:] != prev[2:]:
        return False
    if prev[:2] == 'B-' and cur[:2] == 'I-':
        return True
    if prev[:2] == 'I-' and cur[:2] == 'I-':
        return True
    return False


def join_tag(sent):
    """
    :param sent: sentence as a list of words
    :return: joined sentence as a list of words
    """
    new_sent = []
    prev = ''
    for word in sent:
        if not is_cont(prev, word):
            new_sent.append(word)
        prev = word
    return new_sent


if __name__ == "__main__":
    f_name = 'bio/abstracts_only_result.bio'
    f_out = open('template.txt', 'w')
    f = open(f_name)
    sent = []
    for line in f:
        line = line.strip()
        if not line:
            sent = join_tag(sent)
            f_out.write(' '.join(sent) + ' <eos>\n')
            sent = []
            continue
        line_list = line.split(' ')
        try:
            tag = line_list[3]
        except IndexError:
            continue
        if tag == 'O':
            sent.append(line_list[0])
        else:
            sent.append(tag)

    f.close()
