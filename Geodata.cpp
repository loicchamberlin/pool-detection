#include "Geodata.h"
#include <cpr/cpr.h>
#include <nlohmann/json.hpp> // Include a JSON library like nlohmann/json for handling JSON data

using json = nlohmann::json;

Geodata::Geodata(const std::string &address) : _address{address}
{
}

Geodata::~Geodata()
{
}

const std::pair<double, double> Geodata::retrieve_geolocalisation()
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