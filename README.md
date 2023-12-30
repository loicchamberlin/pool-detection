# pool-detection Computer Vision Project (Python/C++)

Problematic : Is it possible to simply detect pools using Computer Vision on maps ?

**Input** : 
- Name of a town (string)

**Output** : 
- Number of pools (integer)
- List of geographical positions (longitude, latitude)


## Process of [main.py](https://github.com/loicchamberlin/pool-detection/blob/main/Python/main.py)

1. Get the geolocalisation of the town (longitude,latitude)
2. Use of functions of this [project](https://github.com/andolg/satellite-imagery-downloader) to download the main image of the chosen town 
3. Cut the Main Image into multiple Imagette that have the required format for the Deep Learning Model (224,224,3)
4. Iterate the inference process through the imagette
5. Retrieve the data from the inference
6. Convert the pixel positions into geolocalisation 
7. Recreate main image with imagette
8. Display main image with pools detected (bounding boxes predicted)
9. Print number of pools detected
10. Print list of pools geolocalisation
11. Save this data into a json file and the modified main image

## Roadmap

1. C++ : 
    - Use of C++ implementation in order to create a simple application : FAILED 
        - CAN'T load models with Torch because of *version compatibility problem* 
        - CAN'T get sattelite image downloader script working because of *threading usage*
    - Structure for the main program with OOP : 90% (miss the two above features)

2. Python : 
    - Install detectron2 and discover its usage : DONE
    - Save a first basic RCNN model for tests : DONE
    - Reorganize the directory for OOP usage : DONE
    - Recreate the OOP Structure from my C++ program into Python : DONE
    - Add a function to convert pixel position *(x,y)* to geolocalisation *(longitude, latitude)* : DONE
    - Modify geodata.py function download_satellite_image() to save the image with a right name : DONE
    - Create unitests : TO DO
    - Create functionnalities for inference use : TO DO
    - Add UI to simplify use : TO DO

3. DEEP LEARNING in Python : 
    - Get deeper knowlegde of modifications that can be done in the training in order to get better results (mAP)
    - Simplify the **Training Part** by creating a script *or* method in a class
    - Simplify the **Evaluation Part** by creating a script *or* method in a class
    - Add another models to compare the performance (Transformer Based or Basic Neural Network for instance)

4. USE : 
    - Write documentations
    - Write installation guide
    - Write an article (can be segmented in 3 parts)
    - Write examples

## Installation

In order to use this project, an API key is needed.
You'll need to create an account on [geocode](https://geocode.maps.co) and create an account.

Then, when you have an API key, you can add it to your .env file.
```GEOCODE_API_KEY=[add the API key here]``` 