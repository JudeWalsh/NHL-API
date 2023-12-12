# NHL-API
Wrapper for new NHL API

# Predictive Claims Scoring

## Get Started

Clone this repository into your local machine.

Locate in your terminal or open in an IDE to access

# Run the application

## Create a Virtual Environment

In your terminal type the following command
```
python -m venv venv
```

Our interpreter uses python 3.9.16

## Activate Virtual Environment
For windows run the following command
```
venv\Scripts\activate
```

For Mac:
```
source venv/bin/activate
```

## Install necessary libraries
```
pip install -r requirements.txt
```

## Deactivate virtual environment
```
deactivate
```

## Freeze libraries
If you decide to install new libraries, 
run the following command

```
pip freeze > requirements.txt
```

# Concept
The purpose of this wrapper is to be able to easily access 
any of the information on the front page of the NHL website

The types of reports are the following:
Summary
Bio Info
Faceoff percentages
Faceoff Wins and losses
Goals For and Against
Miscellaneous
Penalties
Penalty Kill
Penalty Shots
Power Play
Puck possession
SAT Counts
SAT Percentages
Scoring per 60
Scoring per game
Shootout
Shots by type
Time on Ice

## Summary

## Bio Info

To access player Bio Information

use the function ```playerBio(playerID)```

to return the players height in inches, weight in pounds and current age
in the form of a dict