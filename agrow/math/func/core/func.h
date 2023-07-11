#ifndef __FUNC_CORE_FUNC_H__
#define __FUNC_CORE_FUNC_H__

#include <ctype.h>
#include <stdint.h>
#include <stdbool.h>

#define AG_EPS 1e-17
#define AG_PI 3.14159265358979324
#define AG_EXP 2.71828182845904523
#define AG_NAN 0.0 / 0.0
#define AG_INF 1.0 / 0.0
#define AG_MAX_DOUBLE 1.7976931348623157e308
#define AG_ADOMAIN 1

/*
    @brief This function is a series expansion of math function arcsin(x)
    @param source is a real number - an argue for arcsin function
    @return a value of the function arcsin(x)
*/
long double ag_asin(double source);

/*
    @brief This function is a series expansion of math function arcsin(x).
            It's easy to calculate this value using function asin(x) like PI -
            asin(x).
    @param source is a real number - an argue for arccos function
    @return a vlue of the function arccos(x)
*/
long double ag_acos(double source);

/*
    @brief This functions is a series expansion of math function arctg(x).
    @param source is a real number - an argue for arctg function
    @return a value of the function arctg(x)
*/
long double ag_atan(double source);

/*
    @brief This function is for checking real numbers close to zero
    @param source is a real number
    @return true or false(bool)
*/
bool ag_is_zero(double source);

/*
    @brief This function is for getting an absolute value of the real number
    @param source is a real number
    @return an absolute value of the real number
*/
long double ag_fabs(double source);

/*
    @brief This function is for getting an absolute value of the integer number
    @param source is a integer number
    @return an absolute value of the integet number
*/
long int ag_abs(long int source);

/*
    @brief This function is for getting value of the sqrt(x) function
    @param source is a real number
    @return a value of the function sqrt(x)
*/
long double ag_sqrt(double source);

/*
    @brief This function is for getting value of the sin(x) function
    @param source is a real number
    @return a value of the functions sin(x)
*/
long double ag_sin(double source);

/*
    @brief This function is for getting value of the cos(x) function
    @param source is a real number
    @return a value of the functions cos(x)
*/
long double ag_cos(double source);

/*
    @brief This function is for getting value of the tan(x) function
    @param source is a real number
    @return a value of the functions tan(x)
*/
long double ag_tan(double source);

/*
    @brief This function is for getting value of the ceil(x) function
    @param source is a real number
    @return a value of the functions ceil(x)
*/
long double ag_ceil(double source);

/*
    @brief This function is for getting value of the fmod(x, y) function
    @param source is a real number
    @return a value of the functions fmod(x, y)
*/
long double ag_fmod(double x, double y);

/*
    @brief This function is for getting value of the floor(x) function
    @param source is a real number
    @return a value of the functions floor(x)
*/
long double ag_floor(double source);

/*
    @brief This function is for getting value of the exp(x) function
    @param source is a real number
    @return a value of the functions exp(x)
*/
long double ag_exp(double x);

/*
    @brief This function is for getting value of the log(x) function
    @param source is a real number
    @return a value of the functions log(x)
*/
long double ag_log(double x);

/*
    @brief This function is for getting value of the pow(x) function
    @param source is a real number
    @return a value of the functions pow(x)
*/
long double ag_pow(double base, double exp);

#endif  // __FUNC_CORE_FUNC_H__
