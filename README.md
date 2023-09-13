# Volleyball Winning Team Prediction: Project Overview
* Created a model to predict the winning team of a PlusLiga (Polish Volleyball League) 2023 playoff match
* Used BeautifulSoup to scrape over 250 matches
  * A match is defined as a best of 5 between two teams here
* Constructed nonlinear features such as date and team name, as well as linear features like Rolling Avg Serve Efficiency % and Rolling Avg Score
  * Used match data scraped off the plusliga.pl website
* Optimized parameters of different models w/ GridSearchCV to reach a final best model that used XGBoost 
  * Tried XGboost, Logistic Regression, Support Vector Machine, Random Forest, and K Nearest Neighbors
# Dependencies
* Python 3.10
* BeautifulSoup 4.12.2
* Matplotlib 3.5.2 
* Pandas 1.4.3
* xgboost 1.7.6
* Seaborn 0.12.2
* Scikit learn 1.1.1
* Requests 2.31
# Web Scraping
From each match between two teams, I collected the following variables:
* Team 1 (the team on the left side of any match table on the website)
* Team 2 (the team on right side)
* Time (The date as well as the time that the game occurred)
* Points 1 (number of points Team 1 scored against Team 2 in all sets)
* Points 2 (number of points Team 2 scored against Team 1 in all sets)
* ServeEff 1 (Team 1's Serve efficiency percentage)
* ServeEff 2
* PosPercent 1 (Team 1's Receiving Positional Percentage)
* PosPercent 2
* KillPercent 1 (Team 1's kill percentage)
* KillPercent 2
* EffPercent 1 (Team 1's Efficiency percentage)
* EffPercent 2
* Score 1 (the number of sets that Team 1 won against Team 2 in the best of 5 match)
* Score 2 (number of sets that Team 2 won against Team 1 in the best of 5 match)
# Data Cleaning
To make the data easier to use, the following changes were applied on the raw data:
* Breaking up the score from one single cell per match into two separate scores, one for each team (as reflected in Score 1 and Score 2)
* Filtering out unnecessary text in score cell as well as all percentage cells
* Changing the time data into two different cells, or columns, one being the date the game occurred and the other being the time, expressed into an integer (e.g., 5:30 pm would be 17.5)
* Getting an integer value for the dates, so that data of, say, 4-7-2023 would become Friday, expressed as an integer (Monday being 0, so this integer value would be 4)
* Creating a unique ID for each Team 1. So that we would be working with an integer to represent Team 1
* Creating our target variable, Team1Dub, which took the value of 1 when Team 1 won and 0 when they lost.
# EDA
First, I created a box plot for scores and points. Out of my linear features, these were the only ones that weren't percentages. I wanted to make sure there weren't too many outliers so that I could then apply min max scaling.
![alt text](https://github.com/davidpaylan/Volleyball-Winning-Team-Prediction/blob/main/Boxplot%20Features.png?raw=true)
![alt text](https://github.com/davidpaylan/Volleyball-Winning-Team-Prediction/blob/main/Boxplot%20features%202.png?raw=true)
I decided to use a bar graph to see the correlation between each of the linear variables and the target variable Team1Dub.
![alt text](https://github.com/davidpaylan/Volleyball-Winning-Team-Prediction/blob/main/Lin%20vs%20Correlation.png?raw=true)
I also did this for the nonlinear variables. This showed me the importance of the nonlinear variables here, mainly the name of Team 1
![alt text](https://github.com/davidpaylan/Volleyball-Winning-Team-Prediction/blob/main/Nonlin%20vs%20correlation.png?raw=true)
# Model building and Model Performance
I split the train and test dataset by date. Since my goal was to predict whether Team 1 would win any given playoff match, the test set was all
the games after April 7, 2023, while the training set was all games before April 7, 2023 in the 2022/2023 season. The idea in this was that, if we were predicting
who would win a playoff game with only data from the "Essential Phase", or pre-playoffs, the data that the training set has access to should reflect that.

I used F1 score as the metric to optimize my models and determine which model I would use. I chose this because of the balance that f1 score gives between avoiding false positives and
avoiding false negatives (precision and recall respectively). And of course because it was easy to interpret, giving just one single value to optimize.

I tried 5 models: XGboost, KNN, Logistic Regression, SVM, and Random Forest. Logistic Regression and SVM were only fed the linear data, since they are not as versatile algorithms comparatively.
From Initial runs of the models, Random Forest and KNN gave the best results in terms of F1 score. But after optimizing each of them under grid search, I got the best result of 0.727 as my f1 score under the XGBoost model.

