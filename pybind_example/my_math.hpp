#include <iostream>

class MyClass {
public:
    double data_a;


public:
    MyClass(){}
    MyClass( double a_in) 
    {
        data_a = a_in;
    }

    void run() 
    { 
        std::cout << "MyClass" << std::endl;
    }
};