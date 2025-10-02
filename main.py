import pandas as pd
import requests
from bs4 import BeautifulSoup
ProductName = []
Prices = []
Description = []
Reviews = []

for i in range(2, 8):
    url = "https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(i)

    r = requests.get(url)
    print(r)

    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_ = "DOjaWF gdgoEp")

    names = box.find_all("div", class_ = "KzDlHZ")


    for i in names:
        name = i.text
        ProductName.append(name)


    #print(ProductName)

    prices = box.find_all("div", class_ = "Nx9bqj _4b5DiR")

    for i in prices:
        name = i.text
        Prices.append(name)

    #print(Prices)


    desc = box.find_all("ul", class_ = "G4BRas")

    for i in desc:
        name = i.text
        Description.append(name)

    #print(Description) 


    reviews = box.find_all("div", class_ = "XQDdHH")

    for i in reviews:
        name = i.text
        Reviews.append(name)

#print(Reviews)
#print(len(ProductName), len(Prices), len(Description), len(Reviews))
# If mismatched, print a few samples from each list and inspect selectors.

dataFrame = pd.DataFrame({"Product Name":ProductName,"Prices":Prices,"Description":Description,"Reviews":Reviews})
#print(dataFrame)

dataFrame.to_csv("/Users/malem/Scrap Flipkart Project/flipkart_mobiles_under_50000.csv")

#print(soup)
#while True:
#nextPage = soup.find("a", class_ = "_9QVEpD").get("href")
#completeNextPage = "https://www.flipkart.com"+ nextPage
#print(completeNextPage)

#url = completeNextPage
#r = requests.get(url)
#soup = BeautifulSoup(r.text, "lxml")
