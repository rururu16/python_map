from selenium import webdriver
import requests # for slack  
from pandas import * 
import time

#Access to page

browser = webdriver.PhantomJS()  # DO NOT FORGET to set path
query = "R"
url = "http://b.hatena.ne.jp/search/text?safe=on&q=" + query + "&users=50"
browser.get(url)

df = pandas.read_csv('trend.csv', index_col=0)

#Insert title,date,bookmarks into CSV file

page = 1 #This number shows the number of current page later

while True: #continue until getting the last page
    if len(browser.find_elements_by_css_selector(".pager-next")) > 0:
        print("######################page: {} ########################".format(page))
        print("Starting to get posts...")
        #get all posts in a page
        posts = browser.find_elements_by_css_selector(".search-result")

        for post in posts:
            title = post.find_element_by_css_selector("h3").text
            date = post.find_element_by_css_selector(".created").text
            bookmarks = post.find_element_by_css_selector(".users span").text
            se = pandas.Series([title, date, bookmarks],['title','date','bookmarks'])
            df = df.append(se, ignore_index=True)
            print(df)

        #after getting all posts in a page, click pager next and then get next all posts again

        btn = browser.find_element_by_css_selector("a.pager-next").get_attribute("href")
        print("next url:{}".format(btn))
        browser.get(btn)
        page+=1
        browser.implicitly_wait(10)
        print("Moving to next page......")
        time.sleep(10)
    else: #if no pager exist, stop.
        print("no pager exist anymore")
        break

df.to_csv(query + ".csv")
print("DONE")