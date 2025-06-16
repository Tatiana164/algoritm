#include <iostream>
#include <cmath>


double simpson_rule(double (*f)(double), double a, double b, int n) {
    if (n % 2 == 1) n++; 
    double h = (b - a) / n;
    double sum = f(a) + f(b);

    for (int i = 1; i < n; i += 2)
        sum += 4 * f(a + i * h);

    for (int i = 2; i < n - 1; i += 2)
        sum += 2 * f(a + i * h);

    return (h / 3) * sum;
}


double function(double x) {
    return std::sin(0.5 * x) - 0.5 - std::sin(x);
}

int main() {
    setlocale(LC_ALL, "Russian");
    double a = 4.0; 
    double b = 5.0; 

    
    for (int n = 1; n <= 1000000; n += 100000) {
        double result = simpson_rule(function, a, b, n);
        std::cout << "Площадь фигуры для n = " << n << ": " << result << std::endl;
    }

    return 0;
}