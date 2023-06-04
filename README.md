## Final Project for Modern Data Analytics [G0Z39a]: Noise in Leuven

### Introduction
This Github repository contains source code of our final project for Modern Data Analytics [G0Z39a] at KU Leuven. 
We developed a web application via Dash and Plotly, with the goal of showcasing interactive visualizations on the connections between noise and meteorological data collected in Leuven. 
Additionally, our ideas on modeling for predicting types of noise are also included in this APP.


### Usage
#### Remote Access
Since the APP has been deployed on Render, users can simply access the APP via the link below:  
https://mda-hungary-2023.onrender.com/

#### Local Installation 
Users can either access the web application locally in case remote server might be not available. 
First clone the project and open it on your IDE, then run the command below to install all the dependencies listed in 
`requirements.txt`.
```
python -m pip install -r requirements.txt
```
Next, user can access the web application in localhost server by running the script `app.py`. 



### Repository Structure

    .
    ├── .idea                  
    ├── assets                # Folder that stores figures used in App
    ├── src                   # Source files for app
    ├── modeling              # py scripts and notebooks used in modeling stage
    ├── pre-processing        # py scripts and notebooks used in pre-processing
    ├── README.md             # readme file
    ├── render.yaml           # file for APP deployment
    └── requirements.txt