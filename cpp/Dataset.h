#pragma once
#include "Image.h"
#include "Imagette.h"

class Dataset
{
private:
    int _lenght = 0;
    std::string _path_to_imagette = "./ressources/Images/Images_cropped/";
    std::string _path_to_main_image = "./ressources/Images/Images_raw/";

    const Image _main_image;
    std::vector<Imagette> _imagette_dataset;

public:
    Dataset(const Image main_image);
    ~Dataset(){}; // std::cout << "dataset of images destroyed" << std::endl; };
    void list_dataset();

    void get_main_image(); // download the sattelite image from the aera chosen by the user || Don't WORK (allocation memory problem)

    void create_imagette();       // create the dataset + save the imagette into _path_to_imagette
    void delete_imagette_files(); // free the folder _path_to_imagette from the imagette precedently saved

    void recreate_image();  // glue back together imagette processed by inference with pools drawn
    void apply_inference(); // for the moment, random rectangle drawn onto the imagette
};
