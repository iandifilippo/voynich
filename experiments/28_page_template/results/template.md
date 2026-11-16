# 28 do pages follow a template?

| text | pages | lines | words tested | G | G shuffled | z | p | G rolled | z rolled | p rolled |
|---|---|---|---|---|---|---|---|---|---|---|
| VMS herbal A, hand 1 (body text) | 75 | 734 | 66 | 134.026 | 140.227 | -0.358 | 0.633 | 144.728 | -0.589 | 0.707 |
| VMS herbal A, hand 1 (everything left in) | 95 | 1220 | 138 | 332.257 | 290.425 | 1.594 | 0.064 | 292.315 | 1.594 | 0.062 |
| VMS pharma A, hand 1 (body text) | 14 | 128 | 21 | 32.604 | 41.962 | -0.983 | 0.816 | 43.067 | -1.076 | 0.856 |
| VMS balneo B, hand 2 (body text) | 19 | 555 | 82 | 231.225 | 176.750 | 2.740 | 0.006 | 193.433 | 1.740 | 0.044 |
| VMS stars B, hand 3 (body text) | 22 | 495 | 85 | 221.882 | 180.559 | 2.165 | 0.020 | 193.004 | 1.332 | 0.098 |
| VMS herbal B, hand 2 (body text) | 18 | 158 | 25 | 58.334 | 50.514 | 0.713 | 0.228 | 51.362 | 0.708 | 0.228 |
| Pliny 16, chapters | 44 | 962 | 72 | 179.720 | 150.998 | 1.612 | 0.062 | 161.098 | 0.965 | 0.156 |
| copying model, 13-line pages (body text) | 184 | 1420 | 150 | 326.806 | 311.557 | 0.587 | 0.283 | 324.691 | 0.080 | 0.469 |

G: how unevenly the frequent words are spread over the top, middle and bottom third of the page. Shuffled: lines of each page in random order. Rolled: each page's lines kept in sequence but started at a random line and, half the time, read bottom to top; this keeps runs of similar lines, so only a position effect that is the same on every page can beat it.

## words that depend most on position: VMS herbal A, hand 1 (body text)

| word | top / middle / bottom | expected | G |
|---|---|---|---|
| shy | 16 / 7 / 2 | 9.6 / 8.4 / 7.0 | 8.780 |
| chol | 45 / 61 / 50 | 60.0 / 52.2 / 43.8 | 6.368 |
| kchol | 2 / 8 / 2 | 4.6 / 4.0 / 3.4 | 5.608 |
| cheor | 4 / 2 / 8 | 5.4 / 4.7 / 3.9 | 5.577 |
| ol | 6 / 10 / 13 | 11.2 / 9.7 / 8.1 | 5.322 |
| qotol | 7 / 1 / 2 | 3.8 / 3.3 / 2.8 | 4.607 |
| okol | 6 / 1 / 5 | 4.6 / 4.0 / 3.4 | 4.307 |
| sho | 11 / 20 / 12 | 16.5 / 14.4 / 12.1 | 4.068 |
| qokchy | 7 / 2 / 7 | 6.2 / 5.3 / 4.5 | 4.065 |
| kchy | 5 / 3 / 8 | 6.2 / 5.3 / 4.5 | 3.673 |
| d | 4 / 10 / 5 | 7.3 / 6.4 / 5.3 | 3.598 |
| cho | 10 / 10 / 15 | 13.5 / 11.7 / 9.8 | 3.574 |

## words that depend most on position: VMS stars B, hand 3 (body text)

| word | top / middle / bottom | expected | G |
|---|---|---|---|
| otal | 19 / 13 / 4 | 12.0 / 12.3 / 11.7 | 10.405 |
| dain | 11 / 6 / 1 | 6.0 / 6.2 / 5.9 | 9.568 |
| otar | 20 / 9 / 6 | 11.6 / 12.0 / 11.4 | 8.862 |
| qoteedy | 6 / 5 / 0 | 3.7 / 3.8 / 3.6 | 8.798 |
| keey | 3 / 1 / 9 | 4.3 / 4.4 / 4.2 | 8.394 |
| oteedy | 18 / 11 / 5 | 11.3 / 11.6 / 11.1 | 7.606 |
| dar | 8 / 1 / 2 | 3.7 / 3.8 / 3.6 | 7.555 |
| y | 10 / 2 / 8 | 6.6 / 6.8 / 6.5 | 6.541 |
| lkeey | 6 / 4 / 13 | 7.6 / 7.9 / 7.5 | 6.010 |
| okaiin | 15 / 28 / 14 | 18.9 / 19.5 / 18.6 | 5.380 |
| qol | 2 / 4 / 9 | 5.0 / 5.1 / 4.9 | 5.347 |
| al | 15 / 27 / 29 | 23.6 / 24.3 / 23.1 | 5.260 |

## words that depend most on position: VMS balneo B, hand 2 (body text)

| word | top / middle / bottom | expected | G |
|---|---|---|---|
| aiin | 5 / 4 / 18 | 10.6 / 8.8 / 7.6 | 17.295 |
| dol | 14 / 7 / 1 | 8.6 / 7.2 / 6.2 | 9.530 |
| qokedy | 54 / 38 / 18 | 43.1 / 36.0 / 30.9 | 8.979 |
| qoteedy | 17 / 3 / 6 | 10.2 / 8.5 / 7.3 | 8.785 |
| chcthy | 14 / 2 / 4 | 7.8 / 6.5 / 5.6 | 8.777 |
| ol | 46 / 59 / 56 | 63.1 / 52.7 / 45.2 | 8.256 |
| qokeey | 14 / 28 / 13 | 21.6 / 18.0 / 15.4 | 8.186 |
| chckhy | 18 / 10 / 3 | 12.2 / 10.1 / 8.7 | 7.465 |
| chey | 17 / 14 / 25 | 22.0 / 18.3 / 15.7 | 6.959 |
| shecthy | 6 / 4 / 0 | 3.9 / 3.3 / 2.8 | 6.714 |
| oteedy | 9 / 2 / 9 | 7.8 / 6.5 / 5.6 | 6.232 |
| otain | 3 / 9 / 8 | 7.8 / 6.5 / 5.6 | 5.635 |
