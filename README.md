# CS506 Final Project Proposal

Predicting Flight Delays - 
By accurately forecasting the delay duration of a flight, the goal is to help airlines, airports, and passengers better manage their schedules and minimize the impact of disruptions on travel plans. 
This predictive model can be used to improve operational efficiency, optimize resource allocation, and enhance customer satisfaction by providing more reliable delay estimates.

Data Source: US Department of Transportation – Bureau of Transportation Statistics, August 2019 - August 2023
Data will be cleaned to remove flight cancellations since they can't be modelled in a flight delay model. 

Data will be modelled by fitting a linear regression. 

Our outcome variable is ARR_DELAY, the difference in minutes between scheduled and actual arrival time. 

The predictor variables include:
flight date, airline, origin and destination city, airtime, distance, and delays in minutes due to carrier, weather, national air system, security, and late aircraft

These variables will be visualized in scatter plots that best represent the relationship between the variables and the outcomes.

Testing will be done by using a model selection method and using a 70/15/15 test/train/validation that is randomly selected from the data. 
