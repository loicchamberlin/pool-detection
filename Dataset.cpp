#include "Dataset.h"
#include <filesystem>

Dataset::Dataset(const Image main_image) : _main_image{main_image}
{
    // std::cout << "Dataset created" << std::endl;
}

void Dataset::create_imagette()
{
    cv::Mat image_to_crop = _main_image.get_image();
    int resolution = 224;
    int size = 448;

    int height = image_to_crop.rows;
    int width = image_to_crop.cols;

    int imgette_number_width = width / size;
    int imgette_number_height = height / size;

    for (int i = 0; i < imgette_number_height; i++)
    {
        for (int j = 0; j < imgette_number_width; j++)
        {
            // Convert integers to strings for file path
            std::string i_str = std::to_string(i);
            std::string j_str = std::to_string(j);

            cv::Rect roi(j * size, i * size, size, size);
            cv::Mat cropped_image = image_to_crop(roi).clone();
            std::string imagette_tmp_name = _main_image.get_image_name() + "_x_" + i_str + "_y_" + j_str + ".jpg";
            std::string imagette_tmp_path = _path_to_imagette + imagette_tmp_name;

            cv::resize(cropped_image, cropped_image, (cv::Size(resolution, resolution)));
            cv::imwrite(imagette_tmp_path, cropped_image);

            Imagette imagette_tmp{
                imagette_tmp_path,
                imagette_tmp_name,
                i, j};

            _imagette_dataset.push_back(imagette_tmp);
        }
    }
}

void Dataset::delete_imagette_files()
{
    namespace fs = std::filesystem;
    for (const auto &entry : fs::directory_iterator(_path_to_imagette))
    {
        std::cout << "This image is about to be deleted : " << entry.path() << std::endl;
        remove(entry.path());
    }
}

void Dataset::glue_imagette()
{
}

void Dataset::list_dataset()
{
    unsigned int datasetSize = _imagette_dataset.size();

    for (unsigned int i = 0; i < datasetSize; i++)
    {
        std::cout << "Here's lie the image number " << i << " : " << _imagette_dataset[i].get_image_name() << std::endl;
    }
}
