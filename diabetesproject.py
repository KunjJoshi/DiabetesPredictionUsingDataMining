# -*- coding: utf-8 -*-
"""DiabetesProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rFyXj-kq862xwKLvPOCwCXQ0Ye-Lc6CW

***Importing All The Useful Libraries***
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import seaborn as srn
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from six import StringIO
from IPython.display import Image
import pydotplus
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
import plotly.graph_objects as go
from sklearn import svm

"""Using Pandas Library to read the CSV File. We have used 4 functions of the dataframe object:

1) Head Function: Shows the first 5 object values of the dataframe

2) Tail Function: Shows the last 5 object values of the dataframe

3) Describe Function: To give different statistics of the numerical data

4) Dtypes function: To show the datatype of different columns of the dataframe
"""

df=pd.read_csv("Diabetestype.csv")
df.head()

df.tail()

df.describe()

df.dtypes

"""***Preprocessing Stage***

***First Step:***

Our data is dirty because both Type 1 and Type 2 diabetes are represented as 1 in the column Class. So we will differentiate between them by representing Type 1 diabetes as 1 and Type 2 diabetes as 2
"""

diatypes=df['Type']
dianum=df['Class']
diatypes
dianum

for i in range(len(diatypes)):
  if(diatypes[i]=="Normal"):
    dianum[i]=0
  else:
    if(diatypes[i]=="Type1"):
      dianum[i]=1
    else:
      dianum[i]=2
dianum

df['Class']=dianum
df

"""***Second Step***:

As we can see from data description that BS pp and Plasma F columns have some values missing. We will use Mean to predict the missing values. 
"""

dfcopy=df
dfcopy['BS pp'].fillna(df['BS pp'].mean(),inplace=True)

dfcopy['Plasma F'].fillna(dfcopy['Plasma F'].mean(),inplace=True)

df=dfcopy
df

pd.set_option('max_rows',16)
df

"""***Third Step:***

We will drop the column of Type because we already have a Class Column showing the same information as Type column. So we will save the Type column in another list for future reference before dropping it
"""

Typelist=df['Type']
df=df.drop('Type',axis=1)

Typelist

df

"""Here the complete prerpocessing of the data ends.

***Sorting Values by Age***
"""

df.sort_values(by='Age',inplace=True)
df

"""***Graph Plotting Stage***

We will plot various graphs between different features of the dataset to see the figure of dataset and do a human-based analysis on which kind of models will be used to perfction on the dataset.

***Line Graph*** :
"""

#age and bspp
agearr=df['Age']
BSpparr=df['BS pp']
plt.plot(agearr,BSpparr)
plt.xlabel('Age')
plt.ylabel('BS pp')
plt.show()

#age and plasma f
pfarr=df['Plasma F']
plt.plot(agearr,pfarr)
plt.xlabel('Age')
plt.ylabel('Plasma F')
plt.show

"""The two line graphs show we dont have direct dependence on Age Factor"""

#bs pp and bs fast
bsfastarr=df['BS Fast']
bsfastarr=bsfastarr.sort_values()
plt.plot(bsfastarr,BSpparr)
plt.xlabel('BS Fast')
plt.ylabel('BS PP')
plt.show()

#plasma r and plasma f
prarr=df['Plasma R']
prarr=prarr.sort_values()
plt.plot(prarr,pfarr)
plt.xlabel('Plasma R')
plt.ylabel('Plasma F')
plt.show()

#age and bsfas
plt.plot(agearr,bsfastarr)
plt.xlabel('Age')
plt.ylabel('BS Fast')
plt.show()

"""***Dot Graphs:***"""

age1=df['Age']
bspp1=df['BS pp']
plt.scatter(age1,bspp1)
plt.show()

bsf1=df['BS Fast']
plt.scatter(bsf1,bspp1)
plt.show()

prarr=df['Plasma R']
pfarr=df['Plasma F']
plt.scatter(prarr,pfarr)

"""***Test and Split Step*** :"""

Xtrain,Xtest,Ytrain,Ytest=train_test_split(df[['Age','BS Fast','BS pp','Plasma R','Plasma F','HbA1c']],df['Class'],test_size=0.2)

len(Xtrain), len(Ytrain)

len(Xtest),len(Ytest)

"""***Now The different models for Classification Start***:

***1) Multinomial Logistic Regression:***
"""

regmnlr=LogisticRegression(multi_class='multinomial',solver='lbfgs')
regmnlr.fit(Xtrain,Ytrain)

regmnlr.predict(Xtest)

regmnlr.score(Xtest,Ytest)

"""Multinomial Logistic Regression is one of the easiest Classification methods where we use modifications in the Logit function to classify for multi classes rather than binary classes. Here we acquired 94% Accuracy with 80% training data. 

The lbfgs Solver is a limited memory solver. As a result it doesnt support one vs one kind of multinomial logistic regression. We have done one vs all multinomial logistic regression. 

How does it work:
The model first does a normal binary logistic classification on the data dividing it into  two parts such that values with Class=0 go on one side and values with Class=1,2 go on the other side. After that we will do binary Logistic Regression on the mixed set and values having Class=1 will be classified differently from those having Class=2

***2) Decision Tree Classifier (Gini Index)*** :
"""

dtcgini= DecisionTreeClassifier()
dtcgini.fit(Xtrain,Ytrain)

dtcgini.predict(Xtest)

dtcgini.score(Xtest,Ytest)

dot_data = StringIO()
export_graphviz(dtcgini, out_file=dot_data,  
                filled=True, special_characters=True,class_names=['0','1','2'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('diabetes.png')
Image(graph.create_png())

fimp=pd.Series(dtcgini.feature_importances_,index=Xtrain.columns).sort_values(ascending=False)
fimp

srn.barplot(x=fimp,y=fimp.index)
plt.xlabel("Feature Importance")
plt.ylabel("Features")
plt.show()

"""Decision Tree Classifier acts as one of the more classic accurate algorithms for classifying multiclass data. Here we have used gini function (which uses probability square rather than log function) and we arrive at a 97.5% accuracy with 80% training data. 

Gini Function :      

![8_k4ia8r.png](data:image/png;base64,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)

Here :     

D is a tuple

pi is the probability of D belonging to the class Ci

m is the total number of classes

How it works: We use an Attribute Selection Method and choose the best attribute (here gini index). Make the attribute into decision node and break dataset into smaller subset as we go down the tree, the nodes go on purifying. The leaf nodes represent pure classes. The branches represent splitting decisions.

Here we can see how some of the features dont give significant input to the classification and hence as a result, Decision Tree Classifier using Gini Index cannot be called as the most reliable source of classification

***3) Decision Tree Classifier (Information gain)***:
"""

dtcig=DecisionTreeClassifier(criterion='entropy')
dtcig.fit(Xtrain,Ytrain)

dtcig.predict(Xtest)

dtcig.score(Xtest,Ytest)

dot_dataen = StringIO()
export_graphviz(dtcig, out_file=dot_dataen,  
                filled=True, special_characters=True,class_names=['0','1','2'])
graphen = pydotplus.graph_from_dot_data(dot_dataen.getvalue())  
graphen.write_png('diabetes.png')
Image(graphen.create_png())

fimp=pd.Series(dtcig.feature_importances_,index=Xtrain.columns).sort_values(ascending=False)
fimp

srn.barplot(x=fimp,y=fimp.index)
plt.xlabel("Feature Importance")
plt.ylabel("Features")
plt.show()

"""Information Gain or Entropy is another way of using Decision Tree Classifier. Just as we used GINI index in the earlier model to choose the most accurate data splitting criterion, here Information Gain does the work and as we can see it has provided us with 100% result in 80% training data. 

Formula for Entropy:     
![3_tvqfga.png](data:image/png;base64,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)

Here D is the tuple

Pi is the probability of D belonging to class Ci 

m is the total number of classes. 

Features such as Age, Plasma F and HbA1c give no input to prediction of classes of each data value. This makes Decision Tree using Information Gain highly unreliable and an algorithm that does not use all of the features given to it. Hence we cannot trust completely on the results predicted by Decision Tree using Information Gain

***4) Random Forest Classification*** :
"""

clfrf=RandomForestClassifier(n_estimators=200)
clfrf.fit(Xtrain,Ytrain)

clfrf.predict(Xtest)

clfrf.score(Xtest,Ytest)

estimator = clfrf.estimators_[5]
export_graphviz(estimator, out_file='tree.dot', 
                class_names = ['0','1','2'], proportion = False, 
                precision = 2, filled = True)
from subprocess import call
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])
Image(filename = 'tree.png')

fimp=pd.Series(clfrf.feature_importances_,index=Xtrain.columns).sort_values(ascending=False)
fimp

srn.barplot(x=fimp,y=fimp.index)
plt.xlabel("Feature Importance")
plt.ylabel("Features")
plt.show()

"""Random Forest is an Aggregation of many Decision Trees fromed from the subsets of the dataset provided to the algorithm as input. Decision Trees become highly ineeficient due to not using the data provided perfectly while depending on only certain features for prediction. Random Forest divides the dataset into different sub-datasets (also called Bootstrapped Datasets, in our case 200 bootstrapped datasets) and randomly selects a subset from feature set. Each bootstrapped dataset and feaure subset have equal number of instances and features respectively. We can see Random Forest as usually more accurate algorithm to Decision Tree as it is less sensitive to training data. We get almost 100% or 99.5% accuracy with 80% training dataset

How it Works:    
Our dataset is divided into sub-datasets each having equal number of instances and each of them is worked upon with some feature subset. Each feature subset also has equal number of features which is usually equal to square root of total number of features. Each bootstrapped dataset is made into decision tree and all the final decision trees are aggregated to form one huge forest (or one huge decision tree).

***5) Naive Bayes Algorithm*** :
"""

modelnb=GaussianNB()
modelnb.fit(Xtrain,Ytrain)

pred=modelnb.predict(Xtest)
pred

modelnb.score(Xtest,Ytest)

mat = confusion_matrix(pred, Ytest)
names = np.unique(pred)
srn.heatmap(mat, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=names, yticklabels=names)
plt.xlabel('Truth')
plt.ylabel('Predicted')

"""The Naive Bayes algorithm works highly on conditional probability of the given feature in dataset. 
The Naive Bayes Algorithm:     
![image_3_ijznzs.png](data:image/png;base64,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)

It fails on our classification dataset because our given values arent continous but each of the factor provides individual importance to prediction of Diabetes type. Hence calculation of individual probability to calculate the class of a given instance will be highly ineffecient by the NB Standards. It gives us 94% accuracy with 80% training set. 

How it works:      

The algorithm will first calculate prior probability for each class (i.e. probability of each class). Then it will calculate the conditional probability of each feature with an assumption of its presence in each class. In case of Gaussian Naive Bayes algorithm, this is done by calculating mean and standard deviation and by plotting the Gaussian curve. For every new instance of datavalue to be predicted into class, each of the probabilities are predicted using The Gaussian curve and the probabilities are then multiplied. To discard the presence of very small probabilities we use logarithms on each of the probability. The higher aggregate conditional probability for a class will determine the data instance to be present in a class or not. 

For eg. if the Aggregate Conditonal Probability for a value for Class 0 is -114.56, for class 1 is -110.65 and for class 2 is -98.67, then the data instance belongs to class 2.

***6) K Nearest Neigbours Classififcation with N neighbours as 5 :***
"""

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(Xtrain,Ytrain)

predicted=knn.predict(Xtest)
predicted

knn.score(Xtest,Ytest)

mat = confusion_matrix(predicted, Ytest)
names = np.unique(pred)
srn.heatmap(mat, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=names, yticklabels=names)
plt.xlabel('Truth')
plt.ylabel('Predicted')

"""***7) Support Vector Machine:***"""

mac=svm.SVC(kernel='linear')
mac.fit(Xtrain,Ytrain)

macpr=mac.predict(Xtest)
macpr

mac.score(Xtest,Ytest)

pd.Series(abs(mac.coef_[0]), index=Xtrain.columns).nlargest(10).plot(kind='barh')

mat = confusion_matrix(macpr, Ytest)
names = np.unique(macpr)
srn.heatmap(mat, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=names, yticklabels=names)
plt.xlabel('Truth')
plt.ylabel('Predicted')

df

"""***Plotting a Bar Graph showing performance of each and every Algorithm so it is easy for analysis***"""

scores=np.array([regmnlr.score(Xtest,Ytest),dtcgini.score(Xtest,Ytest),dtcig.score(Xtest,Ytest),clfrf.score(Xtest,Ytest),modelnb.score(Xtest,Ytest),knn.score(Xtest,Ytest),mac.score(Xtest,Ytest)])
scores=100*scores
plotter= pd.Series(scores,index=['Multinomial Logistic Regression','Decision Tree (Gini)','Decision Tree(Info Gain)','Random Forest','Naive Bayes','K Nearest Neighbors','Support vector Machine'])
plotter

srn.barplot(x=plotter,y=plotter.index)
plt.title('Algorithm Performance Graph')
plt.xlabel('performance of Algorithm')
plt.ylabel('Algorithm name')
plt.show()

frzme=df[['Class']]
count=0
dfcop=df.drop(frzme,axis=1)
predvals=mac.predict(dfcop)
n=len(dfcop)
agearr=dfcop['Age']
for i in range(0,n):
  if(agearr[i]>20 and agearr[i]<=25):
    if(predvals[i]==1 or predvals[i]==2):
      count=count+1
perc=(count/n)*100
perc