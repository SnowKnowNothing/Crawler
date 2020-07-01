import pandas as pd
import jieba
import matplotlib.pyplot as plt
from collections import defaultdict


def sent2word(sentence, stopwords):
    seglist = jieba.cut(sentence)
    segResult = []
    for w in seglist:
        segResult.append(w)
    newSent = []
    # 如果词汇是在停用词中，则过滤掉
    for word in segResult:
        if word in stopwords:
            continue
        else:
            newSent.append(word)
    return newSent


def emotional_analysis(text_all):
    ## 载入停用词，使用的是百度的停用词库
    f = open('./WordLibrary/baidu_stopwords.txt', encoding='UTF-8')
    stopwords = f.readlines()
    stopwords = [i.replace("\n", "") for i in stopwords]

    ## 载入情感词
    f1 = open("./WordLibrary/BosonNLP_sentiment_score.txt", encoding='UTF-8')
    senList = f1.readlines()
    senDict = defaultdict()
    for s in senList:
        s = s.replace("\n", "")
        # print(s)
        senDict[s.split(' ')[0]] = float(s.split(' ')[1])
    # 载入否定词
    f2 = open("./WordLibrary/notDict.txt", encoding='UTF-8')
    notList = f2.readlines()
    notList = [x.replace("\n", "") for x in notList if x != '']

    # 载入程度副词
    f3 = open("./WordLibrary/degreeDict.txt", encoding='UTF-8')
    degreeList = f3.readlines()
    degreeDict = defaultdict()
    for d in degreeList:
        degreeDict[d.split(',')[0]] = float(d.split(',')[1])

    t = []
    t.append(sent2word(text_all, stopwords))

    # 评分方法
    def word_score(word_list):
        id = []
        for i in word_list:
            if i in senDict.keys():
                id.append(1)
            elif i in notList:
                id.append(2)
            elif i in degreeDict.keys():
                id.append(3)

        word_nake = []
        for i in word_list:
            if i in senDict.keys():
                word_nake.append(i)
            elif i in notList:
                word_nake.append(i)
            elif i in degreeDict.keys():
                word_nake.append(i)

        score = 0
        w = 1
        score0 = 0
        for i in range(len(id)):
            if id[i] == 1:
                score0 = w * senDict[word_nake[i]]
                w = 1
            elif id[i] == 2:
                w = -1
            elif id[i] == 3:
                w = w * degreeDict[word_nake[i]]
            score = score + score0
            score0 = 0
        return score

    score_list = []
    for i in t[0]:
        score_list.append(word_score(i))
    score_df = pd.DataFrame()
    score_df['word'] = t[0]
    score_df['score'] = score_list
    score_df = score_df.drop_duplicates('word', keep='first')
    #print(score_df)
    return score_df



