from sklearn.linear_model import LogisticRegression
from os.path import join as pjoin
import h5py
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, precision_score, recall_score

data_dir = '/home/kangle/dataset/PedBicCarData'
# file_name = pjoin(data_dir, 'testDataNoCar_01.h5')
# f = h5py.File(file_name, 'r')
# print("Keys: %s" % f.keys())
# key0 = list(f.keys())[0]
# print(key0)
# test_data_raw = f[key0]
# print(test_data_raw.shape)
# imgplot = plt.imshow(test_data_raw[7, 0, :, :])
# plt.show()
#
# test_data_raw = np.array(test_data_raw)

print('load the data.')
# test_data_raw = np.array([], dtype=np.double).reshape(0,1,144,400)
train_data_raw = np.array([])
for i in range(1,21):
    file_index = str(i)
    file_index = "{0:02d}".format(i)
    file_name = 'trainDataNoCar_'+ file_index + '.h5'
    file_name = pjoin(data_dir, file_name)
    print(file_name)
    f = h5py.File(file_name, 'r')
    #print("Keys: %s" % f.keys())
    key0 = list(f.keys())[0]
    train_data_part = f[key0]
    #print(train_data_part.shape)
    #imgplot = plt.imshow(train_data_part[7, 0, :, :])
    #plt.show()
    train_data_part = np.array(train_data_part)
    train_data_part = train_data_part[:,:,0::2,0::4]
    train_data_raw = np.vstack([train_data_raw, train_data_part]) if train_data_raw.size else train_data_part

print(train_data_raw.shape)
#test_data_raw = test_data_raw[:,:,0::2,0::4]
#print(test_data_raw.shape)
#imgplot2 = plt.imshow(test_data_raw[7, 0, :, :])
#plt.show()

train_data = train_data_raw.reshape(train_data_raw.shape[0],-1)
print(train_data.shape)

test_data_raw = np.array([])
for i in range(1,6):
    file_index = str(i)
    file_index = "{0:02d}".format(i)
    file_name = 'testDataNoCar_'+ file_index + '.h5'
    file_name = pjoin(data_dir, file_name)
    print(file_name)
    f = h5py.File(file_name, 'r')
    #print("Keys: %s" % f.keys())
    key0 = list(f.keys())[0]
    test_data_part = f[key0]
    #print(test_data_part.shape)
    #imgplot = plt.imshow(test_data_part[7, 0, :, :])
    #plt.show()
    test_data_part = np.array(test_data_part)
    test_data_part = test_data_part[:,:,0::2,0::4]
    test_data_raw = np.vstack([test_data_raw, test_data_part]) if test_data_raw.size else test_data_part

print(test_data_raw.shape)

test_data = test_data_raw.reshape(test_data_raw.shape[0],-1)
print(test_data.shape)

# read label
file_name = 'trainLabelNoCar.h5'
file_name = pjoin(data_dir, file_name)
f = h5py.File(file_name, 'r')
key0 = list(f.keys())[0]
train_label = f[key0]
train_label = np.array(train_label)
train_label = train_label.flatten()

file_name = 'testLabelNoCar.h5'
file_name = pjoin(data_dir, file_name)
f = h5py.File(file_name, 'r')
key0 = list(f.keys())[0]
test_label = f[key0]
test_label = np.array(test_label)
test_label = test_label.flatten()

print('begin PCA process.')
pca = PCA(n_components=5000, svd_solver='randomized', whiten=True).fit(train_data)
train_feature = pca.transform(train_data)
print(train_feature.shape)
plt.plot(pca.explained_variance_ratio_)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.show()

print('begin Logistic Regression.')
lr = LogisticRegression(solver='lbfgs',multi_class='multinomial',max_iter=400)
lr.fit(train_feature,train_label)

print('predict for test data.')
test_feature = pca.transform(test_data)
print(test_feature.shape)
test_pred = lr.predict(test_feature)
#train_pred = lr.predict(train_feature)

print('evaluate the prediction.')
conf = confusion_matrix(test_label,test_pred)
print(conf)
score_precision = precision_score(test_label, test_pred)
score_recall = recall_score(test_label, test_pred)
print(score_precision)
print(score_recall)

# svm = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid)
# svm = svm.fit(train_data, train_label)