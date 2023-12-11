#include "Image.h"

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <iomanip>
#include <nlohmann/json.hpp> // Include a JSON library like nlohmann/json for handling JSON data

using json = nlohmann::json;

void Image::imagette_processed()
{
    // add a rectangle on an image (random for the moment)
}

void Image::recreate_image()
{
    // reassemble the normal image
    // OR
    // using the coordinates (of the rectangle) + the images number (x,y) : add this rectangle to the original image
}
