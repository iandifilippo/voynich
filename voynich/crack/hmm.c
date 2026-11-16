#include <stdlib.h>
#include <math.h>
#include <string.h>

/* Hidden Markov model over a symbol stream. obs[t] < 0 breaks the chain.
   A: K*K transitions (row = from), pi: K, B: K*V emissions (row = state). */

static double forward(const int *obs, int n, int V, int K, const double *A, const double *pi,
                      const double *B, double *alpha, double *scale) {
    double ll = 0.0;
    int fresh = 1;
    for (int t = 0; t < n; t++) {
        double *a = alpha + (size_t)t * K;
        int o = obs[t];
        if (o < 0) { fresh = 1; scale[t] = 1.0; memset(a, 0, K * sizeof(double)); continue; }
        if (fresh) {
            for (int j = 0; j < K; j++) a[j] = pi[j] * B[(size_t)j * V + o];
            fresh = 0;
        } else {
            const double *p = a - K;
            for (int j = 0; j < K; j++) {
                double s = 0.0;
                for (int i = 0; i < K; i++) s += p[i] * A[i * K + j];
                a[j] = s * B[(size_t)j * V + o];
            }
        }
        double s = 0.0;
        for (int j = 0; j < K; j++) s += a[j];
        if (s <= 0) s = 1e-300;
        for (int j = 0; j < K; j++) a[j] /= s;
        scale[t] = s;
        ll += log(s);
    }
    return ll;
}

double loglik(const int *obs, int n, int V, int K, const double *A, const double *pi, const double *B) {
    double *alpha = malloc((size_t)n * K * sizeof(double));
    double *scale = malloc((size_t)n * sizeof(double));
    double ll = forward(obs, n, V, K, A, pi, B, alpha, scale);
    free(alpha); free(scale);
    return ll;
}

double em(const int *obs, int n, int V, int K, double *A, const double *pi, double *B,
          int iters, int learn_A, double smooth) {
    double *alpha = malloc((size_t)n * K * sizeof(double));
    double *scale = malloc((size_t)n * sizeof(double));
    double *beta = malloc(K * sizeof(double)), *nb = malloc(K * sizeof(double));
    double *cB = malloc((size_t)K * V * sizeof(double));
    double *cA = malloc((size_t)K * K * sizeof(double));
    double ll = 0.0;
    for (int it = 0; it < iters; it++) {
        ll = forward(obs, n, V, K, A, pi, B, alpha, scale);
        for (size_t i = 0; i < (size_t)K * V; i++) cB[i] = smooth;
        for (int i = 0; i < K * K; i++) cA[i] = smooth;
        int have = 0;
        for (int t = n - 1; t >= 0; t--) {
            int o = obs[t];
            if (o < 0) { have = 0; continue; }
            const double *a = alpha + (size_t)t * K;
            if (!have) {
                for (int i = 0; i < K; i++) beta[i] = 1.0;
                have = 1;
            } else {
                int o1 = obs[t + 1];
                double s1 = scale[t + 1];
                for (int i = 0; i < K; i++) {
                    double s = 0.0;
                    for (int j = 0; j < K; j++) {
                        double x = A[i * K + j] * B[(size_t)j * V + o1] * beta[j] / s1;
                        s += x;
                        if (learn_A) cA[i * K + j] += a[i] * x;
                    }
                    nb[i] = s;
                }
                memcpy(beta, nb, K * sizeof(double));
            }
            for (int i = 0; i < K; i++) cB[(size_t)i * V + o] += a[i] * beta[i];
        }
        for (int i = 0; i < K; i++) {
            double s = 0.0;
            for (int v = 0; v < V; v++) s += cB[(size_t)i * V + v];
            for (int v = 0; v < V; v++) B[(size_t)i * V + v] = cB[(size_t)i * V + v] / s;
            if (learn_A) {
                s = 0.0;
                for (int j = 0; j < K; j++) s += cA[i * K + j];
                for (int j = 0; j < K; j++) A[i * K + j] = cA[i * K + j] / s;
            }
        }
    }
    free(alpha); free(scale); free(beta); free(nb); free(cB); free(cA);
    return ll;
}
