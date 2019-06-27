#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 17:46:42 2019

@author: jacky.chen
"""
import requests, json
x_csrftoken = ""
x_newrelic_id = ""

#%% make function to get like and dislike

def getQuestInfo(slug):
    url = "https://leetcode.com/graphql"
    headers = {"Content-Type": "application/json",
               "x-csrftoken": x_csrftoken,
               "x-newrelic-id": x_newrelic_id}
    body = {"operationName":"questionData","variables":{"titleSlug": slug},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}
    r = requests.post(url, headers=headers, data=json.dumps(body))
    jsonData = r.json()
    title = ""
    likes = -1
    dislikes = -1
    if "data" in jsonData.keys():
        if "question" in jsonData["data"].keys():
            if "title" in jsonData["data"]["question"].keys():
                title = jsonData["data"]["question"]["title"]
            if "likes" in jsonData["data"]["question"].keys():
                likes = jsonData["data"]["question"]["likes"]
            if "dislikes" in jsonData["data"]["question"].keys():
                dislikes = jsonData["data"]["question"]["dislikes"]
    #print(title, likes, dislikes)
    return {"title": title, "likes": likes, "dislikes": dislikes} 


twoSumInfo = getQuestInfo("two-sum")
print(twoSumInfo["title"], twoSumInfo["likes"], twoSumInfo["dislikes"])

#%% get all question slugs

url = "https://leetcode.com/api/problems/all/"
headers = {"Content-Type": "application/json",
           "x-newrelic-id": x_newrelic_id}
r = requests.get(url, headers=headers)
jsonData = r.json()
#print(jsonData)

allSlugs = []
quests = []

##Other columns
#"frontend_question_id"
#"difficulty": {
#                "level": 3
#            },
#"progress": 0

if "stat_status_pairs" in jsonData.keys():
    for q in jsonData["stat_status_pairs"]:
        if "stat" in q.keys():
            if "question__title_slug" in q["stat"].keys():
                allSlugs.append(q["stat"]["question__title_slug"])
          
print(allSlugs[:20])
print(len(allSlugs))


#%%

def getLikedSlugs(start, end):
    goodQuests = []
    for slug in allSlugs[start: end]:
        questInfo = getQuestInfo(slug)
        title = questInfo["title"]
        likes = int(questInfo["likes"])
        dislikes = int(questInfo["dislikes"])
        if dislikes > 0 and likes // dislikes >= 2:
            goodQuests.append([title, likes, dislikes])
    return goodQuests


getLikedSlugs(20, 40)
            
        
