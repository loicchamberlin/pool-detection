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
    int size = 224;

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
        // std::cout << "This image is about to be deleted : " << entry.path() << std::endl;
        remove(entry.path());
    }
}

void Dataset::recreate_image()
{
    // Find the maximum x and y values to determine the size of the composite image
    int maxX = 0, maxY = 0;
    for (auto &imagette : _imagette_dataset)
    {
        maxX = std::max(maxX, imagette.get_pos_y());
        maxY = std::max(maxY, imagette.get_pos_x());
    }

    // Calculate the size of the composite image
    int compositeWidth = (maxX + 1) * _imagette_dataset[0].get_image().rows;
    int compositeHeight = (maxY + 1) * _imagette_dataset[0].get_image().cols;

    // Create the composite image
    cv::Mat compositeImage(compositeHeight, compositeWidth, _imagette_dataset[0].get_image().type(), cv::Scalar(0, 0, 0));

    // Copy imagettes to the composite image
    for (auto &imagette : _imagette_dataset)
    {
        std::cout << "x : " << imagette.get_pos_x() << " & y : " << imagette.get_pos_x() << std::endl;
        cv::Rect roi(imagette.get_pos_y() * _imagette_dataset[0].get_image().rows, imagette.get_pos_x() * _imagette_dataset[0].get_image().cols,
                     imagette.get_image().rows, imagette.get_image().cols);
        imagette.get_image().copyTo(compositeImage(roi));
    }
    // changer le nom de l'image
    cv::imwrite("./ressources/Images/Images_processed/" + _main_image.get_image_name() + "_processed.jpg", compositeImage);
}

void Dataset::apply_inference() // for later, add the inference processing here to draw then the rectangle around pool detected
{
    for (auto &imagette : _imagette_dataset)
    {
        // Top Left Corner
        cv::Point p1(30, 30);

        // Bottom Right Corner
        cv::Point p2(100, 100);

        int thickness = 2;
        cv::Mat imagette_tmp = imagette.get_image();
        // Drawing the Rectangle
        cv::rectangle(imagette_tmp, p1, p2, cv::Scalar(0, 0, 255), thickness);

        imagette.set_image(imagette_tmp);
    }
}

void Dataset::list_dataset()
{
    unsigned int datasetSize = _imagette_dataset.size();

    for (unsigned int i = 0; i < datasetSize; i++)
    {
        std::cout << "Here's lie the image number " << i << " : " << _imagette_dataset[i].get_image_name() << std::endl;
    }
}
