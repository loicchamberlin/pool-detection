#include <iostream>
#include "Images.h"
#include "Images.cpp"

int main(int argc, char **argv)
{

    // Reading the image file
    std::string name = "ballonviolet";
    std::string image_path = "../ressources/Images/Images_raw/ballon.jpg";
    std::string address = "2 Impasse Pasteur, 40160 Ychoux, France";

    Image my_img{image_path, name, address};

    if (my_img.get_image().empty())
    {
        std::cerr << "Could not open or find the image." << std::endl;
        return -1;
    }

    // Create a window to display the video frames
    namedWindow("picture", cv::WINDOW_NORMAL);

    // Loop over the video frames and display them in the window
    /*while (true)
    {

        // Display the current frame in the window
        imshow("Video", my_img.get_image());

        // Wait for a key press (or 30 milliseconds) to allow the frame to be displayed
        if (cv::waitKey(30) >= 0)
        {
            break;
        }
    }*/

    std::cout << my_img.get_image_name() << " & " << my_img.get_image_path() << std::endl;
    std::cout << my_img.get_address() << std::endl;

    // my_img.retrieve_geolocalisation();

    // std::cout << my_img.get_latittude() << " & " << my_img.get_longitude() << std::endl;

    my_img.create_imagette();

    // my_img.save_img("../ballon2.jpg", my_img.get_image());
    // Release the video file and destroy the window
    cv::destroyAllWindows();

    return 0;
}