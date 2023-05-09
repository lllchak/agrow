#include "func.h"

long double ag_asin(double source) {
    long double result = source;

    if (source > ADOMAIN || source < -ADOMAIN)
        result = NAN;
    else if (source == ADOMAIN)
        result = PI / 2;
    else if (source == -ADOMAIN)
        result = -(PI / 2);
    else {
        long int n = 1;
        long double term = source;

        while (!(ag_is_zero(term))) {
        term *= ((source * source) * (2 * n - 1) * (2 * n - 1)) /
                ((2 * n) * (2 * n + 1));
        result += term;
        n++;
        }
    }

    return result;
}

long double ag_acos(double source) {
    double result = (PI / 2) - ag_asin(source);
    return result;
}

long double ag_atan(double source) {
    long double atan = ag_acos(1 / ag_sqrt(1 + source * source));
    if (source <= EPS) atan = EPS;
    return atan;
}

int8_t ag_is_zero(double source) {
    return ag_fabs(source) < EPS * EPS;
}

long double ag_fabs(double source) {
    return (source > 0) ? source : (-source);
}

long int ag_abs(long int source) {
    return (source > 0) ? source : (-source);
}

long double ag_sqrt(double source) {
    double result = 1;
    double new_root = MAX_DOUBLE;

    do {
        new_root = (result + source / result) / 2;
        if (ag_fabs(result - new_root) < EPS) break;
        else result = new_root;
    } while (!(ag_fabs(result - new_root) > EPS));

    return result;
}

long double ag_sin(double source) {
    long int n = 1;
    double result = source, term = source;

    while (!ag_is_zero(term / n)) {
        term *= (-1) * (source * source) / ((2 * n + 1) * (2 * n));
        result += term;
        n++;
    }

    return result;
}

long double ag_cos(double source) {
    return ag_sin(PI / 2.0 - source);
}

long double ag_tan(double source) {
    return ag_sin(source) / ag_cos(source);
}

long double ag_ceil(double source) {
    int floored = source;
    if (source - floored && source > 0.) return (long double)(floored + 1);
    return (long double)floored;
}

long double ag_floor(double source) {
    int floored = source;
    if (source - floored && source < 0.) return (long double)(floored - 1);
    return (long double)floored;
}

long double ag_fmod(double x, double y) {
    long double div = (long double)(x) / y;
    return (double)(div - ((int)div)) * y;
}

long double ag_exp(double x) {
    int flag = 0;
    if (x < 0) {
        x = -x;
        flag = 1;
    }

    long double res = 1.0;
    int n = 1;
    long double el = x;

    while (el > EPS) {
        if (el == INF) break;
        res += el;
        el *= (x / ++n);
    }

    res = (double)res;

    return (flag) ? 1 / (long double)res : (long double)res;
}

long double ag_log(double x) {
    long double ans = 0.0;

    if (x < 0) {
        ans = NAN;
    } else if (x < 1) {
        long double alpha = (x - 1) / (x + 1);
        ans = alpha;
        long double save = ans * alpha * alpha;

        for (int i = 2; i <= INT16_MAX; i++) {
            ans += (1.0 / (2 * i - 1)) * save;
            save = save * alpha * alpha;
        }

        ans = (double)ans;

        ans = (x > 0) ? (long double)(2.0 * ans) : -INF;
    } else if (x >= 1) {
        int cnt = 0;
        while (x > EXP) {
            x /= EXP;
            cnt++;
        }

        long double prev = x - 1.0;
        ans = prev;

        do {
            prev = ans;
            long double exp_val = ag_exp(prev);
            ans = prev + 2 * ((x - exp_val) / (x + exp_val));
        } while (prev - ans > EPS);

        ans = (double)ans;

        ans = (long double)ans + cnt;
    }

    return ans;
}

long double ag_pow(double base, double exp) {
    base = (exp < 0) ? (1.0 / base) : base;
    exp = (exp < 0) ? -exp : exp;

    return (base < 0 && !isdigit(exp)) ? NAN : ag_exp(exp * ag_log(base));
}
