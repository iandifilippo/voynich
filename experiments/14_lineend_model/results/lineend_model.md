# 14 line-end transformation

Line-final tokens ending in -m: 627; in -g: 89. 97 tests, so Bonferroni threshold p < 0.0005.

## stem level: family deficit vs stem+m surplus

| set | stems | r | p |
|---|---|---|---|
| all | 107 | -0.124 | 0.894 |
| Currier A | 61 | -0.288 | 0.981 |
| Currier B | 65 | -0.023 | 0.601 |
| Takahashi | 117 | -0.197 | 0.970 |

Mean word length: line-first 5.43, internal 4.96, line-final 4.73.

Line-final vs expected for some word families (ratio > 1 = favoured at line end):

| word | line_final | expected | ratio |
|---|---|---|---|
| al | 28 | 28.405 | 0.986 |
| am | 57 | 2.430 | 23.453 |
| ar | 25 | 45.721 | 0.547 |
| ain | 10 | 14.886 | 0.672 |
| aiin | 39 | 63.645 | 0.613 |
| dal | 48 | 24.455 | 1.963 |
| dam | 54 | 4.557 | 11.850 |
| dar | 43 | 31.139 | 1.381 |
| dain | 26 | 20.506 | 1.268 |
| daiin | 129 | 79.897 | 1.615 |
| otal | 11 | 17.164 | 0.641 |
| otam | 28 | 2.430 | 11.521 |
| otar | 6 | 17.924 | 0.335 |
| otain | 9 | 12.759 | 0.705 |
| otaiin | 11 | 18.987 | 0.579 |
| rar | 2 | 2.127 | 0.940 |
| rain | 5 | 2.430 | 2.057 |
| raiin | 6 | 8.658 | 0.693 |
| ol | 42 | 69.417 | 0.605 |
| or | 17 | 47.999 | 0.354 |
| os | 1 | 3.190 | 0.313 |
| oiin | 0 | 4.557 | 0.000 |
| dol | 6 | 12.911 | 0.465 |
| dor | 6 | 6.228 | 0.963 |
| sal | 10 | 2.886 | 3.465 |
| sar | 12 | 4.101 | 2.926 |
| sain | 7 | 3.342 | 2.095 |
| saiin | 7 | 8.658 | 0.808 |

`-e -> -l` rows are a control: no reason to expect it.

| set | rewrite | types | r | p | line_end_tokens_explained | examples |
|---|---|---|---|---|---|---|
| all | -in -> -m | 96 | -0.131 | 0.891 | 324 | ain->am (57), oin->om (14), dain->dam (54), orain->oram (9), rain->ram (12) |
| all | -iin -> -m | 61 | 0.006 | 0.505 | 349 | aiin->am (57), oiin->om (14), otaiin->otam (28), araiin->aram (6), daiin->dam (54) |
| all | -aiin -> -m | 47 | -0.081 | 0.748 | 22 | oaiin->om (14), choaiin->chom (6), laiin->lm (1), daiin->dm (1), ykaiin->ykm (0) |
| all | -ain -> -m | 32 | 0.106 | 0.109 | 15 | oain->om (14), dain->dm (1), ytain->ytm (0), shodain->shodm (0), chodain->chodm (0) |
| all | -n -> -m | 99 | -0.656 | 0.997 | 104 | dan->dam (54), qokan->qokam (21), chan->cham (11), ain->aim (4), chekain->chekaim (1) |
| all | -y -> -m | 352 | -0.010 | 0.779 | 22 | oy->om (14), choy->chom (6), keey->keem (1), dy->dm (1), sheky->shekm (0) |
| all | -dy -> -m | 156 | -0.172 | 0.960 | 46 | ody->om (14), dody->dom (6), kody->kom (2), chody->chom (6), cheody->cheom (5) |
| all | -r -> -m | 124 | -0.093 | 0.845 | 391 | orar->oram (9), dar->dam (54), rar->ram (12), ar->am (57), otar->otam (28) |
| all | -l -> -m | 116 | -0.502 | 1.000 | 373 | al->am (57), dal->dam (54), oral->oram (9), ral->ram (12), olkal->olkam (8) |
| all | -s -> -m | 22 | 0.127 | 0.202 | 88 | as->am (57), os->om (14), los->lom (4), chos->chom (6), cheos->cheom (5) |
| all | -o -> -m | 41 | -0.542 | 0.993 | 3 | keeo->keem (1), lo->lm (1), do->dm (1), oksho->okshm (0), sho->shm (0) |
| all | -in -> -g | 96 | -0.054 | 0.737 | 12 | oin->og (2), rain->rag (2), chokain->chokag (1), daiiin->daiig (1), dain->dag (2) |
| all | -iin -> -g | 61 | -0.003 | 0.524 | 14 | oiin->og (2), araiin->arag (1), chokaiin->chokag (1), laiin->lag (1), raiin->rag (2) |
| all | -aiin -> -g | 47 | -0.100 | 0.768 | 8 | oaiin->og (2), choaiin->chog (1), araiin->arg (1), laiin->lg (1), daiin->dg (2) |
| all | -ain -> -g | 32 | 0.182 | 0.041 | 5 | oain->og (2), dain->dg (2), qokain->qokg (1), ytain->ytg (0), shodain->shodg (0) |
| all | -n -> -g | 99 | -0.691 | 0.999 | 3 | dan->dag (2), daiin->daiig (1), ykaiin->ykaiig (0), soiin->soiig (0), okaiin->okaiig (0) |
| all | -y -> -g | 352 | -0.085 | 0.941 | 18 | oy->og (2), okcheey->okcheeg (1), okaldy->okaldg (1), ytchdy->ytchdg (1), aly->alg (1) |
| all | -dy -> -g | 156 | -0.393 | 1.000 | 20 | cthody->cthog (2), lchdy->lchg (2), daiidy->daiig (1), ldy->lg (1), dchdy->dchg (1) |
| all | -r -> -g | 124 | -0.071 | 0.784 | 21 | rar->rag (2), lr->lg (1), chokar->chokag (1), chotar->chotag (1), oteor->oteog (1) |
| all | -l -> -g | 116 | -0.313 | 0.998 | 24 | dl->dg (2), ral->rag (2), chotal->chotag (1), chokal->chokag (1), lal->lag (1) |
| all | -s -> -g | 22 | -0.255 | 0.867 | 10 | dals->dalg (1), os->og (2), oteos->oteog (1), qokeos->qokeog (1), ls->lg (1) |
| all | -o -> -g | 41 | -0.242 | 0.914 | 11 | lcho->lchg (2), do->dg (2), dcho->dchg (1), qoko->qokg (1), oteeo->oteeg (1) |
| all | -in -> -l | 96 | -0.161 | 0.965 | 208 | dain->dal (48), orain->oral (4), rain->ral (5), sain->sal (10), ytain->ytal (3) |
| all | -iin -> -l | 61 | -0.062 | 0.658 | 240 | araiin->aral (7), daiin->dal (48), oraiin->oral (4), saiin->sal (10), raiin->ral (5) |
| all | -aiin -> -l | 47 | 0.187 | 0.098 | 69 | olaiin->oll (2), daiin->dl (8), shaiin->shl (1), raiin->rl (1), okaiin->okl (0) |
| all | -ain -> -l | 32 | -0.077 | 0.651 | 65 | olain->oll (2), dain->dl (8), shain->shl (1), rain->rl (1), ytain->ytl (0) |
| all | -n -> -l | 99 | -0.652 | 0.993 | 70 | dan->dal (48), chan->chal (7), aiiin->aiiil (1), soiin->soiil (0), okaiin->okaiil (0) |
| all | -y -> -l | 352 | -0.025 | 0.740 | 68 | dy->dl (8), oly->oll (2), shy->shl (1), sheky->shekl (0), oteey->oteel (0) |
| all | -dy -> -l | 156 | 0.065 | 0.157 | 108 | oldy->oll (2), lchdy->lchl (1), shdy->shl (1), arody->arol (1), choldy->choll (0) |
| all | -r -> -l | 124 | -0.555 | 1.000 | 310 | lor->lol (16), dar->dal (48), orar->oral (4), ror->rol (6), olor->olol (6) |
| all | -l -> -l | 116 | -1.000 | 1.000 | 322 | lol->lol (16), dl->dl (8), dal->dal (48), aral->aral (7), olol->olol (6) |
| all | -s -> -l | 22 | -0.167 | 0.820 | 110 | los->lol (16), as->al (28), ols->oll (2), dals->dall (0), chees->cheel (0) |
| all | -o -> -l | 41 | -0.281 | 0.939 | 13 | do->dl (8), ro->rl (1), lcho->lchl (1), sho->shl (1), oksho->okshl (0) |
| Currier A | -in -> -m | 40 | -0.137 | 0.822 | 46 | ain->am (12), dain->dam (24), chain->cham (4), okain->okam (2), daiiin->daiim (1) |
| Currier A | -iin -> -m | 36 | -0.129 | 0.788 | 86 | doiin->dom (6), choiin->chom (6), aiin->am (12), daiin->dam (24), oiin->om (4) |
| Currier A | -aiin -> -m | 27 | 0.121 | 0.300 | 4 | oaiin->om (4), ykaiin->ykm (0), daiin->dm (0), okaiin->okm (0), cthaiin->cthm (0) |
| Currier A | -n -> -m | 42 | -0.731 | 0.991 | 34 | dan->dam (24), chan->cham (4), ain->aim (1), kaiin->kaiim (1), dain->daim (2) |
| Currier A | -y -> -m | 104 | 0.051 | 0.248 | 7 | choy->chom (6), keey->keem (1), oteey->oteem (0), shody->shodm (0), chocthy->chocthm (0) |
| Currier A | -dy -> -m | 15 | -0.344 | 0.890 | 18 | ody->om (4), chody->chom (6), okeody->okeom (2), cheody->cheom (3), cthody->cthom (2) |
| Currier A | -r -> -m | 60 | -0.538 | 1.000 | 97 | dar->dam (24), ar->am (12), otar->otam (4), sar->sam (4), dor->dom (6) |
| Currier A | -l -> -m | 60 | -0.673 | 1.000 | 91 | dal->dam (24), al->am (12), sal->sam (4), chal->cham (4), otal->otam (4) |
| Currier A | -s -> -m | 10 | 0.201 | 0.276 | 14 | chos->chom (6), os->om (4), cheos->cheom (3), qokeos->qokeom (1), dals->dalm (0) |
| Currier A | -o -> -m | 18 | -0.101 | 0.945 | 1 | keeo->keem (1), oksho->okshm (0), sho->shm (0), sheo->shem (0), cho->chm (0) |
| Currier A | -in -> -g | 40 | -0.281 | 0.962 | 1 | daiiin->daiig (1), ykaiin->ykaig (0), soiin->soig (0), okaiin->okaig (0), cthaiin->cthaig (0) |
| Currier A | -iin -> -g | 36 | -0.160 | 0.830 | 3 | chokaiin->chokag (1), choiin->chog (1), otaiin->otag (1), ykaiin->ykag (0), soiin->sog (0) |
| Currier A | -aiin -> -g | 27 | -0.028 | 0.628 | 2 | qokaiin->qokg (1), daiin->dg (1), ykaiin->ykg (0), okaiin->okg (0), cthaiin->cthg (0) |
| Currier A | -n -> -g | 42 | -0.188 | 0.940 | 1 | daiin->daiig (1), ykaiin->ykaiig (0), soiin->soiig (0), okaiin->okaiig (0), cthaiin->cthaiig (0) |
| Currier A | -y -> -g | 104 | -0.140 | 0.921 | 7 | daly->dalg (1), choy->chog (1), dchy->dchg (1), otchy->otchg (1), qoky->qokg (1) |
| Currier A | -dy -> -g | 15 | 0.085 | 0.431 | 4 | cthody->cthog (2), qokeody->qokeog (1), chody->chog (1), shody->shog (0), chdy->chg (0) |
| Currier A | -r -> -g | 60 | -0.049 | 0.730 | 7 | daiir->daiig (1), otar->otag (1), qokeor->qokeog (1), cthor->cthog (2), dchor->dchog (1) |
| Currier A | -l -> -g | 60 | -0.011 | 0.633 | 6 | cthol->cthog (2), otal->otag (1), dchol->dchog (1), qokeol->qokeog (1), chol->chog (1) |
| Currier A | -s -> -g | 10 | -0.387 | 0.859 | 4 | dals->dalg (1), ches->cheg (1), qokeos->qokeog (1), chos->chog (1), os->og (0) |
| Currier A | -o -> -g | 18 | -0.387 | 0.924 | 4 | dcho->dchg (1), otcho->otchg (1), do->dg (1), cheo->cheg (1), oksho->okshg (0) |
| Currier B | -in -> -m | 73 | -0.276 | 0.984 | 241 | ain->am (44), oin->om (10), orain->oram (8), otain->otam (24), rain->ram (10) |
| Currier B | -iin -> -m | 42 | 0.075 | 0.322 | 240 | oiin->om (10), aiin->am (44), otaiin->otam (24), oraiin->oram (8), shaiin->sham (4) |
| Currier B | -aiin -> -m | 35 | 0.015 | 0.406 | 12 | oaiin->om (10), laiin->lm (1), daiin->dm (1), saiin->sm (0), oraiin->orm (0) |
| Currier B | -ain -> -m | 29 | 0.068 | 0.275 | 11 | oain->om (10), dain->dm (1), okain->okm (0), orain->orm (0), chdain->chdm (0) |
| Currier B | -n -> -m | 74 | -0.089 | 0.923 | 30 | qokan->qokam (19), chekain->chekaim (1), chain->chaim (1), ain->aim (3), olkain->olkaim (1) |
| Currier B | -y -> -m | 262 | -0.161 | 0.986 | 1 | dy->dm (1), ypchedy->ypchedm (0), dchey->dchem (0), chedy->chedm (0), ytedy->ytedm (0) |
| Currier B | -dy -> -m | 131 | -0.244 | 0.984 | 14 | ody->om (10), ldy->lm (1), qotody->qotom (1), cheody->cheom (2), ypchedy->ypchem (0) |
| Currier B | -r -> -m | 79 | 0.110 | 0.157 | 263 | orar->oram (8), rar->ram (10), ar->am (44), otar->otam (24), dar->dam (26) |
| Currier B | -l -> -m | 73 | -0.365 | 0.994 | 239 | al->am (44), ral->ram (10), olkal->olkam (8), dal->dam (26), otal->otam (24) |
| Currier B | -s -> -m | 15 | 0.142 | 0.377 | 57 | as->am (44), os->om (10), cheos->cheom (2), ls->lm (1), sheos->sheom (0) |
| Currier B | -o -> -m | 16 | -0.983 | 1.000 | 1 | lo->lm (1), sheo->shem (0), sheeo->sheem (0), okeeo->okeem (0), ykeeo->ykeem (0) |
| Currier B | -in -> -g | 73 | -0.120 | 0.886 | 8 | rain->rag (2), oin->og (1), dain->dag (2), kain->kag (1), ain->ag (1) |
| Currier B | -iin -> -g | 42 | -0.050 | 0.618 | 10 | araiin->arag (1), laiin->lag (1), raiin->rag (2), oiin->og (1), kaiin->kag (1) |
| Currier B | -aiin -> -g | 35 | -0.061 | 0.700 | 3 | oaiin->og (1), laiin->lg (1), daiin->dg (1), saiin->sg (0), oraiin->org (0) |
| Currier B | -ain -> -g | 29 | 0.097 | 0.151 | 2 | oain->og (1), dain->dg (1), okain->okg (0), orain->org (0), chdain->chdg (0) |
| Currier B | -n -> -g | 74 | 0.003 | 0.314 | 0 | oaiin->oaiig (0), aiin->aiig (0), daiin->daiig (0), saiin->saiig (0), daiiin->daiiig (0) |
| Currier B | -y -> -g | 262 | -0.026 | 0.836 | 5 | lshey->lsheg (1), lchey->lcheg (1), dy->dg (1), qokey->qokeg (1), oteey->oteeg (1) |
| Currier B | -dy -> -g | 131 | -0.503 | 0.996 | 9 | lchdy->lchg (2), ldy->lg (1), ody->og (1), lshedy->lsheg (1), cheody->cheog (1) |
| Currier B | -r -> -g | 79 | -0.158 | 0.897 | 11 | rar->rag (2), chotar->chotag (1), lr->lg (1), cheor->cheog (1), dar->dag (2) |
| Currier B | -l -> -g | 73 | -0.419 | 0.998 | 12 | ral->rag (2), lal->lag (1), aral->arag (1), dl->dg (1), kal->kag (1) |
| Currier B | -s -> -g | 15 | -0.326 | 0.900 | 4 | ls->lg (1), os->og (1), as->ag (1), cheos->cheog (1), sheos->sheog (0) |
| Currier B | -o -> -g | 16 | -0.314 | 0.880 | 4 | lcho->lchg (2), oteeo->oteeg (1), lo->lg (1), sheo->sheg (0), sheeo->sheeg (0) |
| Takahashi | -in -> -m | 95 | -0.157 | 0.925 | 332 | ain->am (57), dain->dam (60), rain->ram (14), otain->otam (29), chain->cham (11) |
| Takahashi | -iin -> -m | 60 | -0.003 | 0.507 | 365 | aiin->am (57), oiin->om (15), otaiin->otam (29), araiin->aram (7), daiin->dam (60) |
| Takahashi | -aiin -> -m | 48 | -0.122 | 0.796 | 24 | oaiin->om (15), choaiin->chom (6), laiin->lm (1), daiin->dm (2), ykaiin->ykm (0) |
| Takahashi | -ain -> -m | 34 | 0.114 | 0.159 | 18 | oain->om (15), lain->lm (1), dain->dm (2), ytain->ytm (0), shodain->shodm (0) |
| Takahashi | -n -> -m | 98 | -0.715 | 0.997 | 118 | dan->dam (60), qokan->qokam (21), chan->cham (11), ain->aim (4), chekain->chekaim (1) |
| Takahashi | -y -> -m | 359 | -0.094 | 0.951 | 13 | choy->chom (6), ly->lm (1), okoldy->okoldm (1), dchy->dchm (1), dy->dm (2) |
| Takahashi | -dy -> -m | 157 | -0.165 | 0.960 | 58 | ody->om (15), dody->dom (6), okody->okom (4), daiidy->daiim (3), cthody->cthom (4) |
| Takahashi | -r -> -m | 126 | -0.163 | 0.968 | 414 | orar->oram (9), rar->ram (14), dar->dam (60), ar->am (57), otar->otam (29) |
| Takahashi | -l -> -m | 120 | -0.540 | 1.000 | 398 | dal->dam (60), ral->ram (14), al->am (57), oral->oram (9), otal->otam (29) |
| Takahashi | -s -> -m | 20 | 0.033 | 0.585 | 36 | os->om (15), los->lom (5), cheos->cheom (6), chos->chom (6), ls->lm (1) |
| Takahashi | -o -> -m | 38 | -0.457 | 0.974 | 6 | do->dm (2), dcho->dchm (1), lo->lm (1), otcho->otchm (1), keeo->keem (1) |
| Takahashi | -in -> -g | 95 | -0.033 | 0.639 | 3 | ain->ag (1), okain->okag (1), dain->dag (1), ykaiin->ykaig (0), daiin->daig (0) |
| Takahashi | -iin -> -g | 60 | 0.154 | 0.107 | 3 | okaiin->okag (1), aiin->ag (1), daiin->dag (1), ykaiin->ykag (0), otaiin->otag (0) |
| Takahashi | -aiin -> -g | 48 | -0.081 | 0.735 | 4 | araiin->arg (1), laiin->lg (1), qokaiin->qokg (1), daiin->dg (1), ykaiin->ykg (0) |
| Takahashi | -ain -> -g | 34 | 0.135 | 0.117 | 3 | lain->lg (1), dain->dg (1), qokain->qokg (1), ytain->ytg (0), shodain->shodg (0) |
| Takahashi | -n -> -g | 98 | -0.739 | 1.000 | 1 | dan->dag (1), ykaiin->ykaiig (0), daiin->daiig (0), otaiin->otaiig (0), cthaiin->cthaiig (0) |
| Takahashi | -y -> -g | 359 | -0.154 | 0.984 | 15 | ly->lg (1), chekey->chekeg (1), chaly->chalg (1), ykchdy->ykchdg (1), okcheey->okcheeg (1) |
| Takahashi | -dy -> -g | 157 | -0.460 | 1.000 | 13 | lchdy->lchg (2), aldy->alg (1), ldy->lg (1), daldy->dalg (1), cthody->cthog (1) |
| Takahashi | -r -> -g | 126 | -0.300 | 0.997 | 8 | alor->alog (1), lr->lg (1), qokeor->qokeog (1), dchor->dchog (1), cthor->cthog (1) |
| Takahashi | -l -> -g | 120 | -0.224 | 0.973 | 9 | alol->alog (1), qokl->qokg (1), dl->dg (1), dchol->dchog (1), qokeol->qokeog (1) |
| Takahashi | -s -> -g | 20 | -0.091 | 0.724 | 4 | qokeos->qokeog (1), ls->lg (1), chees->cheeg (1), ches->cheg (1), oteos->oteog (0) |
| Takahashi | -o -> -g | 38 | -0.451 | 0.979 | 7 | lo->lg (1), qokeo->qokeg (1), qoko->qokg (1), oteeo->oteeg (1), do->dg (1) |
