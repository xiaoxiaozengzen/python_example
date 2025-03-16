#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include "my_math.hpp"

namespace py = pybind11;
constexpr auto byref = py::return_value_policy::reference_internal;

PYBIND11_MODULE(MyMath, m) {
    m.doc() = "optional module docstring";

    py::class_<MyClass>(m, "MyClass")
    .def(py::init<double>())  
    .def("run", &MyClass::run, py::call_guard<py::gil_scoped_release>())
    .def_readonly("data_a", &MyClass::data_a, byref)
    ;
}