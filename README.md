# Big Data Course

## Task 1 -- Hadoop Map Reduce

Link: https://synthesis.frccsc.ru/synthesis/student/BigData/seminar-hadoop/lectures2019/%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%B5%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%201.pdf

<strong>Chosen algorithm is <em>TF*IDF</em></strong>

### Run:
```
$ python3 Do.py docs
```
* output example for `main_line = "the for"`
```
"file://docs/f2.txt"	0.0935688711018841
"file://docs/f3.txt"	0.0028621066454693955
"file://docs/f1.txt"	0.0035776333068367446
```
* The metric is calculated as the sum of the <em>tf-idf</em> values of words from the given ones

