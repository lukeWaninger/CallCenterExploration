### Luke Waninger

### 1. Create a model to gain insight into issues resolved by 'user education'.
The dataset was relatively clean with only minor issues regarding the response variable, Issue Resolution. Several of the predictor features had missing values but were able to be either imputed or eliminated. My modeling approach for this problem started with defining the response variable. The research question at hand was to gain insights into issues resolved by user education. As such, I created a binary response variable, edu that I used throughout the notebook. I first cleaned and imputed missing values, checked for outliers, binned several features, and created several features. 

Several visualizations were made to aid our understanding of the predictors, response, and how they interact. The final logistic regression model was used to gain an understanding of which features have the most impact.  

### 2. Business insights and recommendations for the leadership team.
Several insights can be made from the exploration and insights notebook. 
1. The United States generates the most tickets while their proportion of closed through user education is statistically below the world mean proportion. There are several other countries that have much higher the mean proportions. The leadership team could compare the business processes of these highly contrasting locations to gain a deeper understanding.

2. Tenure and career show an increasing relationship with the response. As tenure or maturity level increase, so does the tickets probability towards successful resolution (user education). The vast majority of tickets are being submitted by employees with low tenure and aren't being resolved successfully. This is a difficult problem to approach from a business standpoint. I would suggest gathering more data on these issues and create a training program targeting the most common problems.

3. The most significant features that indicate success are the category, building and career (ic2). These are somewhat expected. If you call in about an application issue, most likely the user doesn't fully understand that application. This is reflected in cross-tabulation presented below. On the other hand, people who submit multiple tickets or work in an office are much less likely to be resolved successfully. A count of tickets submitted by the person was by far the largest indicator of success or failure. My recommendation for the leadership team is to push users to perform software updates more frequently. I think this is the lowest hanging fruit. Over 600 tickets were resolved by simple updates, all of which could have been precluded.  

### 3. Roadmap for improved results.
Several improvements can be made.
1. Better model selection. For this report, I trained highly interpretable models. Even the final logistic regression model was showing poor performance. It did, however, give valuable insight into the predictor variables. If predicting the response becomes the priority, we should switch to models that can more acutely tune to the target function.

2. Feature engineering. There is much more room for improvement here. Particularly, the position category. It would be useful to map these positions, careers, and divisions into their domain structure (most likely a graph) and use kernel based methods to find patterns. It would be useful for the leadership team to identify and prioritize different areas of the business.

3. Time series data. Ticket behavior can be better understood and interesting features could be generated if timestamps came along with the tickets.