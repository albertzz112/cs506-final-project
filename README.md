# CS506 Final Project Proposal

Predicting Flight Delays - 
By accurately forecasting the delay duration of a flight, the goal is to help airlines, airports, and passengers better manage their schedules and minimize the impact of disruptions on travel plans. 
This predictive model can be used to improve operational efficiency, optimize resource allocation, and enhance customer satisfaction by providing more reliable delay estimates.

Data Source: US Department of Transportation – Bureau of Transportation Statistics, August 2019 - August 2023

[https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023](url)

Our outcome variable is ARR_DELAY, the difference in minutes between scheduled and actual arrival time.

## Midterm Report Video (5 minutes)
[Video Link](https://youtu.be/zwTngcYoQkM?feature=shared)

## Data Cleaning
Filtering by Largest Airports: Flights were filtered to include only those originating from and landing at the 30 largest U.S. airports by passenger traffic. This focus on major airports enhances the relevance of the analysis.

Removing Canceled Flights: All canceled flights were excluded from the dataset, as they cannot be modeled in a flight delay context.

Eliminating Extreme Delays: Flights with an arrival delay greater than 180 minutes (3 hours) were removed to prevent skewing the results with extreme outliers.

Date Filtering: The flight date (FL_DATE) was converted to a datetime format, and flights from the years 2020, 2022, and 2023 were excluded to avoid model bias and ensure a relevant dataset for analysis.

Extracting Flight Month: A new column was created to represent the flight month numerically, derived from the flight date. This feature will facilitate seasonal analysis.

Security Delay Data Removal: Rows indicating delays due to security checks were filtered out unless the delay was recorded as zero or was missing. This step ensures that only relevant delays were analyzed.

Dropping Unnecessary Columns: Irrelevant columns were removed to streamline the dataset and focus on key variables that contribute to understanding flight delays.

Handling Missing Values: Any rows with missing data were eliminated to maintain the integrity of the dataset.


## Data Visualization

![image](https://github.com/user-attachments/assets/e99151c9-407e-487f-98a3-256b1396cd9b)

It can be seen from the data that there is a large portion of the data centered around 0 with a long tail going towards high delays. This could prove issues later on if the model tries to consistently predict a low delay and fail to predict high delays. 

![image](https://github.com/user-attachments/assets/213f3849-26e3-487a-8d1c-c1241c0f0bad)

It can be seen from the data that certain airlines could be a strong indicator that there will be a delay. 

![image](https://github.com/user-attachments/assets/5a1ba5b8-664f-4a04-9a62-0f7492f1a500)

It can be seen from the data that there are seasonal trends in delays, with a large spike of delays in the summer likely due to summer vacations causing high air traffic and therefore delays. 

## Modeling Process

Handeling Categorical Variables: Categorical variables in the feature set were transformed using one-hot encoding. This process converts categorical variables into a numerical format that the Random Forest model can interpret, allowing the model to learn from these variables effectively.

Train-Test Split: 80% Train 20% Test was used to train the model. 

Model Initialization and Training: A Random Forest Regressor was initialized with 100 estimators and trained on the training data. 

### Model Predictions and Evaluation:

After training, the model made predictions on the test data. Evaluation metrics, specifically Mean Absolute Error (MAE) and R-squared (R²), were calculated to assess the model's performance. However, initial results indicated that the model struggled significantly with predicting higher arrival delays accurately.


#### Insights and Model Refinement:
Upon analyzing the model's performance, it became apparent that it was particularly poor at predicting high arrival delays (≥ 50 minutes). This realization prompted the decision to segment the dataset based on arrival delay values. The process involved:

#### Data Subsetting:

The original DataFrame was divided into two subsets: one for flights with arrival delays less than 50 minutes (df_below_50) and another for those with delays of 50 minutes or more (df_above_50). This segmentation aimed to address the discrepancies in model performance across different delay magnitudes.
Separate Model Training:

A function was defined to train and evaluate a Random Forest model on each of the subsets independently. This approach allowed for tailored training to better capture the characteristics of each delay segment.
Evaluation of Segmented Models:

The model for arrival delays below 50 minutes was evaluated and yielded significantly better results than the initial model, indicating improved performance in predicting lower delays. Conversely, the performance for the high-delay segment was less favorable, reflecting the inherent challenges in accurately predicting more extreme delay scenarios.
