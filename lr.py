
# coding: utf-8

# In[ ]:


import sys
files = list(sys.argv)

formattedtrain = files[1]
formattedvalid = files[2]
formattedtest = files[3]

dictionary = files[4]

train_out_labels = files[5]
test_out_labels = files[6]
metrics = files[7]
epoch = int(files[8])


# formattedtrain = './handout/largeoutput/model2_formatted_train.tsv'
# formattedvalid = './handout/largeoutput/model2_formatted_valid.tsv'
# formattedtest = './handout/largeoutput/model2_formatted_test.tsv'
# 
# dictionary = './handout/dict.txt'
# 
# train_out_labels = 'train_out.labels'
# test_out_labels = 'test_out.labels'
# metrics = 'metrics_out.txt'
# epoch = 60

# In[80]:


import csv

train = [[str(code) for code in line.split('\t')] for line in open(formattedtrain,'r').read().splitlines()]
test = [[str(code) for code in line.split('\t')] for line in open(formattedtest,'r').read().splitlines()]
dic = [[str(code) for code in line.split(' ')] for line in open(dictionary,'r').read().splitlines()]

train_y = []
test_y = []
train_x = []
test_x = []

for line in train:
    train_y.append(int(line[0]))
    line.pop(0)
    x =[]
    x.append(0)
    for xid in line:
        s = xid.split(':')
        x.append(int(s[0])+1)
    train_x.append(x)
    
for line in test:
    test_y.append(int(line[0]))
    line.pop(0)
    x =[]
    x.append(0)
    for xid in line:
        s = xid.split(':')
        x.append(int(s[0])+1)
    test_x.append(x)

d = {}
for item in dic:
    d[item[0]] = item[1]


# In[81]:


import math
def SGD(i, xi, yi, theta,learning_rate):
    #print(i, xi, yi,learning_rate)
    matrix = sum([theta[x] for x in xi])
    
    for x in xi:  
        p = - (yi - (math.exp(matrix)/(1+math.exp(matrix))))
        theta[x] = theta[x] - (learning_rate*p)
    return theta


# In[82]:


def pred(X, theta):
    pred_y = []

    for i in range(len(X)):
        prob = 0
        for x in X[i]:
            prob = prob + theta[x]
            yhat = 1/ (1+math.exp(-prob))
        if (yhat >=0.5):
            pred_y.append(1)
        else:
            pred_y.append(0)
    return pred_y

def error(pred_y, Y):
    count = 0
    for i in range(len(pred_y)):
        if (pred_y[i] != Y[i]):
            count = count +1
    error = count/len(pred_y)

    return error


# In[83]:


theta_train = []
theta_test = []

for i in range(len(d)+1):
    theta_train.append(float(0))

for i in range(len(d)+1):
    theta_test.append(float(0))

for e in range(epoch):    
    for i in range(len(train_x)):
        theta_train = SGD(i,train_x[i],train_y[i],theta_train,0.1)    

yhat_train = pred(train_x, theta_train)
yhat_test = pred(test_x, theta_train)

error_train = error(yhat_train,train_y)
error_test = error(yhat_test,test_y)


# In[84]:


print("error(train):" + "{:.6f}".format(error_train))
print("error(test):" + "{:.6f}".format(error_test))
#print(count)


# In[85]:


m = open(metrics,'w')
m.write("error(train): " + "{:.6f}".format(error_train)+"\n")
m.write("error(test): " + "{:.6f}".format(error_test))
m.close()


# In[88]:


l_train = open(train_out_labels,'w')

for i in range(len(yhat_train)):
    l_train.write(str(yhat_train[i])+"\n")
l_train.close()

l_test = open(test_out_labels,'w')

for i in range(len(yhat_test)):
    l_test.write(str(yhat_test[i])+"\n")
l_test.close()

