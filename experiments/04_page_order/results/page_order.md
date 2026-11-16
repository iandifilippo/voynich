# 04 page order

225 pages with 40+ words. Mean cosine similarity of word counts between consecutive pages:

- current order: **0.366**
- random order: 0.217 (p = 0.0000)
- shuffled only within same hand + illustration type: 0.314 (p = 0.0000)

If the second p is small, neighbouring pages share vocabulary beyond what hand and topic explain.

## same leaf vs across leaves

- recto->verso of the same leaf (98 joins): mean cos 0.415
- verso->next recto (99 joins): mean cos 0.329
- difference 0.086, permutation p = 0.0006

Same test with measures that down-weight frequent words:

| measure | same_leaf | cross_leaf | diff | p |
|---|---|---|---|---|
| tfidf_cosine | 0.116 | 0.085 | 0.031 | 0.015 |
| jaccard_no_top50 | 0.094 | 0.068 | 0.026 | 0.000 |

## weakest joins in the current order

| from | to | cos | hand | section |
|---|---|---|---|---|
| f68r1 | f68r2 | 0.026 | 4->4 | A->A |
| f24v | f25r | 0.035 | 1->1 | H->H |
| f67v1 | f68r1 | 0.044 | 4->4 | A->A |
| f67v2 | f67v1 | 0.059 | 4->4 | C->A |
| f53r | f53v | 0.075 | 1->1 | H->H |
| f96r | f96v | 0.077 | 1->1 | H->H |
| f43v | f44r | 0.084 | 2->1 | H->H |
| f57r | f57v | 0.087 | 5->1 | H->C |
| f49v | f50r | 0.090 | 1->2 | H->H |
| f58v | f65v | 0.095 | 3->3 | S->H |
| f47v | f48r | 0.100 | 1->5 | H->H |
| f52v | f53r | 0.106 | 1->1 | H->H |
| f48r | f48v | 0.109 | 5->5 | H->H |
| f95v1 | f96r | 0.111 | 3->1 | H->H |
| f41v | f42r | 0.113 | 5->1 | H->H |
| f93v | f94r | 0.114 | 1->3 | H->H |
| f48v | f49r | 0.114 | 5->1 | H->H |
| f42v | f43r | 0.121 | 1->2 | H->H |
| f96v | f99r | 0.122 | 1->1 | H->P |
| f86v3 | f87r | 0.122 | 2->1 | C->H |

## strongest joins

| from | to | cos | hand | section |
|---|---|---|---|---|
| f77v | f78r | 0.674 | 2->2 | B->B |
| f81r | f81v | 0.679 | 2->2 | B->B |
| f76v | f77r | 0.694 | 2->2 | B->B |
| f107r | f107v | 0.696 | 3->3 | S->S |
| f75r | f75v | 0.722 | 2->2 | B->B |
| f78r | f78v | 0.731 | 2->2 | B->B |
| f84r | f84v | 0.749 | 2->2 | B->B |
| f108v | f111r | 0.768 | 3->3 | S->S |
| f80r | f80v | 0.771 | 2->2 | B->B |
| f103r | f103v | 0.784 | 3->3 | S->S |
