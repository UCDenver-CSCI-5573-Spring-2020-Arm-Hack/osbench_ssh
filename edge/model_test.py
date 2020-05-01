import pandas as pd
import numpy as np
import time
from sklearn.metrics import accuracy_score
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.preprocessing import scale, normalize
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.semi_supervised import label_propagation
from sklearn.semi_supervised import LabelSpreading
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier


print('loading data')
x_tr = np.load('x_tr_file.npy')
y_tr = np.load('y_tr_file.npy')
x_te = np.load('x_te_file.npy')
y_te = np.load('y_te_file.npy')
x_va = np.load('x_va_file.npy')
y_va = np.load('y_va_file.npy')
f = open("edge_log.txt","w+")



print('SVM')
st = time.time()
from sklearn import svm
svm_linear = svm.SVC(kernel='linear')
svm_linear.fit(x_tr, y_tr)
svm_linear.score(x_te, y_te)
svm_linear.score(x_va, y_va)
et =  time.time()
f.write("SVM, " + str(et-st)+"\n")

print('Random Forest Classifier')
st = time.time()
rdf = RandomForestClassifier(max_depth=4, random_state=0)
rdf.fit(x_tr, y_tr)
rdf.score(x_te, y_te)
rdf.score(x_va, y_va)
et =  time.time()
f.write('Random Forest Classifier, ' + str(et-st)+"\n")

print('Ada Boost Classifier')
st = time.time()
adb = AdaBoostClassifier(random_state=0)
adb.fit(x_tr, y_tr)
adb.score(x_te, y_te)
adb.score(x_va, y_va)
et =  time.time()
f.write("Ada Boost Classifier, " + str(et-st)+"\n")

print('K Nearest Neighbors Classifier')
st = time.time()
knn = KNeighborsClassifier()
knn.fit(x_tr, y_tr)
knn.score(x_te, y_te)
knn.score(x_va, y_va)
knn.predict(x_va)
et =  time.time()
f.write("K Nearest Neighbors Classifier, " + str(et-st)+"\n")

print('Naive Bayes')
st = time.time()
bay = GaussianNB()
bay.fit(x_tr, y_tr)
bay.score(x_te, y_te)
bay.score(x_va, y_va)
et =  time.time()
f.write("Naive Bayes, " + str(et-st)+"\n")

