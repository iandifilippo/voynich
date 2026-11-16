# 30 solver calibration (target: Latin)


## plaintext: Latin

| cipher | spaces | symbols | letters right | score per letter | real Latin | in Latin words | real Latin in words | sample |
|---|---|---|---|---|---|---|---|---|
| substitution | kept | 26 | 0.999 | -0.907 | -0.910 | 0.261 | 0.261 | albert of aixhistoria hierosolymitanae expeditionisliber icap i prooem |
| homophonic 50 | kept | 50 | 0.999 | -0.907 | -0.910 | 0.261 | 0.261 | albert of aixhistoria hierosolymitanae expeditionisliber icap i prooem |
| homophonic 100 | kept | 100 | 0.999 | -0.907 | -0.910 | 0.261 | 0.261 | albert of aixhistoria hierosolymitanae expeditionisliber icap i prooem |
| homophonic 200 | kept | 200 | 0.999 | -0.907 | -0.910 | 0.261 | 0.261 | albert of aixhistoria hierosolymitanae expeditionisliber icap i prooem |
| homophonic 400 | kept | 400 | 0.999 | -0.907 | -0.910 | 0.261 | 0.261 | albert of aixhistoria hierosolymitanae expeditionisliber icap i prooem |
| homophonic 50 | removed | 50 | 0.994 | -0.989 | -0.994 | 0.290 | 0.291 | albertofaithistoriahierosolymitanaeetpeditionislibericapiprooemiumsequ |
| homophonic 200 | removed | 200 | 0.990 | -0.989 | -0.994 | 0.280 | 0.291 | albertofaithistoriahierosolymitanaeetpeditionislibericapiprooemiumsequ |
| homophonic 400 | removed | 400 | 0.988 | -0.990 | -0.994 | 0.275 | 0.291 | albertofaithistoriahierosolymitanaeexpeditionislibericapiprooemiumsequ |

## plaintext: Hungarian

| cipher | spaces | symbols | letters right | score per letter | real Latin | in Latin words | real Latin in words | sample |
|---|---|---|---|---|---|---|---|---|
| substitution | kept | 26 | None | -1.239 | -0.910 | 0.001 | None | py sna dree rodamentetion sidenae sna drs iesu sdrs#elel sna alecer ro |
| homophonic 50 | kept | 50 | None | -1.210 | -0.910 | 0.002 | None | pn nsi crae totidesteseos retasia lsi ctr teli nctr#enen nsi enalet to |
| homophonic 100 | kept | 100 | None | -1.223 | -0.910 | 0.003 | None | ab rni proe detimenseseen negonao rni pdr teri rpdr#elel rni aleced de |
| homophonic 200 | kept | 200 | None | -1.216 | -0.910 | 0.001 | None | as rni pree diticansesoen notenae rni pdr teri rpdr#elel rsi alemed di |
| homophonic 400 | kept | 400 | None | -1.224 | -0.910 | 0.003 | None | ay rsa pree decasessesees neserto rsa fls pari lcdn#arau rra theled da |
| homophonic 50 | removed | 50 | None | -1.177 | -0.994 | 0.019 | None | abrnisreeteticensesoentotenaernistuperirstr#elelrnialesettesicenstoaro |
| homophonic 200 | removed | 200 | None | -1.203 | -0.994 | 0.006 | None | peiedeemnaravenissusreusaletlaeveoessanaeae#susiaidtisataaredenisastes |
| homophonic 400 | removed | 400 | None | -1.182 | -0.994 | 0.008 | None | teaisyosdasadeleensnriosanesleedgoeesinieae#sosiaesthnssaaradesieascas |

## plaintext: scrambled Latin

| cipher | spaces | symbols | letters right | score per letter | real Latin | in Latin words | real Latin in words | sample |
|---|---|---|---|---|---|---|---|---|
| substitution | kept | 26 | None | -1.379 | -0.910 | 0.001 | None | dletir ou aireitoasla neesariiobtlsaeo enoaauleraentasdl usia a eoarsu |
| homophonic 50 | kept | 50 | None | -1.374 | -0.910 | 0.000 | None | eanelu ru crullestaen alsedttrrheaicsr sarcciesunseemieo ialn t srnaei |
| homophonic 100 | kept | 100 | None | -1.361 | -0.910 | 0.000 | None | nredis eu eastoteeuna steniciiigsraeei eneeiinenaelsetnr isii e eiispi |
| homophonic 200 | kept | 200 | None | -1.354 | -0.910 | 0.001 | None | aisero ra sraeresteed ietenannsgoeesls sirndresatleosmee earm n sntieb |
| homophonic 400 | kept | 400 | None | -1.329 | -0.910 | 0.002 | None | ntesom iu aersoraesso tneseneeavntmaea eiieiateuaendonst ssee e eiudnd |
| homophonic 50 | removed | 50 | None | -1.302 | -0.994 | 0.004 | None | dneretepietueneeitituosasaeefnnsieeeteiistotiolnauddsseieeeitrseratalo |
| homophonic 200 | removed | 200 | None | -1.288 | -0.994 | 0.003 | None | ealerunasseerinsoaduetatirrsyeeorndmensnramamnairoeeeismtsstaaslireses |
| homophonic 400 | removed | 400 | None | -1.268 | -0.994 | 0.005 | None | earonirfilaoneynteleissrissyueeetslsernsuisasteecraetecrulnpetossmopas |
