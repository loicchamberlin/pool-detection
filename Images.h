#pragma once
#include <iostream>
#include <opencv2/opencv.hpp>
#include <cpr/cpr.h>

class Image
{
private:
    std::string _image_path;
    std::string _name;
    std::string _address;
    double _longitude = 0;
    double _latittude = 0;

public:
    Image(const std::string &image_path,
          const std::string &name,
          const std::string &address) : _image_path{image_path},
                                        _name{name},
                                        _address{address}
    {
        std::cout << "Path & name given" << std::endl;
    };
    ~Image() { std::cout << "Image destroyed" << std::endl; };

    cv::Mat get_image() { return cv::imread(_image_path); };

    std::string get_image_name() { return _name; };
    std::string get_image_path() { return _image_path; };
    std::string get_address() { return _address; };

    void save_img(std::string save_path) { cv::imwrite(save_path, cv::imread(_image_path)); };

    const std::pair<double, double> retrieve_geolocalisation();
    double get_longitude() { return _longitude; };
    double get_latittude() { return _latittude; };

    void create_imagette();
    void imagette_processed();
    void recreate_image();
};
