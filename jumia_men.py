import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import pandas as pd

# URL 
URL = "https://www.jumia.com.eg/mens-fashion/"

# التحقق من إدخال عدد الصفحات
while True:
    try:
        pages_input = input("Enter number of pages: ").strip()  
        pages = int(pages_input)
        print(f"Entered pages: {pages}")  
        if pages < 1:
            print("Number of pages must be at least 1.")
        else:
            break
    except ValueError:
        print("Please enter a valid number.")

# قوائم البيانات
deals = []
names = []
prices = []
old_prices = []
discounts = []
ratings = []
reviews = []

#   سحب  البيانات
for i in range(1, pages + 1):
    # بناء URL مع الصفحات
    page_url = f"{URL}?page={i}"
    results = requests.get(page_url)
    contents = results.content
    soup = BeautifulSoup(contents, "lxml")

    # سحب المنتجات
    products = soup.find_all("article", class_="prd")  

    for product in products:
        name_element = product.find("h3", class_="name")
        price_element = product.find("div", class_="prc")
        deal_element = product.find("span", class_="bdg _xs camp")
        old_price_element = product.find("div", class_="old")
        discount_element = product.find("div", class_="bdg _dsct _sm")
        rating_element = product.find("div", class_="stars _s")
        review_element = product.find("div", class_="rev")

        names.append(name_element.get_text(strip=True) if name_element else "N/A")
        prices.append(price_element.get_text(strip=True).replace("EGP ", "").replace(",", "") if price_element else "nan")
        deals.append(deal_element.get_text(strip=True) if deal_element else "N/A")
        old_prices.append(old_price_element.get_text(strip=True).replace("EGP ", "").replace(",", "") if old_price_element else "nan")
        discounts.append(discount_element.get_text(strip=True).replace("%", "") if discount_element else "nan")
        ratings.append(rating_element.get_text(strip=True).split(" out of ")[0] if rating_element else "N/A")
        reviews.append(review_element.get_text(strip=True) if review_element else "N/A")

# التأكد من صحة طول القوائم
max_length = max(len(deals), len(names), len(prices), len(old_prices), len(discounts), len(ratings), len(reviews))
deals += [''] * (max_length - len(deals))
names += [''] * (max_length - len(names))
prices += ['nan'] * (max_length - len(prices))
old_prices += ['nan'] * (max_length - len(old_prices))
discounts += ['nan'] * (max_length - len(discounts))
ratings += [''] * (max_length - len(ratings))
reviews += [''] * (max_length - len(reviews))

file_list = [deals, names, prices, old_prices, discounts, ratings, reviews]
exported = zip_longest(*file_list)

# حفظ البيانات في ملف CSV
with open("jumia_products2.csv", "w", newline='', encoding='utf-8') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Deal", "Name", "Price", "Old Price", "Discount", "Rating", "Review"])
    wr.writerows(exported)

print("Data has been written to jumia_products2.csv")

data = {
    "Deal": deals,
    "Name": names,
    "Price": prices,
    "Old Price": old_prices,
    "Discount": discounts,
    "Rating": ratings,
    "Review": reviews
}

df = pd.DataFrame(data)

print(df)
df.info()
