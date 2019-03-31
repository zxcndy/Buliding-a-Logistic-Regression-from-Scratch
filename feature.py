
# coding: utf-8

# In[ ]:


import sys
files = list(sys.argv)

trainfile = files[1]
validfile = files[2]
testfile = files[3]
dictionary = files[4]

formatted_train_out = files[5]
formatted_valid_out = files[6]
formatted_test_out = files[7]

feature_flag = files[8]


# trainfile = './handout/smalldata/smalltrain_data.tsv'
# validfile = './handout/smalldata/smallvalid_data.tsv'
# testfile = './handout/smalldata/smalltest_data.tsv'
# dictionary = './handout/dict.txt'
# 
# formatted_train_out = 'train.tsv'
# formatted_valid_out = 'valid.tsv'
# formatted_test_out = 'test.tsv'
# 
# feature_flag = "2"

# In[ ]:


import csv

train = [[str(code) for code in line.split('\t')] for line in open(trainfile,'r').read().splitlines()]
valid = [[str(code) for code in line.split('\t')] for line in open(validfile,'r').read().splitlines()]
test = [[str(code) for code in line.split('\t')] for line in open(testfile,'r').read().splitlines()]
dic = [[str(code) for code in line.split(' ')] for line in open(dictionary,'r').read().splitlines()]

d = {}
for item in dic:
    d[item[0]] = item[1]

if (int(feature_flag) == 1):
    fFlag = 1
else: 
    fFlag = 2


# In[ ]:


def modelOne_feature(data,dictionary):
    formatted={}

    for i in range(len(data)):
        words = data[i][1].split(' ')
        feature = {}
        for word in words:
            if (word in dictionary.keys()):
                feature[dictionary[word]]= 1
        formatted[i]= feature
    return formatted


# In[ ]:


def modelTwo_feature(data,dictionary,threshold):
    formatted={}

    for i in range(len(data)):
        words = data[i][1].split(' ')
        feature = {}
        uniqueWords = set(words)
        for word in uniqueWords:
            if (word in dictionary.keys()):
                count = words.count(word)
                if (count < threshold):
                    feature[d[word]]= 1
        formatted[i]= feature
    return formatted

def labels(data):
    labels=[]

    for i in range(len(data)):
        labels.append(data[i][0])
    return labels


# In[ ]:


if (fFlag == 1):
    output_train = modelOne_feature(train,d)
    output_test = modelOne_feature(test,d)
    output_valid = modelOne_feature(valid,d)
else:
    output_train = modelTwo_feature(train,d,4)
    output_test = modelTwo_feature(test,d,4)
    output_valid = modelTwo_feature(valid,d,4)

labels_train = labels(train)
labels_test = labels(test)
labels_valid = labels(valid)


# In[ ]:


print(len(output_train[0]))


# In[ ]:


fTrain = open(formatted_train_out,'w')
for i in range(len(output_train)):
    line = str(labels_train[i])
    for item in output_train[i]:
        line = line + "\t" + item + ":"+ str(output_train[i][item])
    line = line + "\n"
    line = line.replace("\'","").replace("{"," ").replace("}"," ")
    print(line)
    fTrain.write(line)

fTrain.close()


# In[ ]:


fValid = open(formatted_valid_out,'w')
for i in range(len(output_valid)):
    line = str(labels_valid[i])
    for item in output_valid[i]:
        line = line + "\t" + item + ":"+ str(output_valid[i][item])
    line = line + "\n"
    line = line.replace("\'","").replace("{"," ").replace("}"," ")
    #print(line)
    fValid.write(line)

fValid.close()


# In[ ]:


fTest = open(formatted_test_out,'w')
for i in range(len(output_test)):
    line = str(labels_test[i])
    for item in output_test[i]:
        line = line + "\t" + item + ":"+ str(output_test[i][item])
    line = line + "\n"
    line = line.replace("\'","").replace("{"," ").replace("}"," ")
    #print(line)
    fTest.write(line)

fTest.close()

