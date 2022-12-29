# To use playwright
from playwright.sync_api import sync_playwright
# To parse html response
from bs4 import BeautifulSoup
# To make implicite wait in the code
import time
# To converte time in multiple format
import datetime
# To manage data
import pandas as pd
# To manage the files and directories
import os
# To use regular expressions
import re
# To manage date and time
import datetime
# To have some mathematical function
import math

'''
FUNCTIONS:
Here we create all the function we need for the
scraping.
'''

# Open a page, render the Javascript and parse
# it with BeautifulSoup
def get_page(url):
	with sync_playwright() as playwright:
		# Open new page
		browser = playwright.chromium.launch(headless=True)
		context = browser.new_context()
		page = context.new_page()

		# Get the page
		page.goto(url)
		time.sleep(3) # waiting
		
		# Get the content
		response = page.content()
		soup = BeautifulSoup(response, "html.parser")

		# Close all
		page.close()
		context.close()
		browser.close()  

	return soup

def click_link(url, css, scroll=0):
	with sync_playwright() as playwright:
		# Open new page
		browser = playwright.chromium.launch(headless=True)
		context = browser.new_context()
		page = context.new_page()

		# Get the page
		page.goto(url)
		page.mouse.wheel(0, scroll)
		time.sleep(1) # waiting
		page.click(css)
		time.sleep(1) 

		with page.context.expect_page() as tab:
			# print(tab.value.url)
			url = tab.value.url
			response = tab.value.content()
			soup = BeautifulSoup(response, "lxml")
			result = [url, soup]

		# Close all
		page.close()
		context.close()
		browser.close()  

	return result

# Function to count the maximum number of page
# from a query
def get_max_page(url):
	page = get_page(url)

	if "c42" in url:
		number_of_entities = int(re.findall("\\d+", page.select_one("div.IuRIu span.biGQs").text)[0])
		number_of_pages = math.ceil(number_of_entities/30)
		print("For tours:")
	elif "Attractions" in url:
		number_of_entities = int(re.findall("(?<=of\\s)\\d+",page.select_one("div.Ci").text.replace(",",""))[0])
		number_of_pages = math.ceil(number_of_entities/30)
		print("For attractions:")
	elif "Hotels" in url:
		number_of_entities = int(re.findall("\\d+",page.select_one("span.qrwtg").text.replace(",",""))[0])
		number_of_pages = math.ceil(number_of_entities/30)
		print("For hotel:")
	elif "VRACSearch" in url:
		number_of_entities = int(re.findall("\\d+", page.select_one("div.S5.H4.n").text)[0])
		number_of_pages = math.ceil(number_of_entities/50)
		print("For vacation rental:")
	elif "Restaurants" in url:
		number_of_entities = int(page.select_one("span.SgeRJ span.b").text)
		number_of_pages = math.ceil(number_of_entities/30)
		print("For restaurants:")
	else:
		number_of_entities = 0
		number_of_pages = 0
		print("The link format is not valid...")

	total_time = number_of_pages + number_of_entities

	print(f"Number of entities: {number_of_entities}")
	print(f"Number of pages: {number_of_pages}")
	secondes = str(datetime.timedelta(seconds = (total_time*3.5)))
	print(f"The process will take approximately {secondes}\n")

	return total_time

# Get the first entry link
def get_query(query):
	base_1 = "https://www.tripadvisor.ch/Search?q="
	base_2 = "&searchSessionId=5C06403261128E7969312ED82F061AD61669485490961ssid&sid=B418D3B4C3F74A2E826FEBBDD0AB01ED1669488043512&blockRedirect=true&ssrc=m&isSingleSearch=true&geo=1&o="
	link_max_page = base_1 + query + base_2 + "0"
	return link_max_page

# Format restaurants link format (Ajax)
def format_resto(url):
	geo = re.findall("\\d{6}", url)[0]

	current = datetime.datetime.now()
	
	p1 = "https://www.tripadvisor.com/RestaurantSearch?Action=PAGE&ajax=1&availSearchEnabled=true&sortOrder=popularity&geo="
	p2 = "&itags=10591&eaterydate="
	p3 = "&date="
	p4 = "&time="
	p5 = "&people=2&o=a0"

	resto_url = p1 + geo + p2 + current.strftime("%Y_%m_%d") + p3 + current.strftime("%Y-%m-%d") + p4 + current.strftime("%H:%M:%S") + p5

	return resto_url


# Get the main neccessary links
def get_main_links(query):
	url = get_query(query)

	main_page = click_link(url, "div.prw_search_search_result_geo div.result-content-columns")

	base = "https://www.tripadvisor.com"

	hotel_url = base + main_page[1].select_one(".jdaPs:nth-child(1) a")['href']
	hotel_url = re.sub("(g\\d{6})-", "\\1-oa0-", hotel_url)

	things_url = base + main_page[1].select_one(".jdaPs:nth-child(2) a")['href']

	resto_url = base + main_page[1].select_one(".jdaPs:nth-child(3) a")['href']
	resto_ajax = format_resto(resto_url)

	renta_url = re.sub("(g\\d{6})-","\\1-oa0-Reviews-",hotel_url.replace("Hotels-", "VRACSearch-").replace("-Hotels", "-Vacation_Rentals"))

	things = click_link(things_url, "div.PCHTx.A.krgaa a.raEkE", scroll=4000) 

	things_1_url = things[0]

	things_2_url = base + things[1].select_one("a.KoOWI[href*='c42']").get('href')
	things_2_url = re.sub("(c42)-", "\\1-oa0-", things_2_url)

	main_urls = [things_1_url, things_2_url, hotel_url, renta_url, resto_url, resto_ajax]

	return main_urls

# Get all the necessary links
def get_all_links(query):
	print("Getting the main links...\n")
	main_links = get_main_links(query)

	print("Done! Now estimating the time needed\n")

	total_for_all = 0

	for i in main_links[0:5]:
		total_for_all = total_for_all + get_max_page(i)

	total_for_all = str(datetime.timedelta(seconds = (total_for_all*3.5)))

	print(f"\nIn total, the process will take approximately {total_for_all}")

	return main_links

# Creates all the links of the pages from a query
def search(query):
	max_page = get_max_page(link_max_page)
	all_pages = []
	for i in range(0,max_page):
		all_pages.append(base_1 + query + base_2 + str(i*30))
	return all_pages

# Allows to keep missing value as empty for text
# NOTE: Thank you for the guy who did this: https://gist.github.com/alexanderldavis/628d51405d38bc1d6c45c7eaec9bbd4b
def get_text_if_exists(soup, tag, tag_class=None, return_text=True):
    if tag_class:
        item = soup.find(tag, {"class":tag_class})
    else:
        item = soup.find(tag)
    if item and return_text:
        return item.text
    elif item:
        return item
    return ""

# Allows to keep missing value as empty for
# attributes
def get_attr_if_exists(soup, tag, tag_class=None, return_attr=True):
    if tag_class:
        item = soup.find(tag, {"class":tag_class})
    else:
        item = soup.find(tag)
    if item and return_attr:
        return item['alt']
    elif item:
        return item
    return ""

# Collects all the location names from a page
def get_name(page):
	name = []
	for i in page.select("div[data-widget-type='LOCATIONS'].content-column.result-card"):
		name.append(get_text_if_exists(i, tag = "div", tag_class = "result-title"))
	return name

# Collects all the location ratings from a page
def get_rate(page):
	rate = []
	for i in page.select("div[data-widget-type='LOCATIONS'].content-column.result-card"):
		rate.append(get_attr_if_exists(i, tag = "span", tag_class = "ui_bubble_rating"))
	return rate

# Collects the number of voters for each location
# of a page
def get_review(page):
	review = []
	for i in page.select("div[data-widget-type='LOCATIONS'].content-column.result-card"):
		review.append(get_text_if_exists(i, tag = "div", tag_class = "rating-review-count"))
	return review

# Collects all the location addresses from a page
def get_address(page):
	address = []
	for i in page.select("div[data-widget-type='LOCATIONS'].content-column.result-card"):
		address.append(get_text_if_exists(i, tag = "div", tag_class = "address"))
	return address

# Collects the number of comments for each
# location from a page
def get_comment(page):
	comment = []
	for i in page.select("div[data-widget-type='LOCATIONS'].content-column.result-card"):
		comment.append(get_text_if_exists(i, tag = "div", tag_class = "review-mention-block"))
	return comment

# Collects all the informations cited above
# (name, rating, etc.) and format the in a
# Data Frame (data table)
def collect_data(url):
	page = get_page(url)

	name = get_name(page)
	rate = get_rate(page)
	review = get_review(page)
	address = get_address(page)
	comment = get_comment(page)

	data = {
		"name": name,
		"rate": rate,
		"review": review,
		"address": address,
		"comment": comment
	}

	data = pd.DataFrame(data)

	time.sleep(3)

	return data

# The MAIN FUNCTION which bring all the other
# together. With one query (a place), 
# we get all the information cited above 
# for all the location available in the website.
def tripadvisor(query):
	page_list = search(query)

	print("\nCollection in progress, please wait :)\n")

	data = []

	for link in page_list:
		data.append(collect_data(link))

	data = pd.concat(data)

	file = query + "_tripadvisor.csv"

	data.to_csv(file, header=True, encoding = "utf-8", sep = ";", index = False)

	print(f"Your data was saved as '{file}' in the following folder:\n")
	print(os.getcwd())
	print("\n")

	return data

'''
INTERACTIVE INTERFACE
Now we build the interactive interface to make
the queries possible.
'''

# Welcoming message
# print("Hi! Welcome to the trip advisor scraping app!")
# print("-------------------------------------------------------")
# print("This app helps you to collect data from trip advisor :)\n\n\n")
# 
# term = input("Please enter a location:\n")
# 
# print("\nThank you ;)\n")
# print("So...")
# 
# tripadvisor(term)