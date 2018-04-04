import numpy as np
import pandas as pd
import random

def prep(train,test):
	#把Id作为index
	train.index = train['Id']
	train = train.drop('Id',axis=1)
	train = train.drop('MasVnrArea',axis=1)
	#暂时把相关系数不好的属性删除：

    #如何处理MSZoning属性，序列化？
	for i in range(len(pd.value_counts(train['MSZoning']))):
		train.loc[train['MSZoning']==pd.value_counts(train['MSZoning']).index[i],'MSZoning'] = i+1    
    #$LotFrontage属性需要先补齐，补齐之后再调整数据的规模。
	lot_index = train[pd.isna(train['LotFrontage'])].index
	for n in lot_index:
		train.loc[n,'LotFrontage'] = random.randint(21,150)

    #$LotArea，房屋的面积，可能需要调整规模(比如归一化)
    #相关性并不好,0.264,待定

    #Street,1454个pave，所以删掉.
	train = train.drop('Street',axis=1)
	#Alley属性缺失太多，先删掉。
	train = train.drop('Alley',axis=1)

	#LotShape序列化
	for i in range(len(pd.value_counts(train['LotShape']))):
		train.loc[train['LotShape']==pd.value_counts(train['LotShape']).index[i],'LotShape'] = i+1

    #LandContour变化太小，删掉
	train = train.drop('LandContour',axis=1)

    #Utilities,同上
	train = train.drop('Utilities',axis=1)
 	
 	#LotConfig ,先删除
	train = train.drop('LotConfig',axis=1)

 	#LandSlope，删除。
	train = train.drop('LandSlope',axis=1)

 	#Neighborhood
	for i in range(len(pd.value_counts(train['Neighborhood']))):
		train.loc[train['Neighborhood']==pd.value_counts(train['Neighborhood']).index[i],'Neighborhood'] = i+1

    #Condition1,待定,是否要跟condition2做一个结合？   
	train = train.drop(['Condition1','Condition2'],axis=1)

 	#户型
	for i in range(len(pd.value_counts(train['BldgType']))):
		train.loc[train['BldgType']==pd.value_counts(train['BldgType']).index[i],'BldgType'] = i+1

    #装修风格
	for i in range(len(pd.value_counts(train['HouseStyle']))):
		train.loc[train['HouseStyle']==pd.value_counts(train['HouseStyle']).index[i],'HouseStyle'] = i+1

    #YearBuilt,竣工日期，针对年份应该怎么处理？

    #YearRaemodAdd,翻新日期，若与竣工日期相同，则未翻新。

    #RoofStyle,屋顶的风格
	for i in range(len(pd.value_counts(train['RoofStyle']))):
		train.loc[train['RoofStyle']==pd.value_counts(train['RoofStyle']).index[i],'RoofStyle'] = i+1

    #RoofMatl,删除
	train = train.drop('RoofMatl',axis=1)

    #Exterior1st,不一定,Exterior2st和之前不一样的部分算新组合。
	train = train.drop(['Exterior1st','Exterior2nd'],axis=1)
    #砖的种类,有8个缺失值
	for i in range(len(pd.value_counts(train['MasVnrType']))):
		train.loc[train['MasVnrType']==pd.value_counts(train['MasVnrType']).index[i],'MasVnrType'] = i+1
	train.loc[pd.isna(train['MasVnrType']),'MasVnrType'] = 1

    #ExterQual,外层材料的质量
	for i in range(len(pd.value_counts(train['ExterQual']))):
		train.loc[train['ExterQual']==pd.value_counts(train['ExterQual']).index[i],'ExterQual'] = i+1
    
    #ExterCond,外层材料的状况
	for i in range(len(pd.value_counts(train['ExterCond']))):
		train.loc[train['ExterCond']==pd.value_counts(train['ExterCond']).index[i],'ExterCond'] = i+1
    
    #Foundation
	for i in range(len(pd.value_counts(train['Foundation']))):
		train.loc[train['Foundation']==pd.value_counts(train['Foundation']).index[i],'Foundation'] = i+1
    
    #BsmtQual
	for i in range(len(pd.value_counts(train['BsmtQual']))):
		train.loc[train['BsmtQual']==pd.value_counts(train['BsmtQual']).index[i],'BsmtQual'] = i+1
	train.loc[pd.isna(train['BsmtQual']),'BsmtQual'] = 0

    #BsmtCond,1311个Ta，故删除
	train = train.drop('BsmtCond',axis=1)

    #BsmtExposure
	for i in range(len(pd.value_counts(train['BsmtExposure']))):
		train.loc[train['BsmtExposure']==pd.value_counts(train['BsmtExposure']).index[i],'BsmtExposure'] = i+1
	train.loc[pd.isna(train.BsmtExposure),'BsmtExposure'] = 0

    #BsmtFinType1,BsmtFinSF1,BsmtFinType2,BsmtFinSF2,先放一放
	index = ['GLQ','ALQ','BLQ','Rec','LwQ','Unf'][::-1]
	j = 5
	for i in range(len(index)):
		train.loc[train['BsmtFinType1']==index[i],'BsmtFinType1'] = i+1
	train.loc[pd.isna(train['BsmtFinType1']),'BsmtFinType1'] = 0
	train['BsmtFin1'] = train['BsmtFinType1'] * train['BsmtFinSF1']
	train = train.drop(['BsmtFinType2','BsmtFinSF2'],axis=1)

    #BsmtUnfSF,相关系数有点小，而且跟上面有点重复。不过是线性相关的。TotalBsmtSF,属性很棒,最大规模在几千。
	train = train.drop(['BsmtUnfSF','Heating','CentralAir'],axis=1)

    #HeatingQC还可以，序列化
	for i in range(len(pd.value_counts(train['HeatingQC']))):
		train.loc[train['HeatingQC']==pd.value_counts(train['HeatingQC']).index[i],'HeatingQC'] = i+1

    #Electrical,不大行，先删除
	train = train.drop('Electrical',axis=1)

    #LowQualFinSF,0太多，删除
	train = train.drop('LowQualFinSF',axis=1)

    #1stFlrSF,2ndFlrSF,GrLivArea,相关性不错,规模为几百上千。

    #BsmtFullBath还行，相关系数为0.227

    #BsmtHalfBath删除
	train = train.drop('BsmtHalfBath',axis=1)


    #KitchenQual,先序列化,相关系数0.46
	for i in range(len(pd.value_counts(train['KitchenQual']))):
		train.loc[train['KitchenQual']==pd.value_counts(train['KitchenQual']).index[i],'KitchenQual'] = i+1

    #TotRmsAbvGrd,0.533相关系数，凑合

    #Functional,相关系差，删除
	train = train.drop('Functional',axis=1)

    #Fireplaces,还行,0.467相关

    #FireplaceQu,序列化之后有0.335的相关性,先留着
	for i in range(len(pd.value_counts(train['FireplaceQu']))):
		train.loc[train['FireplaceQu']==pd.value_counts(train['FireplaceQu']).index[i],'FireplaceQu'] = i+1
	train.loc[pd.isna(train['FireplaceQu']),'FireplaceQu'] = 0

    #GarageType,删除
	train = train.drop('GarageType',axis=1)

	#GarageYrBlt,有缺失，而且不知道怎么对年份进行处理(如何补齐？？？？)
	#用随机的方法补齐
	yr_index = train[pd.isna(train['GarageYrBlt'])].index
	for x in yr_index:
		train.loc[x,'GarageYrBlt'] = random.randint(1900,2010)

	#GarageFinish,序列化再补齐缺失值
	for i in range(len(pd.value_counts(train['GarageFinish']))):
		train.loc[train['GarageFinish']==pd.value_counts(train['GarageFinish']).index[i],'GarageFinish'] = i+1
	train.loc[pd.isna(train['GarageFinish']),'GarageFinish'] = 0

	#GarageCars,没毛病

	#GarageArea,同样可以

	#GarageQual,GarageCond,PavedDrive删
	train = train.drop(['GarageQual','GarageCond','PavedDrive'],axis=1)

	#木地板面积的相关系数只有0.324

	#OpenPorchSF也只有0.3158,随时删

	#EnclosedPorch,3SsnPorch,ScrennPorch,PoolArea,PoolQC,Fence,MiscFeature,MiscVal,MoSold,YrSold,SaleType不行，删除
	train = train.drop(['LotFrontage','EnclosedPorch','3SsnPorch','ScreenPorch','PoolArea','PoolQC','Fence','MiscFeature','MiscVal','MoSold','YrSold','SaleType','SaleCondition'],axis=1)

	#相关系数不好的删掉
	train = train.drop(['1stFlrSF','2ndFlrSF','Fireplaces','TotRmsAbvGrd','GarageArea','BsmtFin1','BsmtFinType1','BsmtFinSF1','BsmtFullBath','MSSubClass','MSZoning','Neighborhood','BldgType','HouseStyle','OverallCond','RoofStyle','ExterCond','BedroomAbvGr','KitchenAbvGr'],axis=1)
	#以下处理test数据集也要用
	train['SalePrice'] = np.log(train['SalePrice'])
	train['GrLivArea'] = np.log(train['GrLivArea'])
	train.loc[train['TotalBsmtSF']==0,'TotalBsmtSF'] = 1
	train.loc[pd.isna(train.TotalBsmtSF),'TotalBsmtSF'] = 1
	train['TotalBsmtSF'] = np.log(train.TotalBsmtSF)
	train['LotFrontage'] = np.log(train['LotFrontage'])
	train['LotArea'] = np.log(train['LotArea'])
	train.loc[train['MasVnrArea']==0,'MasVnrArea'] = 1
	train['MasVnrArea'] = np.log(train['MasVnrArea'])
	train.loc[train['WoodDeckSF']==0,'WoodDeckSF'] = 1
	train['WoodDeckSF'] = np.log(train['WoodDeckSF'])
	train.loc[train['OpenPorchSF']==0,'OpenPorchSF'] = 1
	train['OpenPorchSF'] = np.log(train['OpenPorchSF'])

	#对YearBuilt,进行分段,1938以下为1,1938-1985为2,1985以上为3
	train.loc[train.YearBuilt<=1938,'YearBuilt'] = 1
	train.loc[(train.YearBuilt>1938)&(train.YearBuilt<=1985),'YearBuilt'] = 2
	train.loc[train.YearBuilt>1985,'YearBuilt'] = 3

	#对YearRemodAdd,进行分段,1961以下为1,1961-1982为2,1984以上为3
	train.loc[train.YearRemodAdd<=1961,'YearRemodAdd'] = 1
	train.loc[(train.YearRemodAdd>1961)&(train.YearRemodAdd<=1982),'YearRemodAdd'] = 2
	train.loc[train.YearRemodAdd>1982,'YearRemodAdd'] = 3

	#对GarageYrBlt,进行分段,1931以下为1,1931-1983为2,1983以上为3
	train.loc[train.GarageYrBlt<=1931,'GarageYrBlt'] = 1
	train.loc[(train.GarageYrBlt>1931)&(train.GarageYrBlt<=1983),'GarageYrBlt'] = 2
	train.loc[train.GarageYrBlt>1983,'GarageYrBlt'] = 3


	#################test处理
	test.index = test['Id']
	test = test.drop(['2ndFlrSF','Id','MasVnrArea','LotFrontage'],axis=1)
	test.loc[test['GrLivArea']==0,'GrLivArea'] = 1
	test['GrLivArea'] = np.log(test['GrLivArea'])
	test.loc[test['TotalBsmtSF']==0,'TotalBsmtSF'] = 1
	test.loc[pd.isna(test.TotalBsmtSF),'TotalBsmtSF'] = 1
	test['TotalBsmtSF'] = np.log(test.TotalBsmtSF)
	test.loc[test['LotFrontage']==0,'LotFrontage'] = 1
	test['LotFrontage'] = np.log(test['LotFrontage'])
	test.loc[test['LotArea']==0,'LotArea'] = 1
	test['LotArea'] = np.log(test['LotArea'])
	test.loc[test['WoodDeckSF']==0,'WoodDeckSF'] = 1
	test['WoodDeckSF'] = np.log(test['WoodDeckSF'])
	test.loc[test['OpenPorchSF']==0,'OpenPorchSF'] = 1
	test['OpenPorchSF'] = np.log(test['OpenPorchSF'])

	#对YearBuilt,进行分段,1938以下为1,1938-1985为2,1985以上为3
	test.loc[test.YearBuilt<=1938,'YearBuilt'] = 1
	test.loc[(test.YearBuilt>1938)&(test.YearBuilt<=1985),'YearBuilt'] = 2
	test.loc[test.YearBuilt>1985,'YearBuilt'] = 3

	#对YearRemodAdd,进行分段,1961以下为1,1961-1982为2,1984以上为3
	test.loc[test.YearRemodAdd<=1961,'YearRemodAdd'] = 1
	test.loc[(test.YearRemodAdd>1961)&(test.YearRemodAdd<=1982),'YearRemodAdd'] = 2
	test.loc[test.YearRemodAdd>1982,'YearRemodAdd'] = 3

	#对GarageYrBlt,进行分段,1931以下为1,1931-1983为2,1983以上为3
	test.loc[test.GarageYrBlt<=1931,'GarageYrBlt'] = 1
	test.loc[(test.GarageYrBlt>1931)&(test.GarageYrBlt<=1983),'GarageYrBlt'] = 2
	test.loc[test.GarageYrBlt>1983,'GarageYrBlt'] = 3

	train = train.drop([523,1298])



	return train,test
