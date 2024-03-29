

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn import tree

csv_file_name = "1-12. framingham.csv"

df = pd.read_csv( csv_file_name )
df.head(5)

target_column_name = "TenYearCHD"

categorical_target_column = True
#categorical_target_column = False

#Find out number of rows and columns
print(f'Total Number of Rows : {df.shape[0]}')
print(f'Total Number of Columns : {df.shape[1]}')

if categorical_target_column :
  print( df[target_column_name].value_counts() )

"""OBSERVATION

---

There are total 4260 data points in this dataset . Among which 3596 data points belong to class "0" (No Risk of Ten Year in CHD) and other 644 data points belong to class "1" (At Ten Year CHD Risk) .
This indicates that in the dataset the data points are not equally distributed among the classes.
"""

df.isnull().sum().plot(kind='bar')
plt.title("Total Number of Null values for Each Column")

#Find out the percentages of null value cout for each column
#( df.isnull().sum()/len(df) ) *100
print(((df.isnull().sum() / len(df)) * 100).apply(lambda x: f"{x:.2f}%"))

"""OBSERVATION

---


Most of the data points from the column "glucose" are missing. As **9.15%** of the data points are missing , here glocuse is an important factor so we can't drop this column we can use some techniques to handle thos missing values.

The "education" Column has some missing values. Around 2.48% of the data are missing. The null values can be handeled by using different teachniques such as BackFill / FrontFill .

"BPMeds", "totChol", "cigsPerDay", "BMI", "heartRate", these columns are also have some missing values following 1.25%, 1.18%, 0.68%, 0.45%, 0.02%. Those null values also can be handled by using BackFIll or FrontFill.
"""

# If total number of missing value is less than 5% then drop it otherwise fill using backward fill/forward fill.

print(f'Maximum Null values in column (Before Handling)  : { df.isnull().sum().max() }')

if (df.isnull().sum().max() > len(df) ) * 0.05:
  print("\n------Dropped Null Values-------\n")
  df.dropna( inplace = True)
else:
  print("\n------Replaced Null Values-------\n")
  df.fillna( method = 'bfill' , inplace = True) # You can use 'ffill' to forward fill


print(f'Maximum Null values in column (After Handling)  : { df.isnull().sum().max() }')

#Duplicate entry count
df.duplicated().value_counts()

print( ( df.duplicated().value_counts()/len(df) ) * 100)

"""OBSERVATION

---
There are no duplicate entries in this data set

"""

#Pair Plot Gives you an overall insight on how the data's are distributed
sns.pairplot( df )

"""OBSERVATION

---
From the pair plot above some of the observations are :-   

1.    **Age** : From the histogram analysis it can be observed that the graph is left skewed . Also , mentionably high age people are having more High blood pressure.

2.   **SYstolic Pressure** : In this dataset the data points from SysBP is moderately right
3.  **DiaBP and TenYearCHD** : It shows when diaBP are increasing risk of ten year chd also increasing.

4.  **CigsPerDay** : It shows that middle age people are having more cigerate per day.


"""

df.info()

print("\n\n-----------------Unique Values per column--------------------------------\n\n")

df.nunique()

"""All those mentioned below are categorical, education might be a confusion, bt it hase 4 distinct values which are (1,2,3,4) and this is minimal, so it can be categorical, other all mentioned have only two types of values 0 or 1, which is binary posibility and that is of course categorical."""

categorical_columns = ["male" , "education", "currentSmoker" , "BPMeds" ,"prevalentStroke" ,"prevalentHyp" , "diabetes", "TenYearCHD"]
numeric_columns = [ "age" , "cigsPerDay", "totChol", "sysBP", "diaBP", "BMI", "heartRate", "glucose"]

if categorical_target_column:
  for column in categorical_columns:
    if column != target_column_name:
      #sns.barplot(x=column, y='Counts', hue= target_column_name, data= df.groupby([column, target_column_name]).size().reset_index(name="Counts"))
      sns.countplot( x = column , hue = target_column_name , data = df )
      plt.show()

  for column in numeric_columns:
    if column != target_column_name:
      sns.histplot( x = column , hue = target_column_name , data = df)
      plt.show()

else:
  for column in categorical_columns:
      if column != target_column_name:
        sns.histplot( x = target_column_name , hue = column , data = df)
        plt.show()

  for column in numeric_columns:
    if column != target_column_name:
      sns.scatterplot( x = target_column_name , y = column , data = df)
      plt.show()

"""OBSERVATION

---


1.   **TenYearCHD and male**: From the count plot it can be observed that this dataset doesn't have any gender with more risk, both male and female have equal risk for TenYearCHD.

2.  **TenYearCHD and education** : Analysis reveals that a higher proportion of less educated people are more at cardio attack risk, indicating a less risk rate among educated people.

3. **CureentStroke and TenYearCHD** : This pair doesn't show much if difference.

4.   **TenYearCHD and BPMeds**: From the count plot it can be observed that not taking BPMeds people are at higher number of TenYearCHD risk.

5.  **TenYearCHD and PrevalentStroke** : From the plot we find that this dataset has almost 90% data had prevalentStroke, so TanYearCHD risk number of course higher in those who didn't have prevalentStroke.

6. **PrevalentHyp and TenYearCHD** : This pair doesn't show much of difference, we can say for both the categories (0 and 1).

7.   **TenYearCHD and diabates**: It is also same kind of observation as prevalentStroke, which is as the dataset are having huge imbalance in diabates negative data and so the risk for TenYearCHD also are more who are not having diabates.

8.  **TenYearCHD and age** : Analysis reveals that age group 51-64 are at higher risk for heart attack.

9. **CureentStroke and cigsPerDay** : This pair shows that 1-20 cigs data are 90% of data, and from thos 20 cigerate per day with having at higher risk for cardiac attack.

10.   **TenYearCHD and totalChol**: From the count plot it can be observed that cholestoral level 200-280 whoever have this range are at highly risk for ten year chd.

11.  **TenYearCHD and SysBP** : Analysis reveals that a higher proportion of peolpe at risk of TenYearCHD whoever have systolicBP at the range of 120-150.

12. **DiaBP and TenYearCHD** : Range of 70-90 whoever have diastolic bp of this range are at high risk of TenYearCHD.

13.  **TenYearCHD and BMI** : Analysis reveals that BMI range 20.5-30 are at higher risk for heart attack.

14. **heartRate and TenYearCHD** : Range of 66-80 whoever have heartRate of this range are at high risk of TenYearCHD.

15.   **TenYearCHD and glucose**: From the count plot it can be observed that glucose level 70-85 are at higher risk of TanYearCHD.


"""

if categorical_target_column:
  sns.pairplot( data=df , hue = target_column_name)

"""OBSERVATION

---

** People whoever are not taking BPMeds are at higher number of TenYearCHD risk.

** From the graph we find that this dataset has almost 90% data has prevalentStroke.

** Graph also shows that this dataset is imbalance with prevalentHyp also as almost 95% with prevalentHyp positive.

** Mediumly older people are at higher risk of heart disease.

** Older people with high BMI at higher risk of TenYearCHD

"""

df.info()

#Correlation HeatMap for numeric columns among the dataset
sns.heatmap(df.corr( numeric_only =  True))

"""OBSERVATION

---
Based on the correlation matrix, it appears that certain variables like age, prevalentHyp, sysBP, diaBP, and glucose have a more pronounced correlation with TenYearCHD risk. This suggests that older individuals with prevalent hypertension, higher systolic and diastolic blood pressure, and elevated glucose levels are potentially at a higher risk of developing cardiovascular diseases over a ten-year period.

Features and labels are stored in different variables. Categorical columns are encoded using OrdinalEncoder .
"""

X = df.drop(target_column_name , axis=1 )
y =  df[target_column_name]

enc = OrdinalEncoder()
X = enc.fit_transform( X )


le = LabelEncoder()
target_class = y.unique()
y = le.fit_transform( y )

X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.3, random_state=42)

from sklearn.metrics import classification_report, confusion_matrix, recall_score, precision_score
from sklearn.svm import SVC
import seaborn as sns
import matplotlib.pyplot as plt

if categorical_target_column:
    clf = SVC()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print(classification_report(y_test, y_pred, zero_division=1))

    matrix = confusion_matrix(y_test, y_pred)
    sns.heatmap(matrix)
    plt.show()

    sns.barplot(x=target_class, y=recall_score(y_test, y_pred, average=None, zero_division=1))
    plt.title("Class Wise Recall Score (SVM)")
    plt.show()

    sns.barplot(x=target_class, y=precision_score(y_test, y_pred, average=None, zero_division=1))
    plt.title("Class Wise Precision Score (SVM)")
    plt.show()

else:
    # Apply linear regression. As shown in the lab
    print("You need to use Linear Regression as your target column is numeric.")

"""OBSERVATION

---
From the analysis of the classification (SVM) report unveil some variations in precision and recall scores among classes. For class "0," the precision is 0.64, which indicates that the model correctly identifies instances of class "0" 64% of the time. The recall for class "0" is high which is 0.94, meaning the model effectively captures a substantial portion of actual instances belonging to class "0."

However, the performance on class "1" is not so favorable. The precision for class "1" is 0.74, denoting that when the model predicts class "1," it is accurate 74% of the time, which is not so bad. But, the recall for class "1" is comparatively so much low at 0.26, indicating that the model struggles to identify a significant portion of actual instances of class "1."

The overall accuracy of the model is 66%, suggesting that it correctly predicts the class labels for approximately two-thirds of the instances. The macro-average, which provides an unweighted average across classes, yields precision, recall, and F1-score values of 0.69, 0.60, and 0.57, respectively. The weighted average, which considers the class distribution, produces slightly lower values with precision, recall, and F1-score of 0.68, 0.66, and 0.61.
"""

if categorical_target_column:
  clf = tree.DecisionTreeClassifier()
  clf.fit( X_train , y_train )
  y_pred = clf.predict( X_test )

  print( classification_report( y_test , y_pred ) )

  matrix = confusion_matrix( y_test , y_pred )
  sns.heatmap( matrix )
  plt.show()

  sns.barplot( x = target_class ,y = recall_score( y_test , y_pred , average =  None) )
  plt.title( "Class Wise Recall Score (Decision Tree)")
  plt.show()

  sns.barplot( x = target_class ,y = precision_score( y_test , y_pred , average =  None) )
  plt.title( "Class Wise Precision Score (Decision Tree)")
  plt.show()

else:
  #apply linear regression . As shown in lab
  print("You Need to use Linear Regression as your target column in Numeric")

"""OBSERVATION

---

The decision tree model applied to the heart disease dataset achieved an accuracy of 76%. Notably, it exhibited higher precision for individuals without heart disease (class 0) at 86%, compared to those with heart disease (class 1) at 23%. The recall was higher for class 0 at 85% than for class 1 at 25%. The F1-score, considering both precision and recall, was 0.86 for class 0 and 0.24 for class 1.
"""
