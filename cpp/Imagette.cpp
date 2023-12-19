#include "Imagette.h"

Imagette::Imagette(const std::string &image_path,
                   const std::string &name,
                   const int x,
                   const int y)
    : Image{image_path, name},
      _pos_x{x},
      _pos_y{y}
{
    // std::cout << "Imagette created" << std::endl;
}

Imagette::~Imagette()
{
    // std::cout << "Imagette destroyed" << std::endl;
}