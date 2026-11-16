# 15 repeats

Rates per 1000 adjacent word pairs. `ratio` = observed / whole-text shuffle.

| text | exact_per_1000 | exact_shuffled_in_line | exact_shuffled_all | exact_ratio | near_per_1000 | near_shuffled_in_line | near_shuffled_all | near_ratio |
|---|---|---|---|---|---|---|---|---|
| VMS all | 9.371 | 9.216 | 3.423 | 2.738 | 36.020 | 30.636 | 16.904 | 2.131 |
| VMS Currier A | 9.820 | 9.324 | 5.039 | 1.949 | 41.038 | 32.003 | 19.103 | 2.148 |
| VMS Currier B | 9.221 | 9.446 | 4.188 | 2.202 | 33.728 | 30.792 | 20.242 | 1.666 |
| VMS Takahashi | 9.639 | 9.022 | 3.316 | 2.907 | 34.330 | 30.176 | 16.084 | 2.134 |
| Latin_Aix | 0.000 | 4.434 | 6.013 | 0.000 | 1.575 | 3.081 | 3.889 | 0.405 |
| Rettorica | 0.188 | 8.066 | 6.955 | 0.027 | 7.050 | 16.905 | 19.847 | 0.355 |
| Agrippa_Book1 | 0.563 | 14.848 | 14.027 | 0.040 | 19.238 | 12.205 | 9.765 | 1.970 |
| Secreta_Secretorum_LAT | 0.263 | 13.459 | 12.537 | 0.021 | 3.563 | 7.864 | 8.496 | 0.419 |
| Naibbe | 1.327 | 3.123 | 3.943 | 0.336 | 11.424 | 12.983 | 14.192 | 0.805 |
| Naibbe + autokey | 1.780 | 3.649 | 4.283 | 0.416 | 11.456 | 14.029 | 15.095 | 0.759 |

## adjacency beyond line composition (300 within-line shuffles)

| text | exact | exact_null_mean | exact_p_higher | near | near_null_mean | near_p_higher |
|---|---|---|---|---|---|---|
| VMS all | 9.371 | 9.252 | 0.417 | 36.020 | 30.777 | 0.000 |
| VMS Currier A | 9.820 | 9.438 | 0.343 | 41.038 | 31.913 | 0.000 |
| VMS Currier B | 9.221 | 9.259 | 0.547 | 33.728 | 30.613 | 0.000 |

## position of exact repeats in the line (VMS)

| position | repeats | pairs | per_1000 |
|---|---|---|---|
| first pair | 14 | 4103 | 3.412 |
| middle | 250 | 22585 | 11.069 |
| last pair | 24 | 4045 | 5.933 |

## across line breaks

Last word of a line = first word of the next line: 6 of 3390 (expected by frequency 11.8).

## words that repeat most

| word | repeats | expected | ratio | frequency |
|---|---|---|---|---|
| chol | 24 | 3.613 | 6.643 | 378 |
| qokeedy | 18 | 2.383 | 7.553 | 307 |
| qokedy | 16 | 1.926 | 8.307 | 276 |
| qokeey | 12 | 2.321 | 5.169 | 303 |
| daiin | 11 | 16.878 | 0.652 | 817 |
| ol | 9 | 7.130 | 1.262 | 531 |
| shedy | 9 | 4.546 | 1.980 | 424 |
| chedy | 9 | 6.171 | 1.459 | 494 |
| dy | 8 | 1.518 | 5.271 | 245 |
| chor | 7 | 1.094 | 6.399 | 208 |
| ar | 7 | 2.770 | 2.527 | 331 |
| shol | 6 | 0.810 | 7.406 | 179 |
| okaiin | 6 | 1.052 | 5.702 | 204 |
| or | 6 | 3.387 | 1.771 | 366 |
| okeey | 5 | 0.639 | 7.822 | 159 |
| qotedy | 4 | 0.191 | 20.900 | 87 |
| okedy | 4 | 0.300 | 13.315 | 109 |
| chdy | 4 | 0.489 | 8.188 | 139 |
| otaiin | 4 | 0.503 | 7.957 | 141 |
| qol | 4 | 0.510 | 7.845 | 142 |
| shor | 3 | 0.228 | 13.146 | 95 |
| qoteedy | 3 | 0.146 | 20.541 | 76 |
| qokain | 3 | 1.968 | 1.524 | 279 |
| qokal | 3 | 0.922 | 3.252 | 191 |
| otain | 3 | 0.223 | 13.427 | 94 |

## commonest near-repeats

| pair | count |
|---|---|
| o l | 21 |
| ar al | 16 |
| qokedy qokeedy | 15 |
| qokeedy qokedy | 12 |
| or ol | 10 |
| okeey qokeey | 9 |
| daiin dain | 9 |
| qokeey qokedy | 9 |
| qokeedy qokeey | 9 |
| qokeey qokeedy | 9 |
| chor chol | 8 |
| l s | 8 |
| ar or | 8 |
| dar ar | 8 |
| or ar | 8 |
| shedy chedy | 8 |
| al ar | 8 |
| chol chor | 7 |
| chol shol | 7 |
| okaiin otaiin | 7 |

## what changes between near-repeats

delete 313, insert 296, r->l 51, l->r 42, k->t 37, t->k 35, o->l 28, c->s 23, s->c 21, o->a 18, a->o 16, y->o 13, o->y 12, r->m 11, e->d 10, l->s 9, k->d 8, s->y 7, d->k 7, d->e 7
