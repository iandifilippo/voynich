# Research log

Newest first. Numbers come from the `results/` folder of each experiment; rerun to check.

## 2026-11-22 (1)

### 57 spaces in the ink (daniilvaino/VoynichManuscriptOCR stage-1 ink masks + row lines; band +-0.9 xh, 0.5 px step)
115 976 gaps; share per 0.1 xh bin from 0: 3.2 21.5 19.9 14.6 8.7 4.3 3.7 2.3 1.6 1.5 1.2 1.2 1.4 1.4 1.5 1.3 1.2 1.3 1.4 1.2 1.0 ...
Matched 26 pages, 499 P lines. Ink words/line at T .6/.8/1.0/1.2: 9.13/7.37/6.43/5.85; ZL split 7.88, join 7.38; exact match split .263/.395/.265/.170, join .208/.453/.367/.236; r .84/.90/.85/.80.
Boundaries placed by glyph count (tol 1.5 glyphs): 3435; certain mean 1.353 median 1.363 >=.8 .727; doubtful .943 / .843 / .528. Coupling certain by ink tertile: .212 .193 .117.

## 2026-11-21 (3)

### 56 handwriting per sheet (boxes; pages >= 40 boxes; z-scored 4 measures)
same leaf / other leaf same sheet / facing other sheet: hand1 H .77 (45) / .71 (62) / .85 (26); hand1 P too few; hand2 H .83 / .97 / .55 (2); hand2 B 1.07 / .94 / .89; hand3 S .64 / .86 / .86.
Mantel handwriting vs fork profile (2000 perms): hand1 H r .097 p .044; hand2 H .090 .231; hand2 B .058 .324; hand3 S .085 .251.
Other image sources checked: digitalgoldfisj79/voynich-images has 6 bathing pages at 1856 px wide; not enough for a manuscript-wide pixel study.

## 2026-11-21 (2)

### 55 spaces from boxes (lrozanova/voynich-units word boxes, 223 folios, 37 464 boxes, 30 305 in-line gaps; gap / folio median box height)
Gap quantiles 1/5/10/20/30/50/70/90/99%: -.143 0 0 .125 .143 .286 .333 .5 2.857.
Lexicon gain as boxed / touching joined / <=.125 / <=.143 (random-merge control): B -.216 / -.355 (-.386) / -.370 (-.410) / -.511 (-.579), closed .155 .181 .381; A -.317 / -.403 (-.443) / -.543 (-.585) / -.577 (-.596).
Coupling last->first by gap tertile (20 shuffles): B .421 .212 .081 (7670/6139/6333 pairs); A .247 .093 .029.
Residual beyond boundary by tertile (inside-sheet perms, 20): B .291 .241 .247 (all .295); A .137 .029 .134 (all .171).
Literature added: Rozanova & Temerev arXiv:2608.17096; Smith & Ponzi 2019; Parisel 2025-26.

## 2026-11-21 (1)

### 54 fork bits (WB n-gram, train half sheets / test other half, both ways)
Gain from looking further than 1 back (best k): qo channel: 1-bit cipher .085 (8), 2-bit .005, 4-bit .000, gen .017, B .005, A .000. start: 1-bit .008, 2-bit .179 (5), 4-bit .006, gen .064, B .003, A .000. end: 4-bit .009, B .004, A .002. start+end: 4-bit .307 (3), 2-bit .000, gen .000, B .000, A .000. gallows: B .009, A .010, gen .018, ciphers .000.
k=0 bits: qo B .677 A .457 gen .640; start B 1.952 A 1.803; start+end B 3.702 A 3.704.
Added docs/where_it_stands.md.
Channels: gallows 2-bit cipher .179 (k5), gen .012, B .009, A .010; length parity 1-bit .097 (k9), gen/B/A .000; e-run 1-bit .097 (k9), gen .001, B .007, A .022 (k5). A e-run: ZL .022 / lines shuffled .014; IT .026 / .019.

## 2026-11-20 (10)

### 51 replication (3+ signs; habits generator refit per text, grid sigma .3-1.2 x hold 1-4)
beyond boundary text/gen, off-diag text/gen: ZL B .240/.076, .038/-.014 (sigma .9 hold 2.5); ZL A .181/.052, .075/-.008 (.6, 2.5); IT B .259/.109, .041/-.010 (.6, 2.5); IT A .159/.039, .053/-.016 (.6, 2.5).
8 seeds: ZL B beyond .064-.116, off-diag -.023-.001; ZL A .010-.086, -.042-.003.

### 52 grammar (classes start x end, 40 perms, cells exp >= 10, off-diagonal)
corr log ratios: B halves -.019 (153 cells); A halves .073 (46); A vs B -.033 (151); ZL vs IT B .826 (339); B vs gen -.043 (283).
Transfer bits/pair (across sheets / odd-even lines pooled / per sheet): B .0030/.0020/.0042; A .0008/-.0036/-.0010; gen .0045/.0026/.0018.

### 53 recurring pairs (alternate sheets, 20 shuffles)
seen before / shuffled / excess / reversed excess: B .178/.132/.045/-.002; A .105/.089/.016/-.001; gen .092/.076/.016/.001; Naibbe .123/.101/.023/.003; Latin .179/.113/.066/-.055; Italian .317/.180/.137/-.086.
B top: or aiin 44/5.6, s aiin 35/1.8, ar aiin 24/6.4, r aiin 18/1.4, ol shedy 24/9.4, shey qokain 17/3.2, shedy qokedy 21/7.5, chedy qokeey 19/5.8, shedy qokaiin 17/4.2, qokeedy qokeedy 18/5.8. Excess by kind: different .97, one glyph apart .03, same word .01.

## 2026-11-20 (9)

### 50 habits-only generator (B sheets 100+ words; sheet identity = half-sheet own closest; gallows ratio d=2-4, nearby lines)
Target: identity .975, gallows ratio 1.067. Grid sigma 0/.3/.6/.9 x hold 1/1.5/2.5: identity .05/.68-.78/.95-.99/1.00; ratio 1.03-1.09. Best sigma .9 hold 2.5 (misfit .025).
Beyond boundary (15 perms): B .299; gen none .071; gen fitted .116; strong .117.
Residual (20 perms): B repeat obs/base start .076/.072 gallows .379/.346 ending .135/.117 length .234/.228; off-diag CMI .028 .010 .014 .008. Gen fitted: repeats .087/.080 .391/.374 .108/.097 .251/.233; off-diag -.006 -.006 .006 -.004.
Top B start transitions vs expectation: yt->ot 1.69 (33 vs 19.6), or->aii 1.50, che->al 1.48, ot->ar 1.44; che->op .12, ai->ot .45, or->al .46.
Spacing: split .299; 3+ signs .236; join .256; join 3+ .237; generator 3+ .069.

## 2026-11-20 (8)

### 48 beyond boundary (CMI given last sign i and first sign i+1; 30 perms)
Whole-text baseline, start/gallows/ending/length same->same, sum16: B .040 .034 .038 .008, .351; A .035 .032 .033 .014, .310; generator .007 .003 .004 .002, .017; Latin cipher .068 .024 .089 .028, .898; Latin .104 .009 .171 .057, 1.178; Italian .198 .008 .278 .084, 1.832.
Inside-sheet baseline: B .031 .033 .030 .008, .298; A .024 .028 .020 .011, .231; gen .017; cipher .878; Latin .657; Italian 1.369.
Plain MI by distance (shuffle in sheet by position), start d1-3 / gallows / ending: B .182 .053 .028 / .032 .024 .020 / .078 .024 .021; A .137 .048 .039 / .029 .029 .020 / .078 .022 .036; gen .064 .012 .013 / .003 .002 .000 / .055 .009 .007; cipher .150 .052 .013 / .017 .003 .002 / .110 .041 .017; Latin .180 .079 .041 / .001 .000 .000 / .351 .113 .060.

### 49 line setting (agreement ratio same line / other line, line-first words excluded)
gallows d1-4: B 1.116 1.106 1.070 1.073; A 1.080 1.087 1.080 1.053; gen 1.063 1.036 .993 1.019. start: B 1.016 1.141 1.107 1.097; gen 1.058 1.106 1.068 1.148. Latin last letter 1.115 1.217 1.175 1.126.

## 2026-11-20 (7)

### 44 synthetic calibration (Latin ciphers of Voynich words, K=16 held-out MI)
word per letter 5 homophones .460; 40 homophones .284; per syllable 1 hom. .638; 3 hom. .688; codebook .130. B .087, A -.007.

### 46 features (MI next word, minus position-class shuffle, 10 shuffles)
first->first, last->last, gallows, last->first: B .071 .016 .032 .250; A .056 .016 .029 .139; Naibbe .006 .000 .000 .003; letter cipher .081 .047 .034 .060; Latin .021 .096 .001 .040; Italian .060 .057 .006 .118.
B boundary pairs obs/exp: s.a 6.07 (208), o.r 5.40, o.l 5.02, r.a 3.44 (738), l.k 2.96, y.q 1.72 (2999); avoided y.a .15, n.l .17, r.l .25, r.q .28, n.q .38.

### 47 sheet keys (sheets 100+ words: B 20, A 28; 20 within-sheet shuffles)
pooled/inside: first->first B .067/.074, A .051/.051, one-key .034/.032, key-per-sheet .000/.027, generator .019/.022. last->last B .014/.020, A .013/.019, one-key .005/.007, per-sheet .002/.012, gen .014/.018. last->first B .249/.260, A .137/.144, one-key .011/.008, per-sheet .002/.018, gen .233/.226. shape->shape B .297/.209, A .161/.069, one-key .154/.091, per-sheet .047/.131, gen .231/.127.

## 2026-11-20 (6)

### 44 word classes (exchange clustering, 11000 words/half, held-out MI minus shuffled-train baseline)
First pass (all types): K=8/16/32 Naibbe .002/.007/.006, B .011/.030/.049, A -.005/.007/.026, Latin .045/.082/.078.
Min count 5 (rare merged): K=4/8/16/32 Naibbe .036/.042/.039/.047; B .037/.087/.087/.083; A .007/.009/-.007/-.001; copy .001/.008/.008/.032; assembled .008/.027/.021/.036; Latin .079/.092/.133/.130; Italian .148/.250/.308/.317. Line-middle only: B .042/.097/.092/.091.
Lags K=16, d=1/2/3/5/same page: B .083/.012/.010/.006/.006; A .005/-.005/-.002/-.019/-.002; Naibbe .039/.000/.002/-.005/-.000; Latin .149/.021/.002/.005/-.001; Italian .307/.029/.004/.006/.002; assembled .020/-.001/.001/.004/.002.
Edges (d=1): B as written .083, keep first sign .006, first+last .051, first2+last2 .073, free .001; Latin .135/.001/.025/.112/-.000; Italian .305/.005/.039/.257/-.001.

### 45 labels (4+ letters; text units P, R, C)
Exact per 1000, own page / same sheet / other sheets: pharma .612/.650/.620 (225 labels); bathing 1.824/1.439/1.463 (107); zodiac 1.400/1.178/1.168 (310); cosmological 1.633/2.540/.769; astronomical .486/.467/-.
Raw own-page hits: pharma 20, bathing 63, zodiac 35. Labels found anywhere in running text: .467/.701/.574.
Starts: labels o .602 q .010 ch/sh .091 d .086; text o .216 q .168 ch/sh .285 d .075.
Permutation (1000): all labels 118 vs 101.2, p .104; o- labels 57 vs 44.9, p .087; o- as qo- 76 vs 52.2, p .040.

## 2026-11-20 (5)

### 43 cipher page identity (14x8-word pages, 50 pages)
Naibbe ciphertext own/shared-removed .000/.000; plaintext (letters in 5s, generic profile) .010/.010; chance .020.

## 2026-11-20 (4)

### 41 page dial (pages 80+ words; 30 shuffles)
Eigenvalues PC1-5 (shuffled): A hand1 5.17(3.40) 3.34(2.89) 2.94(2.56) 2.76(2.27) 2.22(2.06), 6 real; B hands 2+3 7.57(3.85) 3.97(3.22) 3.09(2.74), 3 real; hand1 H 3 real; hand2 B 4; hand3 S 3.
Split-half ARI k=2..6: A .29 .55 .55 .35 .25; B .89 .59/.68 .73/.60 .33/.64 .61/.50 (two runs; k-means starts); hand1 H .00 .66 .53 .30 .41; hand2 B .60 .69 .60 .47 .43; hand3 S .83 .84 .85 .91 .59. Shuffled all within +-0.05.
Stars k=2: {f58r f58v f104r f104v f105r f105v f106r f106v f107r f112v f113r f113v f114r f114v f115v} vs {f103r f103v f107v f108r f108v f111r f111v f112r f116r}. Bathing k=2: {f75 f78 f79 f80 f81 r/v, f82v, f84r/v} vs {f76v f77r f77v f82r f83r f83v}.

### 42 setting unit (pages 60+, distances relative to group mean pair, 2000 sheet resamples)
same leaf / same side / opposite sides / facing other sheet: hand1 H .64/.66/.64/.85 (n 39/25/25/21); hand2 H .60/.78/.73/.63 (10/10/10/2); hand2 B .62/.52/.81/.88 (10/8/8/8); hand3 S .55/.61/.69/.82 (12/11/11/10).
same side - facing: hand1 H -.196 [-.36,-.05]; hand2 B -.357 [-.58,-.13]; hand3 S -.213 [-.32,-.12]. same side - opposite: hand2 B -.287 (p .074), hand3 S -.083 (.095), hand1 H +.013.

## 2026-11-20 (3)

### 40 page identity (pages 80+ words, halves = odd/even lines)
Own half closest / mean rank / neighbour-far, ZL: hand1 H .382/.104/.818; hand2 H .342/.126/.772; hand2 B .605/.032/.783; hand3 S .729/.031/.705.
Shared words removed: .314 .316 .526 .625. Lines shuffled: .021 .055 .054 .048. Echo generator: .020 .037 .068 .067. Copying (page_lines 20): .291 .553 .553 .382, shared removed .078 .237 .237 .125.
IT: .367 .342 .684 .771, shared removed .265 .289 .579 .667. FG not applicable (alphabet).
Generic profile (15 starts + 15 ends), own / shared removed: Casebook .114/.136 (22 pages), AlphabetOfTales .040/.040, Cirurgie .070/.020, Secreta LAT .080/.030, Picatrix .050/.070, Rettorica .070/.040; VMS hand1 H .284/.206, hand2 H .316/.289, hand2 B .526/.474, hand3 S .729/.479.

## 2026-11-20 (2)

### 39 forks (pages 60+ words, 34 fork features, 2000 permutations)
R2 / random / p / LOO acc / chance: hand1 H vs P .101/.010/<.001/.860/.840; hand2 H/B/T .313/.047/<.001/.907/.465; hand2 H vs B .305/.026/<.001/.949/.513; hand3 H vs S .141/.034/<.001/.967/.800; herbal B hands 2/3/5 .162/.064/.001/.719/.625; text hands 2/5 .294/.250/.601; herbal hand1 vs hand2 .163/.010/<.001/.971/.808.
Halves (time only): hand2 H .085/.053/.119; hand2 B .011/.056/.998; hand3 S .063/.044/.145; hand1 H .024/.012/.029.
Hand 2 means B/H/T: qo .243/.091/.148, -edy .264/.136/.120, -ar .049/.113/.130, -dy .042/.121/.088, -ol .115/.041/.059. Hand 2 quires: H in D-G, B in M, T in M-N.

## 2026-11-20 (1)

### 37 small machine (HMM, EM, 3 starts, 250 iters, uniform pi; even pages train, odd test)
Held-out bits/sign K=2,4,6,8,12,16,24,32,48: B 3.754 3.264 2.809 2.675 2.224 2.126 2.028 2.001 1.969; chain 1/2/3 back 2.139/1.973/2.010.
A: 12 2.511, 24 2.284, 48 2.247; chain 2 back 2.247, 3 back 2.315. Latin: 12 3.275, 24 3.061, 48 2.844; chain 2/3 back 2.691/2.245. Italian: 12 3.159, 24 2.966, 48 2.711; chain 2/3 2.541/2.132. Naibbe: 12 2.378, 24 2.127, 48 2.034; chain 2/3 2.059/2.038. Copying: 12 2.396, 24 2.165, 48 2.110; chain 2/3 2.120/2.124.
Generated vocab at K=48, distinct/1000 and unseen, real vs machine: B 247.7/264.4, .173/.196; A 348.3/344.0, .241/.246; Latin 354.5/669.1, .231/.758; Italian 263.5/532.8, .193/.655; Naibbe 275.8/323.0, .157/.281; copying 232.6/256.5, .137/.216.

### 38 read the machine (K=12, 6 starts, 400 iters, all of Currier B / A)
B states: space; o .91; k .57 t .29 p .07; e .63 ee .29; y .94; l .55 r .35 m .05; a .91; d .88; ch .67 sh .31; q .83; ii .55 i .42; n .89. Max self-transition .002. Diagram results/machine_B.svg, machine_A.svg.

## 2026-11-17 (1)

### 36 assembled words (held-out Currier B, ZL, even pages train / odd test, 3 seeds)
distinct/1000, hapax, unseen tokens, top-20, lexicon gain: VMS 247.7 .672 .173 .234 -.246; asm1 316.3 .796 .263 .327 -.475; asm2 262.2 .700 .179 .254 -.362; asm3 229.5 .593 .116 .231 -.097; asm2 no link 260.9 .701 .177 .256 -.368; lexicon 190.5 .404 0 .235 .386; asm2+recall 290.6 .712 .214 .237 -.365; copying 214.4 .615 .489 .263 .023.
adjacent exact/near per 1000, q-, para-first gallows, line-last -m, doubletons one page: VMS 9.08/33.1 .180 .881 .187 .074; asm2 5.32/24.2 .179 .836 .160 .033; asm2+recall 7.61/33.7 .173 .828 .168 .105; lexicon 4.27/21.1 .178 .079 .024 .029; copying 7.17/37.0 .014 .942 .085 .236.
Tune (training half only): target exact 9.37, near 34.4, dbl .084, distinct 267.4; best p=.01 edit=.10 window=5 (misfit .311); exact-only recall p=.03 gives dbl .16 and near 23.5.
Robustness (knobs not refitted), unseen VMS/asm2, lexicon gain VMS/asm2, within-range asm2+recall: ZL A .241/.224, -.366/-.412, 12; IT B .185/.179, -.259/-.363, 11; GC B .199/.176, -.320/-.372, 10.
Bug found while running: the assembler looped forever when a word-start context was unseen; fixed with a fallback to all word-initial signs.

## 2026-11-16 (28)

### c12-c14
c12 affix parser (top 25, 10000 words): prefix+suffix A .152 B .230 copy .140 Naibbe .212 Latin .156 Italian .112 English .026; stems/distinct words .518/.571/.637/.498/.832/.820/.857; top-10 cells .076/.180/.115/.144/.041/.039/.016; prefix->suffix MI excess .057/.151/.213/.138/.126/.100/.069.
c13 Sukhotin (20000 words): crossing pairs, composites as one: A .826 (shuffled .552), B .842 (.547), copy .776 (.547), Naibbe .816 (.545); plain EVA A .764, B .781, copy .750, Naibbe .850. Latin .838, Italian .804, English .796, Georgian .825, Hebrew .625. Vowels A: o a y n e c g u; B: o e a y n c h u z.
c14 filler (2400 words, 5 splits): repeated-word share least/most quarter A .04/.71, B .17/.77. Lexicon gain least / most / all: A -.467/-.370/-.433; B -.478/-.313/-.453; Latin 1.405/1.400/1.498; Italian 1.409/1.096/1.163.
Correction to 34 notes: Amirandar is Georgian (not Armenian); no French text in that set (Sindbad is Persian).
Blasto (Merricx): monoalphabetic + turning grille hill-climber, en/de/es quadgrams; same family as exp. 31, not rerun. Guy 1991 scan has no text layer; his VMS output not checked.

## 2026-11-16 (27)

### 35 letter-or-pair attack, full text
True cuts + annealer on full Naibbe (52641 symbols, 398 distinct): 98.2% letters right; true key -0.973, found -0.964 (23-letter LM).
EM/HMM with Latin bigram transitions, true cuts: 11-21% letters; ll/symbol EM -5.10 vs true key -5.25 (unigram -5.52).
Old segmenter (cost -2, discount 2): 79.9% token agreement (15.1% wholes split). fit_ranked: k=80 .930, 110 .946, 137 .940, 160 .929, 200 .913, 260 .892.
Single annealing run at k=110, 4M iters: 4 of 6 seeds reach -1.002 (sim .946), misses at -1.037. 12M iters no better. Jobs = best of 4.
Naibbe/Latin k=60/110/200: score -1.034/-1.002/-1.025 (real -0.990), similarity .04/.94/.90, lost by shuffling .032/.083/.073. Italian: -1.009/-1.049/-1.068 (real -0.895), shuffling .039/.017/.023. German: -0.986/-1.002/-1.069 (real -0.947).
Naibbe cut to 5000 / 11231 / 23084 words (Latin, k=110): similarity .14 / .91 / .94; gap .011 / .024 / .014.
VMS A Latin -1.374/-1.454/-1.622, shuffling .008/.005/.019; Italian -1.391/-1.479/-1.652, .007/.004/.022. VMS B Latin -1.395/-1.492/-1.667, .014/.012/.029; Italian -1.406/-1.507/-1.700, .018/.021/.032. Copying model Latin -1.450/-1.558/-1.821, .009/.012/-.023; Italian -1.493/-1.575/-1.783, -.031/.031/.034.
Pieces (k=110) at 2500/5000/10000/20000 words: Naibbe 406/428/445/502; B 584/792/1002/1549; A 569/760/1183/-; copying model 479/701/986/1468. Seen once: Naibbe .15-.20, VMS .43-.52, copy .38-.42. Coverage by top-500 pieces: VMS .92-.96.

## 2026-11-16 (26)

### 34 slots / memory / between
Slot parse (12 slots, early-first): tokens parsed A .790, B .842, copying model .575, Naibbe .921; types parsed A .471, B .477.
Shared bits (sum slot H - word H): A 4.41 (indep. baseline 1.68), B 5.16 (1.51), copy 5.26 (1.43), Naibbe 5.14 (1.63). Late-first parse: A 4.06, B 4.78.
Held-out bits/word indep / chain / whole-so-far: A 13.07 / 9.38 / 9.26; B 14.01 / 9.54 / 9.29; copy 13.60 / 9.54 / 8.71; Naibbe 14.85 / 10.88 / 10.25.
I(prefix; suffix | core) excess over within-core shuffle: A .216, B .200, copy .369, Naibbe .365 (all p .005).
Independent device: types A 4470 vs 1515 real, B 9704 vs 2284; share of device types attested .119 / .084.
memory.py (11000 words, WB interpolation, 5 folds), bits/word order 1/2/3/4: A 11.83/11.30/11.52/11.89; B 11.09/10.43/10.61/10.94; copy 12.09/10.48/10.38/10.54; Naibbe 12.44/11.25/11.07/11.15; Secreta LAT 21.93/17.74/14.66/13.38; Picatrix 18.85/15.67/13.42/12.73; Rettorica 19.03/15.90/13.57/12.94; Cirurgie 16.41/12.95/10.73/10.13; Agrippa 17.95/14.48/11.91/11.17; Steganographia 24.89/21.01/17.91/16.73; Sindbad 16.24/14.58/13.83/14.01; Mishneh 19.04/15.91/14.37/14.28; Amirandar 25.24/20.39/17.14/16.40; Wormianus 17.10/14.46/13.25/13.13.
Plain EVA chars, best order: A 2, B 2, copy 4, Naibbe 4.
Lexicon gain over order-2 (bits/word): A -.31, B -.27, copy +.10, Naibbe +.12; languages +.67 (Sindbad) to +3.82 (Secreta LAT).
between.py, previous word -> word, above shuffled: A .163, B .231, copy .151, Naibbe .104; language words .87-1.40; letters-as-words .38-.77. Last sign -> first sign of next: A .110, B .229, copy .113, Naibbe -.019.

## 2026-11-16 (25)

### c08-c11 (voynich.ninja material)
c08 Caveney Greek: devoicing merger h2 drop Greek .089, Latin .119, Italian .108, French .103 (VMS 2.154). Readings of the line under his alternatives: 8192. Hit rate Greek lexicon: VMS .312 vs shuffled .127 (p .010); copying model .302 vs .160 (p .063).
c09 Turkic key: VMS .202 vs .069 (any of Turkish/Azerbaijani/Turkmen/Uzbek), copying model .202 vs .065, Naibbe(Pliny) .173 vs .056. -m line-final 69.8%; q word-initial 99.4%.
c10 star code: 83% paragraphs open with gallows; 3.4% of gallows are paragraph-initial; first-line share k .16, t .22, p .81, f .78 (first lines = 19.6% of text). q->o 97.8%. e-runs 9134/3945/350/6. Repeats per 1000: B 11.8, C 13.6, H 9.5, P 8.6, S 8.1, T 8.7.
c11 doubletons (537): same line .6% (11.7x), page 3.9% (2.7x), sheet 11.7% (2.0x), section 52% (1.4x), hand 66% (1.1x); >20 pages apart 65%.
Pattern across c07/c08/c09: every vowel-to-vowel-like key beats its own shuffles on VMS and equally on content-free controls.
Not testable from the text: ink titanium / modern-forgery argument (SantaColoma vs Stolfi on McCrone samples 17, 20).

## 2026-11-16 (24)

### 33 letter-or-pair: calibration fails
Pair cipher (signs for top 60/150 pairs + letters), key units = 26 letters + 150 pairs, iters 40000 x symbols, 2 restarts. Latin 84/174 signs: 0% right, gap -0.241/-0.207. Italian 86/176: 25.7%/12.1%, gap -0.270/-0.207. Hungarian -> Latin -0.279/-0.230; -> Italian -0.371/-0.264. No separation. Attack on VMS not run.
To do: grow from the one-letter key; beam/EM over sign lengths; blind Naibbe as the entry test.

## 2026-11-16 (23)

### 32 attack 2 (transformed plaintext)
Power (100 homophones, held-out): Latin no-vowels 91.9%, sorted 95.3%, backwards 99.8%; Italian 98.1 / 96.9 / 100; German no-vowels 100, sorted 98.6; Hebrew, Arabic, Persian 100.
VMS B / A / copying model, best of glyphs, groups, merged 60 (gap; word share): Latin no vowels +0.085 / +0.080 / +0.116; words .335 / .243 / .316 (real .319). Italian no vowels +0.008 / -0.002 / +0.053; .327 / .262 / .350 (real .459). German no vowels -0.026 / -0.043 / +0.023. Latin sorted -0.354 / -0.287 / -0.268. Latin backwards -0.143 / -0.122 / -0.074. Hebrew -0.161 / -0.191 / -0.155. Arabic -0.153 / -0.170 / -0.082. Persian -0.174 / -0.201 / -0.113.
No-vowels target is satisfiable by anything.

## 2026-11-16 (22)

### 31 attack 1 (symbol = letter)
Schemes: glyphs (26-27 symbols), groups (~52), merged 60 (~87), merged 150 (~177), pieces (400, no spaces); spaces kept/ignored; Latin, Italian, Spanish, French, German, Middle English, Czech, Hungarian, Turkish. 3000 words each of A and B; controls copying model and shuffled glyphs. 324 solver runs.
Best VMS gap -0.109 (B, glyphs, no spaces, Latin; also B pieces Latin). Best copying-model gap -0.120 (merged 60, Italian). B > control in 38/81, A in 30/81; mean B - control -0.004, A -0.018. Word-share max VMS 9.0%, control 10.8%; real 36-66%.
Pieces: VMS - copying model +0.05..+0.12 in all 9 languages, but shuffled-glyph control gap +0.052 Latin, +0.042 Italian, +0.031 Czech (above real text): overfit at 400 symbols / 3000 words. Rerun on full text needed.

## 2026-11-16 (21)

### 30 solver + calibration
voynich/crack: C annealer via ctypes, key = symbol -> letter string, interpolated letter 4-gram (.60/.25/.10/.05) + letter-frequency term, incremental rescoring. Latin target, 4000 held-out words (Aix). Latin plaintext: 26/50/100/200/400 symbols, spaces kept: 99.9% letters, score -0.907 (real -0.910), 26.1% letters in dictionary words; no spaces 50/200/400: 99.4/99.0/98.8%, -0.989 (real -0.994), 29.0/28.0/27.5%. Hungarian plaintext: -1.21..-1.24 kept, -1.18..-1.20 removed; hits 0.1-1.9%. Scrambled Latin: -1.33..-1.38 kept, -1.27..-1.30 removed; hits 0-0.5%.
First blind go at Naibbe (pieces from unsupervised 2-cut segmenter, 83% cuts right, 597 symbols): solver -1.035 vs "true" key -1.197, 19% right. Looks like Latin, isn't. Word-level symbols (600-1200 types, units = letters + 120 bigrams): stuck at 29-43% token accuracy below the true key's score.
Bugs: add-k smoothing made all-y the optimum (fixed: interpolation); no frequency term gave "alalaal".

## 2026-11-16 (20)

### 29 sheet geometry
Scribes 2+3, K=5: conjoint a_v->b_r 1.50 [1.20-1.80] (14), next folio 1.28 [0.96-1.55] (9), recto->own verso 1.11 [0.88-1.36] (16), b_v->a_r 0.74 [0.56-0.90] (14), unrelated 1.05. Conjoint - next folio: K4 0.79, K5 0.43, K6 0.42, K8 0.28 (p .000/.001/.004/.004); rare words K5 1.81 (p .005), K8 0.58 (p .11). Scribe 1: own verso 1.55, conjoint 1.38, outside 1.33, next folio 1.53, unrelated 1.13; conjoint - next -0.28 [-0.91, 0.60].
Direction (leaf a -> b vs b -> a, 4 cross pairs each, K=6): stars 1.48 vs 0.77, diff 0.71 [0.26, 1.24], 4/4; herbal B 1.41 vs 1.08, 0.33 [-0.03, 0.68], 4/5; herbal A 1.41 vs 1.29, 0.12 [-0.11, 0.38], 7/15.
Stars matrix: a_r->a_v 2.04, a_v->b_r 1.58, b_r->b_v 1.09, b_v->a_r 0.43.
Replication (conjoint - next folio; stars a->b / b->a): IT 0.31 p .022, 1.50/0.85; GC 0.34 p .021, 1.35/0.92; FG 0.34 p .044, 1.56/0.85.
Consequence: f103-f116 as bound is not the writing order; exp 22/25 stars numbers read it wrongly.

## 2026-11-16 (19)

### prior work I had missed
- Schwartz, "How the Voynich Manuscript was written" (preprint, 1 Oct 2026): reuse 73/77%, local copy 2.0/4.9%, coinage 25.1/18.4% (scribes 1/2); T&S generator local copy rate .42-.48 vs .28/.38; no keyless generator reproduces boundary coupling; subject dependence astro z 2.6, balneo z 2.9, herbal z 1.2; boundary words "distinct, not edge-modified". Overlaps exp 21-22 (core/reuse) and agrees with 27; disagrees with 20 on edge words.
- Zhang & Sheng, arXiv:2610.34499 (25 Oct 2026): copying programs fit as well as two-key ciphers; ported T&S coupling 0.078 vs 0.204 bits.
- Layfield & Davis, Digital Medievalist 2026: singulions; conjoint > facing similarity in 8/9 quires; drawings across 78v/81r, 76v/83r, 33v/40r, 10v/15r, 58v/65r.
- Timm, arXiv:1601.07435 (2016): positional grids for same/similar words, natural-text controls, no shuffle null.
Notes for 18, 20, 22, 24, 25, 27 now cite these.

### 26 extended to all single-scribe blocks
19 sheets. Scribe 1: book 1.56, conjoint 1.28, other 1.21; wins 9/2. Scribes 2+3: book 1.21, conjoint 1.64, other 1.26; wins 1/5, 2 ties; conjoint - book 0.43 [0.12, 0.73]. Fisher p .035. Conjoint wins at f76v->f83r (29 vs 20), f78v->f81r (16 vs 11), f33v->f40r (20 vs 13), f103v->f116r (13 vs 3), f105v->f114r (9 vs 5). Pooled over everything: no difference (1.36 vs 1.48).

## 2026-11-16 (18)

### 28 page template
G of word x page-third (top 150 words), body text only (no paragraph-first/last lines, no line-first/last words). z vs lines shuffled / vs rolled-and-flipped pages: herbal A -0.36 / -0.59 (p .71); herbal A unfiltered 1.59 / 1.59 (p .06); balneo B 2.74 / 1.74 (p .044); stars B 2.17 / 1.33 (p .098); herbal B 0.71 / 0.71; pharma A -1.0 / -1.1; Pliny 1.61 / 0.97; copying model 0.59 / 0.08. Simple shuffle overstates because it breaks runs. No positive control (need an entry-per-page herbal).

Looked at quire 13 by sheet geometry (r->own v 0.80, v->next r 1.18, inner spread 1.35, outer 0.99, other 0.95; n = 4-9 each): nothing I'd stand behind.

## 2026-11-16 (17)

### 27 topic control, and a correction to 25
Pliny NH 16, 44 chapters, 978 lines. Matched-distance test (lines 3-12 apart, same page vs across a break; null = breaks slid along, x400). All words / without 60 commonest: Pliny 1.05 (p .25) / 1.39 (p .010); Pliny lines dealt at random 1.02 / 1.07; Naibbe of Pliny 1.01 / 0.97; copying model 1.15 (.010) / 1.93 (.007); VMS herbal A 0.92 (.91) / 1.23 (.090); balneo B 1.36 (.005) / 1.48 (.015); stars B 1.15 (.017) / 1.39 (.007).

Correction: exp 25 claimed herbal pages have no vocabulary of their own and that vocabulary follows writing order, not the plant. The all-words statistic can't see Pliny's chapters either, so that claim had no support; withdrawn. Also fixed the expectation in 25/26/27 (types occurring once were counted as shareable): sum c(c-1)/(n(n-1)). Ratios unchanged. Herbal A, non-common words: paragraph 2.34, across break 1.70, same page 10-30 lines 1.67 [1.15-2.34], control 0.98. What stands from 25: common-word carry-over across the break (ratio 1.00 [0.84-1.18], 1.22x control), successor recognition, balneo break.

## 2026-11-16 (16)

### 26 writing order
Herbal A hand 1, sheets where next folio != conjugate: 11. Lift end-of-verso -> start of recto: book 1.52, conjugate 1.25, other rectos 1.18; diff 0.28 [-0.55, 0.91], 9/11 favour book. v -> next r inside quire 1.39 [1.08-1.72] (29), between quires 0.95 (3). Outlier f19v: 0 shared with f20r, 20 with f22r. Underpowered.

## 2026-11-16 (15)

### 24 vertical alignment
Matches (same or edit 1, len 3+) between lines k apart, same page, interior words; mean |dx| in glyphs vs upper-line interior shuffle x300. VMS lag 1: 17.18 vs 17.38, z -1.35, p .083 (A z -0.9, B z -1.3); lag 2: 16.60 vs 17.22 z -4.3; lag 3 z -3.5; lag 5 z -2.7; lag 8 z -2.4. Generator: 11.86 vs 13.97 z -16.6 (lag 2 -8.3, lag 3 -9.9). Latin z +0.3, Italian -1.9 (lag 5 -2.6), Naibbe -1.3. Margins included: VMS z -9.2. Sections: S z -2.4, B +0.5, H -0.2; hand 3 z -2.7.

### 25 page memory
Lift of shared types, pairs 1-5 lines apart. Herbal A (hand 1, 95 pp): paragraph 1.33 [1.15-1.51], page break 1.33 [1.14-1.51], r->v 1.37, v->r 1.28, control (end of p vs start of p+2..6) 1.09, same page 10-30 lines 0.95 [0.78-1.23], next page any lines 1.03, 10 pages on 0.97. Break/control 1.22 [1.05-1.41] p .001; break/paragraph 1.00 [0.84-1.18]. Balneo B (hand 2, 19 pp): 1.42 / 0.90 / control 0.84; r->v 0.67, v->r 1.17. Stars B (hand 3, 22 pp): 1.83 / 1.29 / 0.94; break/control 1.37 p .037. Successor test (last 5 vs first 5 lines, rank among block): herbal A mean pct .637, top tenth 25.6%, p < .001 (r->v .66, v->r .60 p .018); balneo .53 (r->v .39, v->r .68); stars .60.

## 2026-11-16 (14)

### 22 locality
Lift at lag 1 line, core/middle/low bands (10k words): VMS B 1.73/1.87/2.18, A 1.52/3.12/4.05, Latin 1.00/1.78/2.23, Italian 1.37/4.46/11.4, Naibbe 1.01/1.14/0.66, copying model 1.86/8.11/17.2. At lag 100: VMS B 1.04/1.43/1.17, model 0.95/0.88/0.56. global_p 0.6: core share .50 but cohesion 1.09. common_p (re-pick source if seen < 3 times) 0.3/0.5/0.7: distance 1.85/1.49/1.63 (sd .45/.25/.07), core share .40/.51/.64, cohesion 2.43/1.84/1.55, MATTR .58/.51/.42, h2 2.20/2.02/1.75. Rare-word lift still 6.8/13.5 at c .5. Three fitted rates now.

### 23 scorecard
Best model on 26 untuned measures, 8 seeds. B: 10 ok / 10 off / 6 wrong; A: 8 / 11 / 7. Wrong: q- words .014 vs .197, o- .074 vs .213, line-first d- .058 vs .143, t- .029 vs .101, q- .013 vs .205, 1-glyph words .003 vs .026. Right: near/in-line 1.06 vs 1.00, singleton one-edit .65 vs .63, mean length 5.21 vs 4.95. Model A-B distance 1.21 (VMS 1.31) but B-B across seeds 0.80. Benchmark is blind to glyph content; q deficit may be my port.

## 2026-11-16 (13)

### 20 singletons
First 10k words. Singleton make-up (one edit from a 2+ word / two known joined / neither): VMS A 64/15/22, B 63/15/23, copying model 66/12/22, Naibbe 81/2/16, Latin 17/1/82, Italian 18/26/56. Singleton rate first/middle/last: A .29/.17/.29, B .27/.13/.24, model B .29/.12/.11, Latin flat .24-.26. Paragraph openers .47, labels .36 (whole MS). Line-first singletons: glyph added at start 38-40% (mid 19-22%); line-last: glyph added at end 15-19% (mid 7-11%), y d g s m. Exp 14 tested swaps only; additions do happen at line end.

### 21 line-end rule
AutoCopy(line_end_p). q 0/.2/.4/.6/.8: distance 2.39/2.32/2.06/1.89/1.86, last-word singleton rate .11/.17/.22/.27/.33, line_last_jsd .028/.036/.048/.082/.095 (VMS B .065), hapax .553/.560/.570/.590/.598. Spectrum, 10k words: VMS B types x1 1575, x2 240, x3-5 223, x6-20 177, x21+ 87 (53.5% of tokens); model q=.5: 1681, 405, 402, 296, 58 (30.4%). The gap is the core, not the tail.

## 2026-11-16 (12)

### c07 Bax 2014
Key from his Appendix 1 (14 signs). 11665/38718 tokens use only his signs. Consonant skeletons (K N T R X S) vs 30 Wikipedia lexicons, against 1000 shuffles of his own values over the 10 consonant signs. VMS: 17-20/30 languages p <= .05 (Tatar, Uzbek, Azerbaijani, Arabic ~.001), best-language p .03-.10. Naibbe of Pliny: 21-23/30, Arabic/Persian p .001, best-language p .02. Self-citation generator: 0-6/30, best p .46-.70. ZL reads his Taurus label as dary (f68r1.6), not doary.

## 2026-11-16 (11)

### c06 tolor (r/voynich)
tolor f38r.1 (paragraph-initial), otolor labels f67r2 (1 of 64) and f77v (1 of 10). 1652 types with 2-5 occurrences; 61% of paragraph-opening words unique. Same layout (opening X, label oX, 2-5 total): tolor, torain, tokol, fcheody, pairar, palar, porain. l/r agreement vs in-line shuffle: VMS z 0.85 (A 2.09 p .017, B -1.07); Italian -a/-o z 16.1; Latin -a/-us 3.1, -am/-um 4.3. Context cosine / random: o- 1.53, t/k 1.98, l/r 1.77, q- 1.50, y- 1.45.

## 2026-11-16 (10)

### 19 copying model vocabulary
extra_change q (one more substitution per word), boundary p 0.65, B, 3 seeds. q 0/0.3/0.6/0.9: hapax 0.551/0.561/0.594/0.593, MATTR 0.564/0.590/0.595/0.599 (VMS B 0.535), cohesion 1.99/1.95/1.66/1.67, near 34.0/29.1/28.9/28.6 vs null 27.9/25.3/27.1/27.2. Hapax deficit is a shape problem (too few singletons, not too little variety). Not a comma artifact: VMS hapax 0.686/0.679/0.720 split/smart/join (exp 16).

## 2026-11-16 (9)

### 18 copying + boundary habit
AutoCopy(boundary=..., boundary_p=p). Fitted list from odd-line PMI > 0. B, 3 seeds. p 0/0.5/0.65/0.8/0.95: edge 0.013/0.057/0.115/0.227/0.508, core 0.98/0.83/0.71/0.79/1.85, distance ~2.42 until 0.95 (2.97), pattern r vs even lines 0.09/0.67/0.70/0.73/0.55. Random lists p 0.8: edge 0.18, r 0.02 (max 0.16). Odd vs even VMS r 0.98, so the hold-out is weak. Remaining misses: hapax 0.55, line_last -7, line-start d/t/q.

## 2026-11-16 (8)

### 17 self-citation (Timm & Schinner)
voynich/autocopy.py: reimplemented from VoynichTextGenerator's procedure and tables (their repo has no license; procedure only). 8 seeds x A/B settings, 1400 lines. Distance 2.45 / 2.46 (sd 0.15 / 0.20), core 1.03 / 0.97. Edge 0.009 / 0.013. Hapax 0.54. h2 2.35 / 2.22. Cohesion 1.45 / 2.01. Near-repeats 36.8 vs 28.2 in-line null (B); exact 7.8 vs 8.6 (generator drops half of immediate duplicates). Worst: line_last_jsd -7.3, line_first -3.0 (B). Line-initial d/t/q too rare.

Ciphers: right words, wrong lines. Copying: right lines, wrong words. Neither gives coupling except autokey.

## 2026-11-16 (7)

### 16 commas
Parser now takes `commas="split"|"smart"|"join"`. smart = glue across `,` when the result occurs 2+ times. Tokens 38718 / 37849 / 35973. Ranks among 18 historical texts, split/smart/join: h2 0/0/0, h1 1/1/1, word_mi 0/0/0, line_first 18/18/18, line_last 18/18/18, edge_coupling 15/11/9 (0.147/0.121/0.108). Shift split→smart 0.18 units vs A-B gap 1.17. Naibbe (Greshko) core 0.94/0.80/0.89.

Correction: edge coupling is real but not extreme; exp 13 target should be ~0.12 under smart.

## 2026-11-16 (6)

### 15 repeats
Exact repeats per 1000 adjacent pairs: VMS 9.37, words shuffled within their line 9.25 (300 shuffles, p 0.42; A 0.34, B 0.55), shuffled across the text 3.42. So exact repeats = line composition. Near-repeats (edit distance 1): 36.0 vs 30.8 in-line, p < 0.003 in all/A/B. Latin and Italian avoid immediate repeats (Aix 0 vs 4.4 expected); Naibbe inherits this (1.3 vs 3.1). Repeat rate by position: first pair 3.4, middle 11.1, last 5.9. Across line breaks 6 vs 11.8 expected. Near-repeat edits: mostly insert/delete, then r<->l, k<->t, c<->s, o<->a.

Consequence for the benchmark: `repeat_rate` and `line_cohesion` partly measure the same thing.

## 2026-11-15 (5)

### 14 line-end model
Mirror of 10 for line ends. Rewrites "-e → -m/-g" for 12 endings, ZL all/A/B + Takahashi: nothing significant (97 tests); -l→-m and -n→-m strongly negative (both partners favoured). Stem-level pooled test (stem+{r,l,s,n,in,iin,y,dy} vs stem+m): r −0.29 to −0.02, p 0.60-0.98. Line-final words shorter (4.73 vs 4.96 internal, 5.43 first). am ×23, dam ×12, otam ×12 at line end; al ×1.0, ar ×0.55, aiin ×0.61. Line start = rewrite, line end = selection/special forms.

### 13 autokey Naibbe
Reimplemented Naibbe from Greshko's tables; matches his ciphertext (h2 2.11/2.09, hapax 0.59/0.58, edge 0.004/0.004).

Autokey (last glyph of the previous word picks the next table from a fixed chart, with probability p): edge coupling 0.006 / 0.08 / 0.15 / 0.37 at p = 0 / 0.5 / 0.65 / 1; nothing else moves. p ≈ 0.65 matches the VMS for Pliny and Dante.

Pattern of coupling (PMI of last glyph x next initial): VMS odd vs even lines 0.98; random charts 0.00 (best 0.16); chart fitted on odd lines → simulated cipher vs even lines 0.43 (Pliny), 0.24 (Dante). Partial.

VMS coupling is not a comma artifact: 0.166 bits across certain spaces only (0.411 across uncertain ones).

Benchmark distance: 4.86 (published Naibbe) → 4.78 (+autokey) → 3.92 (+autokey + line-start rule, q=0.5). Untouched: line_last, repeat_rate, line_cohesion.

Bug on the way: a chart object that subclassed an empty dict was replaced by the default chart (`chart or DEFAULT`), so the first chart search returned nonsense (-0.04). Fixed (`is None`); the quick check done earlier outside the experiment had it right (0.47).

## 2026-11-15 (4)

### community tests (experiments/community)
Reran five outside claims with our data and controls; full notes in each folder.

- **c01 Naibbe (Greshko's own ciphertext).** Core distance 0.94, about as far from the reference as Currier B is (0.71); my reimplementation in 05 was 2.22, so that one was my fault. h2 2.09 matches. Misses: edge coupling 0.002 vs 0.18, hapax 0.58 vs 0.68. One-word-at-a-time ciphers can't produce coupling across word boundaries.
- **c02 uncertain spaces (Rozanova & Temerev).** Gluing across `,` gives a known word 33.7% of the time vs 3.7% for `.` and 82.8% for real word-internal cuts; edge MI 0.55 vs 0.16 and 1.70. Implies ~38% of commas are word-internal. Partly right.
- **c03 anagram decipherments.** With a 30k-word Italian vocabulary, random strings of 4-9 letters anagram into one or two Italian words 75-90% of the time; Voynich words through an arbitrary key 83-99%. A successful anagram is expected from noise.
- **c04 seasonal label prefixes (voynich.ninja 5817).** Prefix mix differs between signs (chi-square p < 0.001) for labels and also for ring text (p = 0.001). Ordered trend through the year: rho -0.60, p = 0.08. Page effect, not a season effect.
- **c05 re-cutting EVA.** Byte-pair merging: VMS h2/log2(alphabet) goes 0.46 → 0.56 → 0.53 (0, 40, 120 merges) while Latin/Italian/English fall from 0.64-0.70 to 0.53-0.57. They meet around 100-150 units, where a VMS word is ~1.8 units (natural texts 2.4-3.4). Looks like a syllabary or code, not a mis-cut alphabet.

### 12 scans
PDF scans of quire 20 (~1100x1536 px). Line detector tuned on alternate pages: held-out MAE 3.2 lines, within ±1 on 7/11; fails on f112r (damaged leaf), f104r skipped (half resolution). Space test on 187 lines: b/a 1.0-1.4 across thresholds but CI roughly 0-4. Inconclusive at this resolution.

## 2026-11-15 (3)

### correction on 08
Line-initial s is not new. Emma May Smith described a "linestart transformation" (Agnostic Voynich, 2015-2016: s, d, y added or swapped in at line start, sa-/so- words strongly line-initial esp. in Q20); Nick Pelling has long called line-initial s a likely null; voynich.ninja threads 2945, 4343 and 5309 cover it. 08 is a replication.

### 10 linestart model
Testing Smith's mechanism directly. For every word type x with 5+ line-internal uses: deficit(x) = how much rarer x is at line start than expected, surplus(g+x) = how much commoner g+x is there. If g+x at line start stands for x, the two should correlate across x.

| glyph | r (all) | p | Currier A | Currier B | Takahashi |
|---|---|---|---|---|---|
| s | 0.130 | <0.001 | 0.047 (ns) | 0.124 (<0.001) | 0.116 (<0.001) |
| d | 0.158 | <0.001 | 0.015 (ns) | 0.168 (<0.001) | 0.143 (0.001) |
| t | 0.097 | <0.001 | 0.021 (ns) | 0.101 (<0.001) | 0.102 (<0.001) |
| p | 0.070 | 0.007 | ns | 0.067 (0.019) | 0.077 (0.005) |
| y, q, k, l, r, o | negative or ns | | | | |

40 tests, so only p < 0.00125 counts: s, d, t survive, p doesn't. Strongest pairs: s+ain, s+aiin, s+ol, s+ar; d+aiin, d+ain, d+shedy; t+ol, t+chedy.

Reading: in Currier B, s/d/t at line start behave like something added to an ordinary word. y does not (Smith already suggested y replaces ch rather than being added). Nothing like this in Currier A. The correlations are modest: plenty of line-initial g-words are not g + a known word.

As far as we found, nobody has tested the transformation this way (deficit vs surplus with a permutation null). Needs a proper literature check before claiming it.

### 09 bifolia (singulion hypothesis)
101 leaves with 60+ words, pairs inside each quire, same scribe and same illustration type only. Conjoint leaves (same bifolium) vs other pairs:

- raw cosine: +0.022 vs -0.017 under random re-pairing, p = 0.002, higher in 9/10 quires
- tf-idf cosine: p = 0.53
- Jaccard without the 50 most common words: p = 0.43

So conjoint leaves share their common-word profile (which could be the scribe's state or the session) but not specific vocabulary. Suggestive at most. Not evidence for or against singulions on its own.

### 04 again, with better measures
Same-leaf (recto→verso) vs cross-leaf (verso→next recto): tf-idf cosine 0.116 vs 0.085 (p = 0.015), rare-word Jaccard 0.094 vs 0.068 (p < 0.001). This one holds: the two sides of a leaf share specific vocabulary more than pages that face each other across leaves. Still needs a baseline from a manuscript we know is bound correctly.

### 11 label reuse
758 single-word labels, 634 distinct, 63 repeated on 2+ pages, 49 of those across sections (e.g. otaly on 7 pages: zodiac, biological, pharmaceutical; otaldy on f70v2, f88r, f101v). Same-section share of repeat pairs 30.8% vs 22.6% when sections are shuffled (p = 0.009). Mostly short ot-/ok- forms, many rare in running text. Looks more like a stock of label words than unique names. Full list in results for checking against the scans.

## 2026-11-15 (2)

### parser fix
`{...}` in IVTFF are ligatures (`{ckh}`, `{cth}`, `{ikh}`), not comments. The first parser dropped them. Comments are `<!...>`. All numbers below use the fixed parser, so they differ slightly from entry (1).

### 08 line positions
Some frequent words almost only appear at the start of a line (dshedy 29/32, tchedy 25/34, pol, tol, sol, sor, sain, saiin). With shuffled words no top-300 word gets above a 3.4x ratio; these reach 4-8x.

Many look like a normal word with one glyph in front: d+shedy, t+chedy, s+ol, s+ain. Measured: removing the first glyph turns 60.6% of line-initial words into one of the 500 most common words, vs 40.4% of line-internal ones. Almost all of that comes from **s**: 52.4% at line start vs 7.7% mid-line (599 vs 3291 words). d, t, y show small differences.

Reading: line-initial s- behaves like something added to the word because it is at the start of the line. Next: check whether the stripped word is the one that *would* be expected there (e.g. compare with the last word of the previous line), and look at p/f in the same way.

### 07 word structure
Glyph positions inside words are far more fixed than in any comparison text: positional entropy 0.70 (A 0.71, B 0.63) vs 0.83-0.93 for Latin, Italian, Spanish, English, Icelandic, Hebrew, Georgian. Inside-word conditional entropy 2.13 vs 2.98-3.78. Same with Glen Claston's alphabet (0.72, 2.65), so it isn't an EVA artifact.

### 06 zodiac labels
Labels taken in ZL order (each has a clock position). 10 signs, 30 labels each (Gemini 29, Aries and Taurus split across two pages).

- **Cisiojanus (Pelling's idea)**: aligned label i with syllable i of that month's Cisiojanus, calendar month and sign span (21st to 20th), both reading directions. Mantel test of label similarity vs syllable similarity: 2 of 40 at p<0.05, which is what chance gives. **Null.** The Cisiojanus file syllabifies to exactly 365 syllables (31, 28, 31...), so it isn't a counting problem.
- **Position as number**: same-position labels across signs are slightly more alike by bigram Jaccard (+0.005, p=0.043), but nothing with prefix, suffix, first glyph or length (p 0.17-0.99). **Not robust**, treat as nothing.
- ot- share by sign: high in spring (Aries 73%, Pisces 53%), low in summer/autumn (Cancer 7%, Virgo 7%). Known already.

### 05 cipher benchmark
13 metrics, z-scored by the spread across 18 historical texts. VMS reference = first 10k paragraph words of ZL (mostly Currier A herbal, so "VMS Currier A" overlaps the reference and its 0.32 is optimistic; "later pages" at 1.04 and "Currier B" at 1.23 are the honest floor).

- Every cipher/generator: distance 5-6. Shuffled VMS words: 4.5. Nothing gets close.
- The four line metrics (line-start/end distributions, repeats, cohesion) are what nothing reproduces. Without them ("core"), plain Italian (1.69) is still closer than any cipher (2.06+).
- Verbose, syllable and Naibbe-like ciphers do reach VMS h2 (2.12-2.28) but lose the open vocabulary (hapax 0.22-0.41 vs 0.68) and edge coupling (~0 vs 0.15). Same conclusion as Rozanova & Temerev (2026) for published imitations.
- My self-citation generator is far too repetitive (cohesion 5-14). It's a crude version, not Timm & Schinner's. Next: run their actual generator (TorstenTimm/VoynichTextGenerator).
- My Naibbe-like cipher is my reading of the idea, not Greshko's tables.

### 04 page order
225 pages with 40+ words. Mean cosine between consecutive pages 0.366, random 0.217, shuffled within same hand and illustration type 0.314 (both p<0.0005). So the current order keeps real local structure.

Recto→verso of the same leaf (can't be separated by rebinding): 0.415, n=98. Verso→next recto: 0.329, n=99. Difference p=0.0006. Fits Layfield & Davis (2026): joins between leaves are weaker than inside a leaf. Caveat: the two sides of a leaf may have been written in one sitting even in a correct order. Need a baseline from a normal manuscript, and to redo this per singulion.

Weakest joins listed in results (f68r1→f68r2, f24v→f25r, f67v1→f68r1...).

### 03 scribes and Currier languages
Hand 1: 10,749 A / 0 B. Hand 2: 0 / 11,128. Hand 3: 750 / 10,908. Hands 4, 5: only B where marked. Closest vocabularies: hands 2-3 (JSD 0.27). Most distant: 1-5 (0.61). Marker words: hand 1 daiin, chol, chor, cthy; hand 2 shedy, qokedy, qol; hand 3 qokeey, al, lkaiin; hand 4 oteody, oteos.

### 02 languages
283 texts (265 Wikipedia + 18 historical) after dropping 28 whose script my tokenizer breaks into 1-glyph "words" (Brahmic scripts, Thaana, pointed Hebrew...). **None has h2 at or below the VMS (2.15).** Lowest: Sranan 2.59, Hakka 2.69, Venda 2.79. Even the GC transliteration (2.57) is below all of them. Nearest on six metrics combined: Venda, Tswana, Malagasy, Maori, Samoan — CV-syllable languages, but still far off on h2.

### 01 transliterations
Seven files, first 8000 paragraph tokens. EVA family (ZL, IT, RF, VT) agree closely (h2 2.148-2.151). Bigger-unit alphabets push h2 to 2.40-2.57: still under every natural text. Line-start effect 0.11-0.16 and cohesion 1.7-1.9 in every file. These are properties of the manuscript, not of the transcriber.

### 00 baseline
227 pages, 5,385 loci, 38,718 legible tokens, 8,048 types, 308 tokens dropped for uncertain glyphs. q word-initial 99.4%, then o 97.7%. p+f: 41.8 per 1000 glyphs on paragraph-first lines vs 2.7 elsewhere. Hapax 0.68, h2 2.11 on paragraph text.

By scribe: hand 3 has the strongest line-start effect (0.30), hand 4 the weakest (0.11).

## 2026-11-15 (1)

First pass with a simple parser. Baseline numbers matched Currier, Bennett, Zandbergen. h2 far below Latin/Italian means plain monoalphabetic substitution of either is out. Started the zodiac work.

## Next

- run Timm & Schinner's generator and Greshko's actual Naibbe tables through the benchmark
- benchmark metric from Zhang & Sheng: same-line word-pair tendency across 28 texts
- leaf test against a baseline from a manuscript we know is bound correctly
- check the cross-section repeated labels against the drawings
- glyph tracings (Trace the Voynich) once released: stroke-level stats
- f116v glyphs vs the main text's slot rules
- web explorer (GitHub Pages)
- parser option: decide each `,` by whether the glued form is a known word (c02), rerun benchmark
- port Timm & Schinner's generator from Swift and score it
- autokey: co-fit chart and tables on held-out lines; line-end and repeat mechanisms
- Elu-Sinhala claim once the Zenodo vocabulary is downloaded
- full-resolution scans + word alignment for the space question
