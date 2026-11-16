/* Simulated annealing for "symbol -> short letter string" ciphers.
 *
 * A ciphertext is a stream of symbol ids. Each symbol stands for a unit: a
 * string of 0-3 plaintext letters. The key is one unit per symbol. The decoded
 * letters are scored with a 4-gram language model. Covers simple and
 * homophonic substitution (units = single letters) and verbose/syllabic
 * schemes where a cipher word stands for one or two letters.
 *
 * tokens: >= 0 symbol id, -1 boundary (unknown word, line end), -2 space.
 * lm: log10 P(d | a b c), indexed ((a*A + b)*A + c)*A + d, A = alphabet size.
 * The last letter of the alphabet (A-1) is the boundary mark.
 */
#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static uint64_t rs;
static inline uint64_t rnd(void) {
    rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs;
}
static inline double unif(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }

static double score(const int *tok, int n, const int *assign, const int8_t *units,
                    const int8_t *ulen, const float *lm, int A, int space) {
    int a = A - 1, b = A - 1, c = A - 1;
    double s = 0;
    for (int i = 0; i < n; i++) {
        int t = tok[i];
        if (t >= 0) {
            int u = assign[t];
            const int8_t *p = units + 4 * u;
            for (int k = 0; k < ulen[u]; k++) {
                int d = p[k];
                s += lm[((a * A + b) * A + c) * A + d];
                a = b; b = c; c = d;
            }
        } else {
            int d = (t == -2) ? space : A - 1;
            if (d == c && d == A - 1) continue;
            s += lm[((a * A + b) * A + c) * A + d];
            a = b; b = c; c = d;
        }
    }
    return s;
}

/* score of tokens lo..hi inclusive, with context taken from the tokens before lo */
static double seg(const int *tok, int n, const int *assign, const int8_t *units,
                  const int8_t *ulen, const float *lm, int A, int space, int lo, int hi) {
    int ctx[3] = {A - 1, A - 1, A - 1};
    int got = 0;
    /* walk back until three letters of context are known */
    for (int i = lo - 1; i >= 0 && got < 3; i--) {
        int t = tok[i];
        if (t >= 0) {
            int u = assign[t];
            const int8_t *p = units + 4 * u;
            for (int k = ulen[u] - 1; k >= 0 && got < 3; k--) ctx[2 - got++] = p[k];
        } else {
            ctx[2 - got++] = (t == -2) ? space : A - 1;
            if (t == -1) { while (got < 3) ctx[2 - got++] = A - 1; }
        }
    }
    int a = ctx[0], b = ctx[1], c = ctx[2];
    double s = 0;
    if (hi >= n) hi = n - 1;
    for (int i = lo; i <= hi; i++) {
        int t = tok[i];
        if (t >= 0) {
            int u = assign[t];
            const int8_t *p = units + 4 * u;
            for (int k = 0; k < ulen[u]; k++) {
                int d = p[k];
                s += lm[((a * A + b) * A + c) * A + d];
                a = b; b = c; c = d;
            }
        } else {
            int d = (t == -2) ? space : A - 1;
            s += lm[((a * A + b) * A + c) * A + d];
            a = b; b = c; c = d;
        }
    }
    return s;
}

/* sum of seg() over the merged windows [i, i+3] around every occurrence of s1 (and s2) */
static double local(const int *tok, int n, const int *assign, const int8_t *units,
                    const int8_t *ulen, const float *lm, int A, int space,
                    const int *start, const int *occ, int s1, int s2) {
    int i1 = start[s1], e1 = start[s1 + 1];
    int i2 = s2 >= 0 ? start[s2] : 0, e2 = s2 >= 0 ? start[s2 + 1] : 0;
    double s = 0;
    int lo = -1, hi = -1;
    while (i1 < e1 || i2 < e2) {
        int p;
        if (i2 >= e2 || (i1 < e1 && occ[i1] <= occ[i2])) p = occ[i1++]; else p = occ[i2++];
        if (lo < 0) { lo = p; hi = p + 3; }
        else if (p <= hi + 1) { if (p + 3 > hi) hi = p + 3; }
        else { s += seg(tok, n, assign, units, ulen, lm, A, space, lo, hi); lo = p; hi = p + 3; }
    }
    if (lo >= 0) s += seg(tok, n, assign, units, ulen, lm, A, space, lo, hi);
    return s;
}

/* lambda * sum_l n_l * log10(q_l / p_l): 0 when the decoded letters have the language's frequencies */
static double freq_term(const double *cnt, const double *target, int A, double lambda) {
    double tot = 0, s = 0;
    for (int l = 0; l < A; l++) if (target[l] > -90) tot += cnt[l];
    if (tot <= 0) return 0;
    for (int l = 0; l < A; l++)
        if (target[l] > -90 && cnt[l] > 0) s += cnt[l] * (target[l] - log10(cnt[l] / tot));
    return lambda * s;
}

/* returns best score; assign is input (start key) and output (best key).
 * Units must not be empty: the windows above rely on every token giving a letter. */
double anneal(const int *tok, int n, int nsym, int *assign, const int8_t *units,
              const int8_t *ulen, int nunits, const float *lm, int A, int space,
              long iters, double t0, double t1, uint64_t seed, const double *symw,
              const double *target, double lambda) {
    rs = seed * 2654435761u + 88172645463325252ULL;
    int *best = malloc(sizeof(int) * nsym);
    int *start = calloc(nsym + 2, sizeof(int));
    for (int i = 0; i < n; i++) if (tok[i] >= 0) start[tok[i] + 1]++;
    for (int s = 0; s < nsym; s++) start[s + 1] += start[s];
    int *fill = malloc(sizeof(int) * (nsym + 1));
    memcpy(fill, start, sizeof(int) * (nsym + 1));
    int *occ = malloc(sizeof(int) * (n + 1));
    for (int i = 0; i < n; i++) if (tok[i] >= 0) occ[fill[tok[i]]++] = i;
    /* letter counts of the decoded text, kept up to date, for the frequency term */
    double cnt[64];
    for (int l = 0; l < A; l++) cnt[l] = 0;
    for (int sy = 0; sy < nsym; sy++) {
        int u = assign[sy], k = start[sy + 1] - start[sy];
        for (int j = 0; j < ulen[u]; j++) cnt[units[4 * u + j]] += k;
    }
    double fq = lambda > 0 ? freq_term(cnt, target, A, lambda) : 0;
    double cur = score(tok, n, assign, units, ulen, lm, A, space) + fq, bestv = cur;
    memcpy(best, assign, sizeof(int) * nsym);
    double cum_total = 0;
    double *cum = malloc(sizeof(double) * nsym);
    for (int i = 0; i < nsym; i++) { cum_total += symw[i]; cum[i] = cum_total; }
    double ratio = pow(t1 / t0, 1.0 / (double)iters), T = t0;
    for (long it = 0; it < iters; it++, T *= ratio) {
        double r = unif() * cum_total;
        int lo = 0, hi = nsym - 1;
        while (lo < hi) { int m = (lo + hi) / 2; if (cum[m] < r) lo = m + 1; else hi = m; }
        int s1 = lo, old1 = assign[s1], s2 = -1, old2 = -1, new1;
        if (unif() < 0.3) {
            s2 = rnd() % nsym;
            if (s2 == s1 || assign[s2] == old1) continue;
            old2 = assign[s2];
            new1 = old2;
        } else {
            new1 = rnd() % nunits;
            if (new1 == old1) continue;
        }
        double before = local(tok, n, assign, units, ulen, lm, A, space, start, occ, s1, s2);
        int k1 = start[s1 + 1] - start[s1], k2 = s2 >= 0 ? start[s2 + 1] - start[s2] : 0;
        double fq_new = fq;
        if (lambda > 0) {
            for (int j = 0; j < ulen[old1]; j++) cnt[units[4 * old1 + j]] -= k1;
            for (int j = 0; j < ulen[new1]; j++) cnt[units[4 * new1 + j]] += k1;
            if (s2 >= 0) {
                for (int j = 0; j < ulen[old2]; j++) cnt[units[4 * old2 + j]] -= k2;
                for (int j = 0; j < ulen[old1]; j++) cnt[units[4 * old1 + j]] += k2;
            }
            fq_new = freq_term(cnt, target, A, lambda);
        }
        assign[s1] = new1;
        if (s2 >= 0) assign[s2] = old1;
        double after = local(tok, n, assign, units, ulen, lm, A, space, start, occ, s1, s2);
        double nw = cur + after - before + fq_new - fq;
        if (nw >= cur || unif() < exp((nw - cur) / T)) {
            cur = nw; fq = fq_new;
            if (cur > bestv) { bestv = cur; memcpy(best, assign, sizeof(int) * nsym); }
        } else {
            assign[s1] = old1;
            if (s2 >= 0) assign[s2] = old2;
            if (lambda > 0) {
                for (int j = 0; j < ulen[old1]; j++) cnt[units[4 * old1 + j]] += k1;
                for (int j = 0; j < ulen[new1]; j++) cnt[units[4 * new1 + j]] -= k1;
                if (s2 >= 0) {
                    for (int j = 0; j < ulen[old2]; j++) cnt[units[4 * old2 + j]] += k2;
                    for (int j = 0; j < ulen[old1]; j++) cnt[units[4 * old1 + j]] -= k2;
                }
            }
        }
    }
    memcpy(assign, best, sizeof(int) * nsym);
    bestv = score(tok, n, assign, units, ulen, lm, A, space);
    free(best); free(cum); free(start); free(fill); free(occ);
    return bestv;
}

double score_key(const int *tok, int n, const int *assign, const int8_t *units,
                 const int8_t *ulen, const float *lm, int A, int space) {
    return score(tok, n, assign, units, ulen, lm, A, space);
}
