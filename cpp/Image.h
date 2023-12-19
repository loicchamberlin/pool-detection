#pragma once
#include <iostream>
#include <opencv2/opencv.hpp>
#include <cpr/cpr.h>

class Image
{
private:
    std::string _image_path;
    std::string _name;

public:
    Image(const std::string &image_path,
          const std::string &name) : _image_path{image_path},
                                     _name{name} {
                                         // std::cout << "Path & name given" << std::endl;
                                     };
    ~Image(){}; // std::cout << "Image destroyed" << std::endl; };

    const cv::Mat get_image() const { return cv::imread(_image_path); };
    void set_image(cv::Mat image_new) { cv::imwrite(_image_path, image_new); };

    const std::string get_image_name() const { return _name; };
    const std::string get_image_path() const { return _image_path; };

    void save_img(std::string save_path) { cv::imwrite(save_path, cv::imread(_image_path)); };

    void imagette_processed();
    void recreate_image();
};
