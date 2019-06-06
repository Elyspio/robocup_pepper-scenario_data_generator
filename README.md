# Robocup Pepper scenario data generator

This repo contains a python script which creates json configuration files that we use in [General Manager](https://github.com/jacques-saraydaryan/robocup_pepper-general_mng) and [HRI](https://github.com/Elyspio/robocup_pepper-hri_meta).


## Installation

You can use Python 2 or Python 3.

We use .xlsx format to store our data, so you need to install [xlrd](https://pypi.org/project/xlrd/) on your python installation

`pip install xldr`

> if you don't have root permissions use: `pip install --user xlrd`  


## Use

> First clone the repo:

`git clone https://github.com/Elyspio/robocup_pepper-scenario_data_generator.git data-generator`
 
> Move to the repo locally:

`cd data-generator`

> Then launch json_generator.py:

`python ./json_generator.py`

Generated data will be located in the folder `dist/`