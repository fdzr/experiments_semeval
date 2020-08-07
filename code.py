import time
from gensim.models.word2vec import PathLineSentences
from gensim.models import Word2Vec
from scipy import spatial
from collections import defaultdict


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f_in:
        targets = [line.strip() for line in f_in]
    return targets


def replace_all(sentence, sub, targets):
    for target in targets:
        while target in sentence:
            sentence[sentence.index(target)] = f"{target}_{sub}"
    return sentence


def transform_corpus(path, targets, sub):
    corpus = PathLineSentences(path)
    sentences = []

    for sentence in corpus:
        sentences.append(replace_all(sentence, sub, targets))

    return sentences


def train_model(languages):
    path = "test_data_public/"
    models = {}

    for language in languages:
        targets = read_file(f"{path}{language}/targets.txt")
        sentences_corpus_1 = transform_corpus(f"{path}{language}/corpus1/lemma", targets, "t1")
        sentences_corpus_2 = transform_corpus(f"{path}{language}/corpus2/lemma", targets, "t2")
        sentences_corpus_1.extend(sentences_corpus_2)
        corpus = sentences_corpus_1

        model = Word2Vec(corpus, min_count=1, sg=1, size=200, negative=5, window=2)
        models[language]= model

    return models


# This code is implemented just to run one experiment,
# but if you want to execute much more, you need to add
# a loop, or may be two, with all configurations of parameters
# that you wish to include in the experiments.
def main():
    path = "test_data_public/"
    languages = ["english", "german", "latin", "swedish"]
    models = train_model(languages)

    for language in languages:
        targets = read_file(f"{path}{language}/targets.txt")
        ranking = defaultdict(float)

        with open(f"answer/task1/{language}.txt", "w", encoding="utf-8") as f_out:
            for target in targets:
                target_t1 = models[language][f"{target}_t1"]
                target_t2 = models[language][f"{target}_t2"]

                score = 1 - spatial.distance.cosine(target_t1, target_t2)
                ranking[target] = score

                if score <= 0.50:
                    f_out.write('\t'.join((target, str(1) + '\n')))
                else:
                    f_out.write('\t'.join((target, str(0) + '\n')))

        with open(f"answer/task2/{language}.txt", "w", encoding="utf-8") as f_out:
            for key, value in ranking.items():
                f_out.write('\t'.join((key, str(value) + '\n')))


if __name__ == '__main__':
    start_time = time.time()

    main()

    time_total = time.time() - start_time
    hours = round(time_total // 3600, 0)
    min = round((time_total % 3600) // 60, 0)
    sec = round((time_total % 3600) % 60, 0)

    print("time elapsed :", hours, " hours ", min, " min ", sec, " sec ")

    with open("log.txt", "w", encoding="utf-8") as f_out:
        f_out.write(f"time elapsed : {hours} hours, {min} min, {sec} sec")
