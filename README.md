Introduction

This code sample collects and analyzes data from Major League Baseball (MLB) games, using the
Python programming language. Please refer to the Baseball Wikipedia page
(https://en.wikipedia.org/wiki/Baseball) for a full explanation of the game, and the 
BaseballREADME.md for specific terms and concepts that will be necessary to understand the
sample.

The sample was inspired by the desire to have a simple measure of a concept in Baseball called
bullpen management. Essentially, how well does a manager use their pitchers to minimize the
number of runs the opposing team scores? To that end, it isolates one event in Baseball that
marks failed bullpen management, blown leads. A lead is blown when one team has more runs than
the other, and then surrenders that lead. The idea being that managers who are effective at
managing their bullpen will be better at substituting pitchers, and therefore have fewer blown
leads.

This README will take you through the process of downloading the code sample (Downloading
section), setting it up on your computer so that you can run it locally (Set Up section), and
a brief run through of what the project does in more detail (Overview of the Code Sample).

Downloading

Download the repository from github onto your machine using the command:
git clone https://github.com/dccodesample/baseball_project.git

Setup

Using Python 3.6 or your latest version of Python3, create a virtual environment in the
project folder:
python -m venv venv

Install the required dependencies in the requirements.txt file. (Note: make sure to activate
your virtual environment before this step).
pip install -r requirements.txt

Overview of the Code Sample

This code sample has two main steps, and several sub-steps within each of those steps.

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

You can also run the code yourself, in which case your primary entry point is main.py. It contains
two lines, one to collect data and one to analyze it. The data collection process is very time
intensive. To avoid this, you can reduce the number of years in the study, using the years
variable in data_collection.py. It is also recommended that you only run the data collection step
in main.py once. If you only want to run the data analysis step, simply comment out the data
collection line from main.py.

Note: For the purposes of this sample, I only analyzed instances where a team blew a lead of
three or more runs. I did this to isolate the analysis to events of gross mismanagement.