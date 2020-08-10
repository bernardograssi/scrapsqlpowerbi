from bs4 import BeautifulSoup
from urllib.request import urlopen
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import pymysql



# Establish connection to MySQL and create database.
def DfToSQL(df):
    sqlEngine = create_engine("mysql+pymysql://root:grassi@127.0.0.1/cities")
    dbConnection = sqlEngine.connect()
    df.to_sql("most_populated_cities", dbConnection)


# Create scrapper object, do the scrapping, convert it to a pandas DataFrame and call DfToSQL.
def ScrapWebsite():
    url = "https://en.wikipedia.org/wiki/List_of_largest_cities"
    list_of_cities, list_of_pops, list_of_countries = [], [], []
    webpage_html = urlopen(url)
    scrapper_object = BeautifulSoup(webpage_html.read(), 'html.parser')
    table = scrapper_object.find_all("table")[1]
    table_body = table.find("tbody")
    for tag in table_body.find_all("tr"):
        found = tag.find("td")
        if found != None:
            list_of_cities.append(tag.findAll("td")[0].get_text().strip("\n"))
            list_of_countries.append(tag.findAll("td")[1].get_text().strip("\xa0\n"))
            list_of_pops.append(tag.findAll("td")[3].get_text().strip("\xa0\n"))

    df = pd.DataFrame({"City": list_of_cities,
                       "Country": list_of_countries,
                       "Population": list_of_pops})
    DfToSQL(df)


def main():
    ScrapWebsite()

main()
