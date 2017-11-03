
from selenium import webdriver
from bs4 import BeautifulSoup
browser = webdriver.Firefox()
browser.get('https://twitter.com/search?f=tweets&vertical=default&q=%22aj%20green%22%20since%3A2016-11-14%20until%3A2016-11-17&l=en&src=typd')
pagewith = browser.page_source
soupwith = BeautifulSoup(pagewith,'lxml')
