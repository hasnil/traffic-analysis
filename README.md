## Introduction

This project deals with analyzing and interactively mapping City of Calgary traffic incident and volume data. Sources are ENSF 592 course documents and City of Calgary records.

## First Phase

Running main_traffic_analysis_GUI.py will present an interface that allows a user to read, add, or delete traffic accident/volume data (see csv_files folder for format), as well as to read records in batches, sort in descending order, plot yearly values, and generate maps. MongoDB is used to store records. Ensure that you set MONGO_USERNAME and MONGO_PASSWORD environment variables (in a .env file for example) to produce a valid connection string.

## Demonstration

![GUI](First%20Phase/samples/demonstration_1.gif)

Example Traffic Volume Map:

![Traffic Volume Map](First%20Phase/samples/demonstration_3.gif)

Example Traffic Incidents Map:

![Traffic Incidents Map](First%20Phase/samples/demonstration_2.gif)

## Second Phase

See the Interactive_Grid_Map_and_Data_Analysis.ipynb file for results (https://nbviewer.org/github/hasnil/traffic-analysis/blob/main/Second%20Phase/Interactive_Grid_Map_and_Data_Analysis.ipynb). An interactive grid map of the City of Calgary is created. Each grid area can be clicked to display pertinent statistics. A speed limit map is presented. Hovering over (major) streets will display information. Traffic volume heatmaps and data analysis for the collected traffic information are also included.

![Grid Map](Second%20Phase/demonstration_4.png)

![Speed Limits Map](Second%20Phase/demonstration_5.png)
