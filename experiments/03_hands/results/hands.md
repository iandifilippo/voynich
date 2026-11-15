# 03 hands and Currier languages

## vocabulary distance between hands (JSD, bits)

| a | b | jsd |
|---|---|---|
| hand 2 | hand 3 | 0.273 |
| hand 2 | hand 5 | 0.457 |
| hand 3 | hand 4 | 0.496 |
| hand 1 | hand 3 | 0.506 |
| hand 1 | hand 2 | 0.511 |
| hand 3 | hand 5 | 0.512 |
| hand 2 | hand 4 | 0.518 |
| hand 1 | hand 4 | 0.529 |
| hand 4 | hand 5 | 0.593 |
| hand 1 | hand 5 | 0.612 |

## hand vs Currier language (tokens)

| hand | A | B |
|---|---|---|
| 1 | 10749 | 0 |
| 2 | 0 | 11128 |
| 3 | 750 | 10908 |
| 4 | 0 | 528 |
| 5 | 0 | 925 |

## share of each hand's tokens that are words also used by another hand

| hand | tokens | types | tokens_with_shared_word |
|---|---|---|---|
| 1 | 10927 | 3180 | 0.769 |
| 2 | 11128 | 2534 | 0.878 |
| 3 | 11708 | 3302 | 0.821 |
| 4 | 3570 | 1748 | 0.732 |
| 5 | 925 | 558 | 0.822 |

## most characteristic words per hand (log-odds z)

- hand 1: daiin (492/357, z=18.5), chol (268/127, z=15.8), chor (176/35, z=13.9), s (198/152, z=11.2), sho (102/23, z=10.6), chy (108/56, z=9.7), cthy (94/9, z=9.5), shol (113/73, z=9.2), shor (68/28, z=8.1), qotchy (49/13, z=7.3)
- hand 2: shedy (293/141, z=16.2), qokedy (200/76, z=14.0), chedy (276/231, z=12.4), ol (290/271, z=11.8), qokain (172/107, z=11.3), qol (109/33, z=10.6), qokal (122/75, z=9.6), qokeedy (165/142, z=9.3), qotedy (61/28, z=7.4), qokar (90/69, z=7.4)
- hand 3: qokeey (167/140, z=8.9), al (141/120, z=8.1), l (102/86, z=6.9), qokaiin (131/134, z=6.7), okeey (97/87, z=6.4), aiin (217/287, z=6.3), lkaiin (39/9, z=6.3), otain (58/38, z=6.1), okain (76/65, z=5.9), lkeey (34/5, z=5.8)
- hand 4: oteody (21/20, z=7.6), oteos (19/7, z=7.6), ar (78/325, z=7.0), oteey (37/108, z=6.5), okeo (13/6, z=6.3), oteo (11/6, z=5.8), okody (11/6, z=5.8), oteeos (10/4, z=5.6), otody (12/14, z=5.5), air (22/62, z=5.2)
- hand 5: sheody (8/41, z=5.7), cheky (8/58, z=4.9), okedy (11/109, z=4.7), dal (12/230, z=2.8), qokedy (11/265, z=1.9), y (10/296, z=1.2), chedy (14/493, z=0.7), shedy (11/423, z=0.3), daiin (17/832, z=-0.6), ol (9/552, z=-1.1)
