## PRODUCT SCRAPE ##

#Specifications Completed**
This console application scrapes the website given and returns a JSON array of all the product options on the page.
Did not include unit tests because I tried to be in the time limit of approximately 2 hours, so I didn't have much time
as well as I don't have a lot of experience on testing web scraping code. I definitely want some improvement and practice
on this part. I'm also sure that there is definitely a better way to sort the items in the JSON file, but I haven't done
anything similar, so I just improvised in the time that I had just to take this requirement out of the way.

#How it works
You have to just run the main.py and the ProductSpider class will scrape all the product options on the given page,
returning an array of ‘option title, ‘description’, ‘price’ and ‘discount’ keys for each of them. Then the SortJson 
class will read this JSON file reordering the items in it based on their annual price, printing them to the Run window
and lastly overwriting them in the new order in the JSON file.

#Dependencies
The library that I use is Scrapy (https://scrapy.org/), as I had already worked with it during the 1st semester of my studies.
The settings for Scrapy are coded in the main.py. 
The IDE that I use is Pycharm and the python version is 3.9. Virtualenv tool is used for the virtual environment.
