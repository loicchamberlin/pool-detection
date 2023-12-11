#pragma once
#include <iostream>

class Geodata
{
private:
    std::string _address;
    double _longitude = 0;
    double _latittude = 0;

public:
    Geodata(const std::string &address);
    ~Geodata();

    const std::pair<double, double> retrieve_geolocalisation();

    const std::string get_address() { return _address; };
    const double get_longitude() { return _longitude; };
    const double get_latittude() { return _latittude; };
};
