# fire-detection-system
University of Messina A.Y. 2023/2024 | Distributed Systems Project | Prof: Antonio Puliafito (antonio.puliafito@unime.it)

# Overview
In recent years, the rapid development of technologies for the Internet of
Things (IoT) and distributed systems has led to a significant evolution in
the field of smart cities. In this context, the integration of intelligent and
automated solutions is revolutionising urban infrastructure management,
offering new opportunities to improve the safety, efficiency and quality of
life of citizens.
The project presented is placed in this scenario and aims to simulate a
solution for emergency management in urban areas, with particular at-
tention to the detection and management of risk situations. Through the
adoption of advanced technologies, such as reliable communication pro-
tocols, containerised infrastructures and distributed architectures, it has
been possible to create a scalable system adaptable to the modern needs
of smart cities.

# Installation
The “project” folder is divided into three subfolders. To make the system work, these steps must be followed.

- Distribution of nodes
<br/>Node 1: container orchestrator 
<br/>Node 2: container controller
<br/>Node 3: container database
<br/>Node 4: container network
<br/>Node 5: container webgui

- VPN network configuration.
Each node has its own IP address connected to the shared VPN network (overlay network). Depending on where you installed the reference container, change the IP address appropriately in the FlaskConfig.py and Database.py class files within the container folder files.

- Install containers
1. Open the terminal
2. $: cd folderName
3. $: docker compose up -d

- Test the system from the terminal
1. Open several terminals to simulate sensors and actuators (change folder name based on which device to connect to the system)
2. $: cd Terminal/Sensor1
3. $: python sensor.py

<strong>PLEASE NOTE:</strong></br>
It was not possible to upload the “model” folder within the Project/Raspberry/Sensor Fire Camera/ path because of the heavy file load. The model folder is the trained model of Machine Learning with SVM algorithm. It is recommended to download the full folder from the Google Drive made available below or train your own SVM model.
<br><br>
The files that must be present are:
- scaler.joblib
- svm_model.joblib
- X_train.npy

# Project Folder
<a href="https://drive.google.com/drive/folders/1BsQhkn5JYtl5DHnSZOlqfL8Krp2Dj1vx?usp=sharing" target="_blank">Google Drive Folder</a> <br>
<a href="https://www.youtube.com/watch?v=PkMYUouv5AA" target="_blank">Demonstration Video</a>

# Credits
- Allegra Davide Giuseppe
- Miano Alberto
- Musmeci Edoardo
