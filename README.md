# CS506 Final Project

Predicting Flight Delays - 
By accurately forecasting the delay duration of a flight, the goal is to help airlines, airports, and passengers better manage their schedules and minimize the impact of disruptions on travel plans. 
This predictive model can be used to improve operational efficiency, optimize resource allocation, and enhance customer satisfaction by providing more reliable delay estimates.

Data Source: US Department of Transportation – Bureau of Transportation Statistics, August 2019 - August 2023

[Data Link](https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023)

Our outcome variable is ARR_DELAY, the difference in minutes between scheduled and actual arrival time.

## Midterm Report Video (5 minutes)
[Video Link](https://youtu.be/zwTngcYoQkM?feature=shared)


## Setup

- Clone or Download the Repository
- Once setup locally, in the terminal, type "make" or "make install" to install dependencies
- After dependencies are installed, in the terminal once more type "make run" to start the Flask server
- Once the server is running, navigate to the address provided in the terminal (e.g., http://127.0.0.1:3000) using your web browser.
- You can now interact with the site and its features, including visualizations and model training.
- ***NOTE**: it can take upwards of 2-3 minutes to train the model!* 

## Data Cleaning
Filtering by Largest Airports: Flights were filtered to include only those originating from and landing at the 30 largest U.S. airports by passenger traffic. This focus on major airports enhances the relevance of the analysis.

Removing Canceled Flights: All canceled flights were excluded from the dataset, as they cannot be modeled in a flight delay context.

Date Filtering: Flights from the year 2020 were excluded to avoid model bias and ensure a relevant dataset for analysis.

Extracting Flight Month and Day: New columns were created to represent the flight month and day numerically, derived from the flight date. These features will facilitate seasonal and weekend analysis. 

Extracting Route and Month Indicators: Historical data was used to generate a feature that represents the probability that the flight will be delayed or early for the respective month or route. These values ranged from -1 to 1 for the flight being likely to be early or delayed based on the specific route and month. 

Dropping Features: Irrelevant columns were removed to streamline the dataset and focus on key variables that contribute to understanding flight delays. Columns containing data that would allow the model to cheat were also dropped. 

Handling Missing Values: Any rows with missing data were eliminated to maintain the integrity of the dataset.


## Data Visualization

![image](https://github.com/user-attachments/assets/e99151c9-407e-487f-98a3-256b1396cd9b)

It can be seen from the data that there is a large portion of the data centered around 0 with a long tail going towards high delays. This could prove issues later on if the model tries to consistently predict a low delay and fail to predict high delays. 

![image](https://github.com/user-attachments/assets/213f3849-26e3-487a-8d1c-c1241c0f0bad)

It can be seen from the data that certain airlines could be a strong indicator that there will be a delay. 

![image](https://github.com/user-attachments/assets/5a1ba5b8-664f-4a04-9a62-0f7492f1a500)

It can be seen from the data that there are seasonal trends in delays, with a large spike of delays in the summer likely due to summer vacations causing high air traffic and therefore delays. 

## Modeling Process

Handling Categorical Variables: Categorical variables in the feature set were transformed using the CatBoost framework, which natively handles categorical features. The categorical columns (AIRLINE, ORIGIN, DEST) were explicitly marked and passed as categorical features during model training, eliminating the need for one-hot encoding.

Train-Test Split: 80% Train 20% Test was used to train the model. 

Model Initialization and Training: 
A CatBoost Regressor was initialized with the following parameters:
Iterations: 1000
Depth: 6
Learning Rate: 0.1
Loss Function: Tweedie with variance power = 1.5

### Model Predictions and Evaluation:

After training, the model made predictions on the test data. Evaluation metrics, specifically Mean Absolute Error (MSE) and R-squared (R²), were calculated to assess the model's performance. However, initial results indicated that the model struggled significantly with predicting higher arrival delays accurately. 
