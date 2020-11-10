from mrjob.job import MRJob
from mrjob.step import MRStep
from math import log
from os import environ

word_list = ["the", "for"]

total_files = 3

class MRMostUsedWord(MRJob):
    SORT_VALUES = True

    def mapper_get_word_from_file(self, _, this_line):
        doc_name = environ['map_input_file']
        for word in this_line.split(" "):
            yield (doc_name, word), 1

    def combiner_how_much_words(self, doc_word, occurences):
        yield doc_word, sum(occurences)

    def reducer_how_much_words(self, doc_word, occurences):
        yield doc_word, sum(occurences)
        
    def mapper_restructured_word_and_sum(self, doc_word, summ):
        yield doc_word[0], (doc_word[1], summ)
    
    def reducer_get_sums(self, doc, word_summ):
        gen_summ = 0
        forced_same_words = []
        for _, summ in word_summ:
            gen_summ += summ
            forced_same_words += [(_, summ)]
        for _, __ in forced_same_words:
            yield (doc, _), (__, gen_summ)

    def mapper_restructured_word_and_sums(self, doc_word, summ_fields):
        yield doc_word[1], (doc_word[0], summ_fields[0], summ_fields[1])

    def reducer_get_measurement_structure(self, word, doc_and_summ_fields):
        forced_same = []
        for _, __, ___ in doc_and_summ_fields:
            forced_same += [(_, __, ___)]
        for _, __, ___ in forced_same:
            yield (_, word), (__, ___, total_files, len(forced_same))


    def mapper_set_weight(self, doc_word, measurement_fields):
        yield doc_word[0], (doc_word[1], (measurement_fields[0] / measurement_fields[1]) * log(measurement_fields[2] / measurement_fields[3]))
    
    def reducer_get_full_weight(self, doc, word_tfidf):
        gen_tfidf = 0
        for word, tfidf in word_tfidf:
            if word in word_list:
                gen_tfidf += tfidf
        yield doc, gen_tfidf
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_word_from_file,
                   combiner=self.combiner_how_much_words,
                   reducer=self.reducer_how_much_words),
            MRStep(mapper=self.mapper_restructured_word_and_sum,
                   reducer=self.reducer_get_sums),
            MRStep(mapper=self.mapper_restructured_word_and_sums,
                   reducer=self.reducer_get_measurement_structure),
            MRStep(mapper=self.mapper_set_weight,
                   reducer=self.reducer_get_full_weight)
        ]

if __name__ == '__main__':
    MRMostUsedWord.run()
