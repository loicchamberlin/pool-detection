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
    std::string image_path = "./ressources/Images/Images_raw/gojo4k.jpg";
    // std::cout << "Give me an image path" << std::endl;
    // std::cin >> image_path;
    std::string address = "40160 Ychoux, France";

    Image my_img{image_path, name};

    Dataset first_dataset{my_img};

    if (my_img.get_image().empty())
    {
        std::cerr << "Could not open or find the image." << std::endl;
        return -1;
    }
    else
    {
        first_dataset.create_imagette();

        // first_dataset.list_dataset();

        first_dataset.apply_inference();
        first_dataset.recreate_image();
        first_dataset.delete_imagette_files();

        Geodata dateee{address};

        std::cout << dateee.get_address() << std::endl;

        cv::destroyAllWindows();

        return 0;
    }
}