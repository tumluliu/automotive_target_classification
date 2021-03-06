from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.decomposition import PCA, KernelPCA, SparsePCA
from sklearn.metrics import confusion_matrix, precision_score, recall_score
import matplotlib.pyplot as plt
import numpy as np
from load_dataset import load_data
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV



data_dir = '/home/kangle/dataset/PedBicCarData'
train_data, train_label, test_data, test_label = load_data(data_dir, 2, 2)

scaler = StandardScaler()
train_data = scaler.fit_transform(train_data)
test_data = scaler.transform(test_data)

print('\nbegin PCA process.')
#pca = PCA(n_components=1000, svd_solver='randomized', whiten=True).fit(train_data)
pca = KernelPCA(n_components=30, kernel='cosine', eigen_solver='arpack', n_jobs=8, fit_inverse_transform=True).fit(train_data)
#pca = SparsePCA(n_components=50,n_jobs=4).fit(train_data)
train_feature = pca.transform(train_data)
print(train_feature.shape)

train_feature_inverse = pca.inverse_transform(train_feature)
print(np.linalg.norm(train_feature_inverse-train_feature)/np.linalg.norm(train_feature))

#plt.plot(pca.explained_variance_ratio_)
#plt.plot(np.cumsum(pca.explained_variance_ratio_))
#plt.show()

# pca = PCA()
# pca.fit(train_data)
# cumsum = np.cumsum(pca.explained_variance_ratio_)
# d = np.argmax(cumsum >= 0.95) + 1
# print(d)


# print('\nbegin gradient boosting classification.')
# # param_grid = {'n_estimators': [300,400],
# #               'learning_rate': [0.1],
# #               'max_depth': [5]}
# #classifier = GridSearchCV(GradientBoostingClassifier(), param_grid)
# #classifier = GridSearchCV(XGBClassifier(), param_grid)
# classifier = XGBClassifier()
# classifier.fit(train_feature, train_label)
# #print("The best parameters are %s with a score of %0.2f" % (classifier.best_params_, classifier.best_score_))

# # cv_params = {'n_estimators': [400, 500]}
# # other_params = {'learning_rate': 0.1, 'n_estimators': 500, 'max_depth': 5, 'min_child_weight': 1, 'seed': 0,
# #                 'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}
# # model = XGBClassifier(**other_params)
# # classifier = GridSearchCV(estimator=model, param_grid=cv_params, scoring='r2', cv=3, verbose=1, n_jobs=8)
# # classifier.fit(train_feature, train_label)
# # print("The best parameters are %s with a score of %0.2f" % (classifier.best_params_, classifier.best_score_))


# print('\npredict for test data.')
# test_feature = pca.transform(test_data)
# print(test_feature.shape)
# test_pred = classifier.predict(test_feature)
# train_pred = classifier.predict(train_feature)

# print('\nevaluate the prediction(train data).')
# conf = confusion_matrix(train_label, train_pred)
# print(conf)
# score_precision = precision_score(train_label, train_pred, average=None)
# score_recall = recall_score(train_label, train_pred, average=None)
# print(score_precision)
# print(score_recall)

# print('\nevaluate the prediction(test data).')
# conf = confusion_matrix(test_label, test_pred)
# print(conf)
# score_precision = precision_score(test_label, test_pred, average=None)
# score_recall = recall_score(test_label, test_pred, average=None)
# print(score_precision)
# print(score_recall)




