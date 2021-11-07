import random

# read in file


def file_to_trigram(file_name):
    file = open(file_name, "r", encoding="utf-8")
    tokens = []
    for line in file:
        tokens.extend(line.split())
    file.close()
    return tokens

# find the most probable tail, with 2 head words


def find_tails(head_word_1, head_word_2, words):
    tails = []
    weights = []
    d = dict()
    for i in range(len(words) - 2):
        if words[i] == head_word_1 and words[i + 1] == head_word_2:
            d[words[i + 2]] = d.get(words[i + 2], 0) + 1
    for key, value in d.items():
        tails.append(key)
        weights.append(value)
    most_prob_tail = random.choices(tails, weights, k=1)
    return most_prob_tail[0]

# check whether a word is a start word


def is_head_1(word):
    if word[0].isupper() and not word.endswith(('.', '!', '?')):
        return True
    return False

def is_head_2(word):
    if not word.endswith(('.', '!', '?')):
        return True
    return False

def is_end(word):
    if word.endswith(('.', '!', '?')):
        return True
    return False

def generate_end(words):
    while True:
        end_word = random.choice(words[2:])
        if is_end(end_word):
            return end_word

# start generate random sentence


def main():
    seed = 100023
    random.seed(seed)
    num_of_sentence = 10

    file_name = input()
    trigram = file_to_trigram(file_name)
    head_1, head_2 = "", ""

    for i in range(num_of_sentence):
        sentence = ""
        if (head_1 == "" or head_2 == "" or not is_head_1(head_1) or not is_head_2(head_2)
                or head_1 == trigram[-2] or head_1 == trigram[-1] or head_2 == trigram[-1]):
            while True:
                head_index = random.randint(0, len(trigram) - 3)
                head_1, head_2 = trigram[head_index], trigram[head_index + 1]
                if is_head_1(head_1) and is_head_2(head_2):
                    break

        sentence += head_1 + " " + head_2 + " "
        sentence_len = 2
        while True:
            next_word = find_tails(head_1, head_2, trigram)
            sentence += next_word + " "
            head_1, head_2 = head_2, next_word
            sentence_len += 1
            if sentence_len >= 5 and is_end(head_2):
                break
        sentence = sentence[:-1]
        print(sentence)


if __name__ == '__main__':
    main()

