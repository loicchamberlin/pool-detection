#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <thread>
#include <vector>
#include <cmath>
#include <cstring>
#include <curl/curl.h>

cv::Mat download_tile(const std::string &url, const std::map<std::string, std::string> &headers, int channels)
{
    std::cout << "Im here & " << url << std::endl;
    CURL *curl = curl_easy_init();
    if (!curl)
    {
        std::cerr << "Failed to initialize curl" << std::endl;
        return cv::Mat();
    }

    CURLcode res;
    std::vector<unsigned char> buffer;

    struct curl_slist *headerlist = NULL;

    for (const auto &header : headers)
    {
        std::string header_str = header.first + ": " + header.second;
        headerlist = curl_slist_append(headerlist, header_str.c_str());
    }

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headerlist);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, [](void *ptr, size_t size, size_t nmemb, void *data) -> size_t
                     {
        size_t total_size = size * nmemb;
        std::vector<unsigned char>& buffer = *static_cast<std::vector<unsigned char>*>(data);
        buffer.insert(buffer.end(), static_cast<unsigned char*>(ptr), static_cast<unsigned char*>(ptr) + total_size);
        return total_size; });
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buffer);

    res = curl_easy_perform(curl);

    curl_easy_cleanup(curl);
    curl_slist_free_all(headerlist);

    if (res != CURLE_OK)
    {
        std::cerr << "Failed to download tile" << std::endl;
        return cv::Mat();
    }

    cv::Mat img = cv::imdecode(buffer, channels == 3 ? 1 : -1);
    return img;
}

std::pair<double, double> project_with_scale(double lat, double lon, double scale)
{
    double siny = std::sin(lat * M_PI / 180);
    siny = std::min(std::max(siny, -0.9999), 0.9999);
    double x = scale * (0.5 + lon / 360);
    double y = scale * (0.5 - std::log((1 + siny) / (1 - siny)) / (4 * M_PI));
    return std::make_pair(x, y);
}

void build_row(int tile_y, int tl_tile_x, int br_tile_x, int tl_pixel_x, int tl_pixel_y, int img_w, int img_h, const std::string &url, const std::map<std::string, std::string> &headers, int zoom, int tile_size, int channels, const cv::Mat &img)
{
    for (int tile_x = tl_tile_x; tile_x < br_tile_x + 1; ++tile_x)
    {
        cv::Mat tile = download_tile(url + "?x=" + std::to_string(tile_x) + "&y=" + std::to_string(tile_y) + "&z=" + std::to_string(zoom), headers, channels);
        std::cout << "Im here after download  tile" << std::endl;
        if (!tile.empty())
        {
            int tl_rel_x = tile_x * tile_size - tl_pixel_x;
            int tl_rel_y = tile_y * tile_size - tl_pixel_y;
            int br_rel_x = tl_rel_x + tile_size;
            int br_rel_y = tl_rel_y + tile_size;

            int img_x_l = std::max(0, tl_rel_x);
            int img_x_r = std::min(img_w + 1, br_rel_x);
            int img_y_l = std::max(0, tl_rel_y);
            int img_y_r = std::min(img_h + 1, br_rel_y);

            int cr_x_l = std::max(0, -tl_rel_x);
            int cr_x_r = tile_size + std::min(0, img_w - br_rel_x);
            int cr_y_l = std::max(0, -tl_rel_y);
            int cr_y_r = tile_size + std::min(0, img_h - br_rel_y);

            tile(cv::Rect(cr_x_l, cr_y_l, cr_x_r - cr_x_l, cr_y_r - cr_y_l)).copyTo(img(cv::Rect(img_x_l, img_y_l, img_x_r - img_x_l, img_y_r - img_y_l)));
        }
    }
}

cv::Mat download_image(double lat1, double lon1, double lat2, double lon2,
                       int zoom, const std::string &url, const std::map<std::string, std::string> &headers, int tile_size, int channels)
{
    double scale = 1 << zoom;

    auto tl_proj = project_with_scale(lat1, lon1, scale);
    auto br_proj = project_with_scale(lat2, lon2, scale);

    int tl_pixel_x = tl_proj.first * tile_size;
    int tl_pixel_y = tl_proj.second * tile_size;
    int br_pixel_x = br_proj.first * tile_size;
    int br_pixel_y = br_proj.second * tile_size;

    int tl_tile_x = tl_proj.first;
    int tl_tile_y = tl_proj.second;
    int br_tile_x = br_proj.first;
    int br_tile_y = br_proj.second;

    int img_w = std::abs(tl_pixel_x - br_pixel_x);
    int img_h = br_pixel_y - tl_pixel_y;

    cv::Mat img(img_h, img_w, CV_8UC3, cv::Scalar(0, 1, 0));

    std::vector<std::thread> threads;

    for (int tile_y = tl_tile_y; tile_y <= br_tile_y; ++tile_y)
    {
        std::cout << "Im here before thread append" << std::endl;
        threads.emplace_back(build_row, tile_y, tl_tile_x, br_tile_x, tl_pixel_x, tl_pixel_y, img_w, img_h, url, headers, zoom, tile_size, channels, std::ref(img));
        std::cout << "Im here after thread append" << std::endl;
    }

    for (auto &thread : threads)
    {
        std::cout << "Im here before thread join" << std::endl;
        thread.join();
        std::cout << "Im here after thread join" << std::endl;
    }

    return img;
}

std::pair<int, int> image_size(double lat1, double lon1, double lat2,
                               double lon2, int zoom, int tile_size)
{
    double scale = 1 << zoom;
    auto tl_proj = project_with_scale(lat1, lon1, scale);
    auto br_proj = project_with_scale(lat2, lon2, scale);

    int tl_pixel_x = tl_proj.first * tile_size;
    int tl_pixel_y = tl_proj.second * tile_size;
    int br_pixel_x = br_proj.first * tile_size;
    int br_pixel_y = br_proj.second * tile_size;

    return std::make_pair(std::abs(tl_pixel_x - br_pixel_x), br_pixel_y - tl_pixel_y);
}

int main()
{
    int zoom = 14;
    int channels = 3;
    int tile_size = 256;
    double lat1 = 44.333732;
    double lon1 = -0.963802;
    double lat2 = 44.321988;
    double lon2 = -0.939601;
    std::string url = "https://mt.google.com/vt/lyrs=s&";
    std::map<std::string, std::string> headers;

    headers["cache-control"] = "max-age=0";
    headers["sec-ch-ua"] = "' Not A;Brand';v='99', 'Chromium';v='99', 'Google Chrome';v='99'";
    headers["sec-ch-ua-mobile"] = "?0";
    headers["sec-ch-ua-platform"] = "'Windows'";
    headers["sec-fetch-dest"] = "document";
    headers["sec-fetch-mode"] = "navigate";
    headers["sec-fetch-site"] = "none";
    headers["sec-fetch-user"] = "?1";
    headers["upgrade-insecure-requests"] = "1";
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36";

    cv::Mat img = download_image(lat1, lon1, lat2, lon2, zoom, url,
                                 headers, tile_size, channels);

    if (!img.empty())
    {
        cv::imshow("Map", img);
        cv::waitKey(0);
    }

    std::string name = "test_download_img.jpg";
    cv::imwrite(name, img);

    return 0;
}