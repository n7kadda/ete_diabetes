from scipy.stats import randint, uniform

# Expanded hyperparameter search space for LightGBM
LIGHTGM_PARAMS = {
    'n_estimators': randint(100, 1000),
    'num_leaves': randint(20, 60),
    'max_depth': [-1, 10, 20, 30],
    'learning_rate': uniform(0.01, 0.2),
    'colsample_bytree': uniform(0.6, 0.4), 
    'subsample': uniform(0.6, 0.4),
    'reg_alpha': uniform(0, 1), 
    'reg_lambda': uniform(0, 1) 
}

# Parameters for RandomizedSearchCV, with more iterations
RANDOM_SEARCH_PARAMS = {
    "n_iter": 50, 
    "cv": 5,
    "n_jobs": -1,
    "verbose": 1,
    "random_state": 42,
    "scoring": "f1" 
}
