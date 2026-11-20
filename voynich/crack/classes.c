#include <math.h>
#include <stdlib.h>
#include <string.h>

/* Exchange clustering (Kneser & Ney 1993; Martin, Liermann & Ney 1998):
   put word types into K classes so that the mutual information between the
   classes of adjacent tokens is as large as possible.

   seq: token ids, -1 = boundary (no bigram across it). cls: in/out class per type.
   Returns the final class-bigram MI in nats per bigram. */

static double xlx(double x) { return x > 0 ? x * log(x) : 0.0; }

typedef struct { int n; int *to; int *cnt; } Adj;

static void build(const int *seq, int n, int V, Adj *right, Adj *left) {
    int *rc = calloc(V, sizeof(int)), *lc = calloc(V, sizeof(int));
    for (int t = 0; t + 1 < n; t++) if (seq[t] >= 0 && seq[t + 1] >= 0) { rc[seq[t]]++; lc[seq[t + 1]]++; }
    for (int v = 0; v < V; v++) {
        right[v].to = malloc((rc[v] + 1) * sizeof(int)); right[v].cnt = malloc((rc[v] + 1) * sizeof(int)); right[v].n = 0;
        left[v].to = malloc((lc[v] + 1) * sizeof(int)); left[v].cnt = malloc((lc[v] + 1) * sizeof(int)); left[v].n = 0;
    }
    for (int t = 0; t + 1 < n; t++) {
        int a = seq[t], b = seq[t + 1];
        if (a < 0 || b < 0) continue;
        Adj *r = &right[a]; int k;
        for (k = 0; k < r->n && r->to[k] != b; k++);
        if (k == r->n) { r->to[k] = b; r->cnt[k] = 0; r->n++; }
        r->cnt[k]++;
        Adj *l = &left[b];
        for (k = 0; k < l->n && l->to[k] != a; k++);
        if (k == l->n) { l->to[k] = a; l->cnt[k] = 0; l->n++; }
        l->cnt[k]++;
    }
    free(rc); free(lc);
}

double exchange(const int *seq, int n, int V, int K, int *cls, int passes) {
    Adj *right = malloc(V * sizeof(Adj)), *left = malloc(V * sizeof(Adj));
    build(seq, n, V, right, left);
    double *N = calloc((size_t)K * K, sizeof(double)), *L = calloc(K, sizeof(double)), *R = calloc(K, sizeof(double));
    double total = 0;
    for (int v = 0; v < V; v++)
        for (int k = 0; k < right[v].n; k++) {
            int a = cls[v], b = cls[right[v].to[k]];
            N[a * K + b] += right[v].cnt[k]; L[a] += right[v].cnt[k]; R[b] += right[v].cnt[k]; total += right[v].cnt[k];
        }
    double *rw = calloc(K, sizeof(double)), *lw = calloc(K, sizeof(double));
    double *row = calloc(K, sizeof(double)), *col = calloc(K, sizeof(double));
    for (int pass = 0; pass < passes; pass++) {
        int moved = 0;
        for (int w = 0; w < V; w++) {
            if (right[w].n == 0 && left[w].n == 0) continue;
            int a = cls[w];
            memset(rw, 0, K * sizeof(double)); memset(lw, 0, K * sizeof(double));
            double self = 0, sr = 0, sl = 0;
            for (int k = 0; k < right[w].n; k++) {
                int u = right[w].to[k]; double c = right[w].cnt[k];
                if (u == w) self += c; else rw[cls[u]] += c;
                sr += c;
            }
            for (int k = 0; k < left[w].n; k++) {
                int u = left[w].to[k]; double c = left[w].cnt[k];
                if (u != w) lw[cls[u]] += c;
                sl += c;
            }
            /* remove w from a */
            for (int c = 0; c < K; c++) { N[a * K + c] -= rw[c]; N[c * K + a] -= lw[c]; }
            N[a * K + a] -= self;
            L[a] -= sr; R[a] -= sl;
            /* gain of putting w into class b, relative to an empty move */
            int best = a; double bestgain = -1e300;
            for (int b = 0; b < K; b++) {
                double g = 0;
                for (int c = 0; c < K; c++) {
                    if (c == b) continue;
                    g += xlx(N[b * K + c] + rw[c]) - xlx(N[b * K + c]);
                    g += xlx(N[c * K + b] + lw[c]) - xlx(N[c * K + b]);
                }
                g += xlx(N[b * K + b] + rw[b] + lw[b] + self) - xlx(N[b * K + b]);
                g -= xlx(L[b] + sr) - xlx(L[b]);
                g -= xlx(R[b] + sl) - xlx(R[b]);
                if (g > bestgain + 1e-12) { bestgain = g; best = b; }
            }
            int b = best;
            for (int c = 0; c < K; c++) { N[b * K + c] += rw[c]; N[c * K + b] += lw[c]; }
            N[b * K + b] += self;
            L[b] += sr; R[b] += sl;
            if (b != a) { cls[w] = b; moved++; }
        }
        if (!moved) break;
    }
    double mi = 0;
    for (int a = 0; a < K; a++) for (int b = 0; b < K; b++) mi += xlx(N[a * K + b]);
    for (int a = 0; a < K; a++) mi -= xlx(L[a]) + xlx(R[a]);
    mi = mi / total + log(total);
    for (int v = 0; v < V; v++) { free(right[v].to); free(right[v].cnt); free(left[v].to); free(left[v].cnt); }
    free(right); free(left); free(N); free(L); free(R); free(rw); free(lw); free(row); free(col);
    return mi;
}
