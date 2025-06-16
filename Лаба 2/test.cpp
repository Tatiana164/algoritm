#include <gtest/gtest.h>
#include <cmath>
#include "Лаба 2"

// Объявляем функции из основного проекта
extern double simpson_rule(double (*f)(double), double a, double b, int n);
extern double function(double x);

// Тестовая функция x^2
double test_function(double x) {
    return x * x;
}

// Тест 1: Проверка метода Симпсона на x^2 в [0, 1]
TEST(SimpsonRuleTest, QuadraticFunction) {
    double a = 0.0, b = 1.0;
    int n = 10;
    double expected = 1.0 / 3.0; // Аналитический интеграл x^2 от 0 до 1 = 1/3
    double result = simpson_rule(test_function, a, b, n);
    EXPECT_NEAR(result, expected, 1e-6);
}

// Тест 2: Проверка обработки нечетного n
TEST(SimpsonRuleTest, OddNHandling) {
    double a = 0.0, b = 1.0;
    int n = 9; // Нечетное, должно стать 10
    double expected = 1.0 / 3.0;
    double result = simpson_rule(test_function, a, b, n);
    EXPECT_NEAR(result, expected, 1e-6);
}

// Тест 3: Проверка целевой функции на [4, 5] для n=10
TEST(SimpsonRuleTest, TargetFunction) {
    double a = 4.0, b = 5.0;
    int n = 10;
    double expected = 0.672738; // Численное значение с высокой точностью
    double result = simpson_rule(function, a, b, n);
    EXPECT_NEAR(result, expected, 1e-5);
}

// Тест 4: Проверка сходимости для больших n
TEST(SimpsonRuleTest, Convergence) {
    double a = 4.0, b = 5.0;
    double expected = 0.672738;
    double result1 = simpson_rule(function, a, b, 1000);
    double result2 = simpson_rule(function, a, b, 100000);
    EXPECT_NEAR(result1, expected, 1e-6);
    EXPECT_NEAR(result2, expected, 1e-7);
}

// Тест 5: Проверка значений функции function(x)
TEST(FunctionTest, TargetFunctionValues) {
    EXPECT_NEAR(function(4.0), std::sin(0.5 * 4.0) - 0.5 - std::sin(4.0), 1e-10);
    EXPECT_NEAR(function(4.5), std::sin(0.5 * 4.5) - 0.5 - std::sin(4.5), 1e-10);
    EXPECT_NEAR(function(5.0), std::sin(0.5 * 5.0) - 0.5 - std::sin(5.0), 1e-10);
}


