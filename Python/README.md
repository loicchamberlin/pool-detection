# pool-detection Computer Vision Project 

Part of the project where I train models and evaluate them.

Here's my few things to do in order to understand the poor performance of my models : 
    
1. Visual Inspection: Examine predictions on new images to identify specific patterns of failure. Look for common scenarios where the model struggles.
   - Create functions to display the results of inference and to compare between models easily

    2. Metrics Analysis: Evaluate performance using different metrics and consider breaking down performance by different classes to identify if certain classes are particularly challenging.
        a. Define the metrics the metrics to use 
        b. Understand them
        b. Create functions to automate the evaluation process

    3. Additional Data Collection: If feasible, consider augmenting your training dataset with more diverse examples that resemble the new images.  
        a. Look for tools that helps for the creation of dataset easily

    4. Ensemble Methods: Experiment with ensemble methods, combining predictions from multiple models or variations of your current model.
        a. Modify training paramaters to see the change that it adds to the result, either on the validation dataset or on a entirely new one (unknown from the models)



## Usage/Examples

- In [dataset_analysis.ipynb](https://github.com/loicchamberlin/pool-detection/blob/main/Python/dataset_analysis.ipynb), you can perform a dataset analysis in order to get statistical informations about the color characteristics of your dataset. For instance, this helps to define what could be the difference between two datasets. 

- In [model_training.ipynb](https://github.com/loicchamberlin/pool-detection/blob/main/Python/model_training.ipynb), you can perform the training of a dataset using Detectron2 library. You can also evaluate the performance of your model within this jupyter notebook.


