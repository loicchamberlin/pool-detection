#pragma once
#include "Image.h"

class Imagette : public Image
{
private:
    const int _pos_x; // position x in the main image
    const int _pos_y; // position y in the main image

public:
    Imagette(const std::string &image_path,
             const std::string &name,
             const int x,
             const int y);
    ~Imagette();

    const int get_pos_x() { return _pos_x; };
    const int get_pos_y() { return _pos_y; };
};
