#include <iostream>
#include "Image.h"
#include "Image.cpp"
#include "Dataset.h"
#include "Dataset.cpp"
#include "Geodata.h"
#include "Geodata.cpp"
#include "Imagette.h"
#include "Imagette.cpp"

int main(int argc, char **argv)
{

    // Reading the image file
    std::string name = "ballonviolet";
    std::string image_path = "../ressources/Images/Images_raw/ballon.jpg";
    std::string address = "40160 Ychoux, France";

    Image my_img{image_path, name};

    Dataset first_dataset{my_img};

    if (my_img.get_image().empty())
    {
        std::cerr << "Could not open or find the image." << std::endl;
        return -1;
    }

    first_dataset.create_imagette();

    first_dataset.list_dataset();

    first_dataset.delete_imagette_files();

    cv::destroyAllWindows();

    return 0;
}