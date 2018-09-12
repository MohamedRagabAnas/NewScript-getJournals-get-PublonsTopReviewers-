import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import lxml.html
import re
import sys
import csv
import operator
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
DBLP_SEARCH_URL = DBLP_BASE_URL + "search?q="

driver = webdriver.Chrome()

def readAuthorscsv(CSVFile):
    df=pd.read_csv(CSVFile)
    return df


def query_DBLP(authorName):

    
    driver.get(DBLP_SEARCH_URL+""+authorName)
    html = driver.page_source
    time.sleep(1)
    elem = driver.find_element_by_tag_name("body")
    no_of_pagedowns = 50
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        no_of_pagedowns-=1

    html = driver.page_source    
    return BeautifulSoup(html,"lxml")


def get_journal_conf(authorName):
    
    jours_confs=[]
    
    soup = query_DBLP(authorName)
    jours_confs_Soup=soup.findAll('span', attrs={"itemprop": "isPartOf"})

    for jour_conf in jours_confs_Soup:
        if("name" in str(jour_conf)):
            jours_confs.append(jour_conf.text)

    return jours_confs

def getJournal_ConferenceTopRev():    
    Publons_BASE_URL = 'https://publons.com/journal/'
    Publons_SEARCH_URL = Publons_BASE_URL + "7923/"+"cluster-computing"
    driver.get(Publons_SEARCH_URL)

    toprevElement =driver.find_elements_by_xpath("//*[@class='row']/div/div/section/div/a")

    toprevDict={}

    for rev in toprevElement:
            
            s=str(rev.text)
            revRank= s[s.find("(")+1:s.find(")")]
            revName=s.split(') ')[-1]
            
            if (revRank is not ''):
                toprevDict[revName]=int(revRank)
    #toprevDict=dict((k, v) for k, v in toprevDict.iteritems() if k is not '')
    toprevDict =sorted(toprevDict.items(), key=operator.itemgetter(1),reverse=True)  # sort the Revs collections descending accord. to rank 

    return toprevDict

def checkIfTopRanked(authorNamesFile="Authors.csv",toprevDict=[]):

    authors=readAuthorscsv(authorNamesFile)
    authorNames=authors['Name'].tolist()
    
    authorNames.append("Peng Zhang") # just for test
    authorNames.append("Inoooo") # just for test
    authorNames.append("Sherif Sakr") # just for test

    toprevDict=getJournal_ConferenceTopRev()
    #print toprevDict 

    
    for authorName in authorNames:
        for rev in toprevDict:
            if (authorName in rev[0]):
                print ("Yea",authorName)
            else:
                pass#print "Noo"



def checkIfRevPublishedIn(journal='Algorithmica', Reviewer="Christos Levcopoulos"):

    authorPublishedVenues=get_journal_conf(Reviewer)

    count=0
    published_in = False
    for jour_conf in authorPublishedVenues:
        if (journal == jour_conf):
            count+=1
            published_in=True
        else:
            pass
    return published_in, count        



def main():

    '''venues= get_journal_conf("Christos Levcopoulos ")
    print (venues)'''

    flag, count = checkIfRevPublishedIn("Semantic Web Conference")
    print ('Flag: ' , flag,  'Count', count)

    #checkIfTopRanked()

    '''DF= getJournal_ConferenceTopRev()
    print DF
    driver.quit()'''

    
    
if __name__ == '__main__':
        main()