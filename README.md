This README will provide an introduction to the project (Introduction section), take you
through the process of downloading the project (Downloading section), setting it up on
your computer so that you can run it locally (Setup section), and a brief run through
of what the project does in more detail (Project Overview section).

# Introduction

This project collects and analyzes data from Major League Baseball (MLB) games, using the
Python programming language. Please refer to the Baseball Wikipedia page
(https://en.wikipedia.org/wiki/Baseball) for a full explanation of the game, and the 
BaseballREADME.md for specific terms and concepts that will be necessary to understand the
project.

This project was inspired by the desire to have a quantitative measurement of a concept in
Baseball called bullpen management. Essentially, how well does a manager use their pitchers to
minimize the number of runs the opposing team scores? To accomplish this, it compares teams on
the metric of blown leads.

## Blown Leads

The most obvious indication of failed bullpen management is blown leads. A lead is blown when
one team has more runs than the other, and then surrenders that lead. The idea being that
managers who are effective at managing their bullpen will be better at substituting pitchers,
and therefore have fewer blown leads.

For the purposes of this project, a blown lead is defined as any time a team surrenders a lead
of three or more runs. A three run delta was chosen to isolate the analysis to events of gross
mismanagement.

## St. Louis Cardinals
This project collects general blown lead statistics for all MLB teams, but focuses in particular
on the St. Louis Cardinals. The Cardinals' manager had a reputation for being bad at bullpen
management. Therefore the Cardinals are used as a control point to assess whether or not this
reputation is fairly earned, or alternatively, if these basic metrics are able to capture what
our eyes see.

# Downloading

Download the repository from github onto your machine using the command:
git clone https://github.com/dccodesample/baseball_project.git

# Setup

Using Python 3.6 or your latest version of Python3, create a virtual environment in the project
folder using the command, python -m venv venv.

Install the required dependencies in the requirements.txt file using the command, pip install -r
requirements.txt. (Note: make sure to activate your virtual environment before this step).


# Project Overview

This project has two main steps, and several sub-steps within each of those steps.

1) Collect data on MLB games (i.e., box score data) from a website called Baseball Reference.
    Note: Baseball Reference has box score data, but it does not make it available for
    download via an API or other means. Instead, every box score is stored on its own web
    page, from which we can web scrape the data and store it. To accomplish this, there are
    three sub-steps.

    A) Find the Baseball Reference Season Home Page. This web page contains a "season table"
    in it, where every row (apart from break rows) represents a game the team played that
    season.

    B) Web scrape the urls from the "season table", so we can now access the box score web
    page for every game the team played that season. 

    C) Web scrape each box score web page, for every game a team played, for every team in
    MLB, for every season in the study (2012-2018), and store the data in a data file.

2) Analyze the data.

    A) Read the data from the data file.

    B) Convert each box score in the data file to a "Box Score Object". This object, defined
    in BoxScore.py, is a class that contains instance variables to hold the box score data,
    as well as other information necessary to analyze the data (e.g., the number of leads
    the team blew that game).

    C) Store each "Box Score Object" as a row in a Pandas data frame.

    D) Analyze the data and output the analysis in the form of charts and a results.txt file.

Both of these steps have already been completed, and the results are available for you to look
at. The datafile is located at data/box_score_data.json, and the charts and results.txt file are
located in the results folder.

You can also run the code yourself, in which case there are two entry points to the project:
box_score_data_analysis.py and box_score_data_collection.py, located in the src file.
box_score_data_collection.py should be run first as it handles the data collection process, and box_score_data_analysis.py should
be run second as it analyzes the collected data. The data collection process is very time
intensive, taking approximately 30 minutes for every year included in the project. To avoid this,
you can reduce the number of years in the study, using the years variable in
box_score_data_collection.py. It is also recommended that you only run the data collection step
once. If you only want to run the data analysis step, simply run the box_score_data_analysis.py
file.
