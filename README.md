# pool-detection Computer Vision Project (Python/C++)

Problematic : Is it possible to simply detect pools using Computer Vision on maps ?

**Input** : 
- Name of a town (string)

**Output** : 
- Number of pools (integer)
- List of geographical position (longitude, lattitude)


## Process

    1. Retrive multiple imagette from the chosen town
    2. Use detection algorithm trained on findings pools on pictures
    3. Saved these positions
