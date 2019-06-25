# Robocup Pepper scenario data generator

This repo contains Python scripts which create json configuration files that we use in [General Manager](https://github.com/jacques-saraydaryan/robocup_pepper-general_mng) and [HRI](https://github.com/Elyspio/robocup_pepper-hri_meta).


## Installation

You can use Python 2 or Python 3.

We use Google Sheet store our data, so you need get your credentials [Google API client](https://developers.google.com/drive/api/v3/quickstart/python).




## Use

 First clone the repo:
`git clone https://github.com/Elyspio/robocup_pepper-scenario_data_generator.git data-generator`
 
 Move to the repo locally:
`cd data-generator`

 Install dependencies: 
`pip install -r requirement.txt`

> If you don't have root permissions use: `pip install --user requirement.txt`  

 Then launch the script generator.py:

`python ./generator.py`

### Options

| Flag              | Args                      | Description                                                              |
| ----------------- | ------------------------- | ------------------------------------------------------------------------ |
| --local,  -l      | \<Path>                   | Indicates if local excel files will be used (need a path to root folder). |
| --output, -o      | \<Path>                   | The output folder for generated jsons.                                   |
| --online          | \<Google Drive folder id> | The folder id of the Google Drive scenarios root folder.                 |
| --save-online, -s |                           | Indicates if excel files should be saved on disk.                        |
