#include "Images.h"

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <iomanip>
#include <nlohmann/json.hpp> // Include a JSON library like nlohmann/json for handling JSON data

using json = nlohmann::json;

const std::pair<double, double> Image::retrieve_geolocalisation()
{
    // Replace spaces with '+'
    std::string &address_withplus = _address;
    std::replace(address_withplus.begin(), address_withplus.end(), ' ', '+');

    try
    {
        // Make an HTTP GET request to the geocoding service
        auto r = cpr::Get(cpr::Url{"https://geocode.maps.co/search?q=" + address_withplus});
        std::string my_json = r.text;

        // Parse JSON data
        json data = json::parse(my_json);

        std::cout << data << std::endl;

        // Extract latitude and longitude from the JSON response
        double latittude = std::stod(data[0]["lat"].get<std::string>());
        double longitude = std::stod(data[0]["lon"].get<std::string>());

        _longitude = longitude;
        _latittude = latittude;

        return std::make_pair(latittude, longitude);
    }
    catch (const std::exception &e)
    {
        // Handle exceptions, e.g., print an error message
        std::cerr << "Error: " << e.what() << std::endl;
        return std::make_pair(0.0, 0.0); // Return a default value or handle the error accordingly
    }
}

void Image::create_imagette()
{
    cv::Mat image_to_crop = cv::imread(_image_path);
    int resolution = 224;
    int size = 448;

    int height = image_to_crop.rows;
    int width = image_to_crop.cols;

    int imgette_number_width = width / size;
    int imgette_number_height = height / size;

    std::cout << "imgette_number_width : " << imgette_number_width << " and imgette_number_height : " << imgette_number_height << std::endl;

    for (int i = 0; i < imgette_number_height; i++)
    {
        for (int j = 0; j < imgette_number_width; j++)
        {
            // Convert integers to strings for file path
            std::string i_str = std::to_string(i);
            std::string j_str = std::to_string(j);

            std::cout << "I'm here in the image i : " << i << " and here j : " << j << std::endl;

            cv::Rect roi(j * size, i * size, size, size);
            cv::Mat cropped_image = image_to_crop(roi).clone();

            cv::resize(cropped_image, cropped_image, (cv::Size(resolution, resolution)));
            cv::imwrite("../ressources/Images/Images_cropped/" + _name + "_x_" + i_str + "_y_" + j_str + ".jpg", cropped_image);

            cv::imshow("cropped_image", cropped_image);
            cv::waitKey(0);

            cv::destroyAllWindows();
        }
    }
}

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
