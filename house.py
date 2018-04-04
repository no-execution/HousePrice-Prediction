import numpy as np
import pandas as pd

from sklearn.model_selection import KFold,cross_val_score,train_test_split
from sklearn.linear_model import RandomForestRegressor,GradientBoostingRegressor
from sklearn.kernel_ridge import Kernel_ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessor import RobustScaler
from sklearn.base import BaseEstimator,TransformerMixin,RegressorMixin,clone
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import lightgbm as lgb



def df_res(test,res):
	s = pd.DataFrame({'Id':test.index,'SalePrice':res.astype(np.float64)})
	s['SalePrice'] = np.exp(s['SalePrice'])
	return s

def cv(train,model):
	test_set = KFold(n_splits=5,shuffle=True,random_state=5)
	score = cross_val_score(model,np.mat(train.drop('SalePrice',axis=1)),np.array(train.SalePrice),scoring="neg_mean_squared_error",cv=test_set)
	print('Score is :',np.sqrt(-score).mean(),np.sqrt(-score).std())

def models(train):
