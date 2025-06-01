#include <iostream>
#include <vector>
#include <chrono> 


void addElements(std::vector<int>& arr, int N) {
    for (int i = 0; i < N; ++i) {
        arr.push_back(i); 
    }
}

int main() {
    setlocale(LC_ALL, "Russian");
    int N;
    std::cout << "Введите количество элементов N: ";
    std::cin >> N;
    std::vector<int> arr; 
    arr.reserve(N); 

  
    auto start = std::chrono::high_resolution_clock::now();
    addElements(arr, N); 
    auto end = std::chrono::high_resolution_clock::now();

  
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
    double milliseconds = duration / 1000.0;

   
    std::cout << "Размер массива: " << arr.size() << std::endl;
    std::cout << "Емкость массива: " << arr.capacity() << std::endl;


    std::cout << "Время выполнения: " << milliseconds << " миллисекунд" << std::endl;

    return 0;
}