import asyncio
import re
from playwright.async_api import async_playwright
import requests
from datetime import datetime, timezone, timedelta
import os
import random

# MAX_PRODUCTS = 150
# EXECUTION_HOURS = 4

# Run only during allowed window (9 AM UTC)
# current_hour = datetime.now(timezone.utc).hour
# print(f"Current UTC hour: {current_hour}")
# if current_hour != 9:
#     print(f"⏭️ Not running. Allowed only at 9 AM UTC.")
#     exit(0)

TELEGRAM_TOKEN = "8734950255:AAHV-0nuTLtkwrOF-7ur6atCzdMzXyBbWDM"
CHAT_ID = "@GadgetsDealIndia"
AFFILIATE_TAG = "crystabloom - 21"

# CATEGORIES = [
# "Mobile Phones",
# "Mobile Accessories",
# "Laptops",
# "PC Components",
# "Smartwatches",
# "Fitness Bands",
# "Gaming Consoles",
# "Gaming Accessories",
# "Smart Home",
# "Home Appliances",
# "Cameras & Photography",
# "Audio & Headphones",
# "Networking Devices",
# "Drones & Accessories",
# "Wearable Health Devices",
# "TVs & Home Entertainment",
# "Printers & Office Equipment",
# "Car Tech & Gadgets",
# "Chargers & Power Banks",
# "Tech Gifts & Gadgets",
#     "smartphone deals",
#     "laptop deals",
#     "earbuds deals",
#     "smartwatch deals",
#     "gaming mouse deals",
#     "bluetooth speaker deals",
#     "power bank deals",
#     "ssd deals",
#     "wifi router deals",
#     "monitor deals",
# ]


# SCRAPED_FILE = "products.txt"
# scraped_ids = set()

# if os.path.exists(SCRAPED_FILE):
#     with open(SCRAPED_FILE, "r", encoding="utf-8") as f:
#         for line in f:
#             try:
#                 pid = eval(line).get("affiliate_link").split("/dp/")[1].split("/")[0]
#                 scraped_ids.add(pid)
#             except:
#                 pass


# def shorten_link(long_url):
#     try:

#         r = requests.get("https://tinyurl.com/api-create.php", params={"url": long_url})
#         if r.status_code == 200:

#             return r.text

#         return long_url
#     except Exception as e:

#         return long_url


# def send_to_telegram(text, image_url=None):
#     try:

#         url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
#         payload = {"chat_id": CHAT_ID, "caption": text, "parse_mode": "HTML"}

#         files = {"photo": requests.get(image_url).content} if image_url else None
#         r = requests.post(url, data=payload, files=files)

#     except Exception as e:
#         print("Telegram send error:", e)


# def save_product(data):

#     with open(SCRAPED_FILE, "a", encoding="utf-8") as f:
#         f.write(str(data) + "\n")


# async def safe_goto(page, url, tries=3):
#     for attempt in range(tries):
#         try:

#             await page.goto(url, timeout=60000)
#             return True
#         except Exception as e:

#             if attempt == tries - 1:
#                 return False
#             await asyncio.sleep(3)


# async def scrape_amazon_item(page):
#     async def safe(selectors):
#         for sel in selectors:
#             try:
#                 txt = await page.inner_text(sel)
#                 if txt.strip():
#                     return txt.strip()
#             except:
#                 continue
#         return "Not Available"

#     title = await safe(["#productTitle"])
#     price = await safe(
#         [
#             ".a-price .a-offscreen",
#             ".priceToPay .a-offscreen",
#             "#corePrice_feature_div .a-offscreen",
#         ]
#     )
#     rating = await safe(["span.a-icon-alt", "#acrPopover"])
#     desc = await safe(["#feature-bullets"])

#     img = None
#     for sel in ["#landingImage", ".imgTagWrapper img", ".a-dynamic-image"]:
#         try:
#             img = await page.get_attribute(sel, "src")
#             if img:
#                 break
#         except:
#             pass

#     return title, price, rating, desc, img


# async def main():
#     async with async_playwright() as p:

#         # FIXED: No automationcontrolled issue
#         browser = await p.firefox.launch(headless=True)

#         page = await browser.new_page(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#         )

#         start_time = datetime.now(timezone.utc)
#         end_time = start_time + timedelta(hours=1)

#         while datetime.now() < end_time:
#             print(f"Starting new cycle at: {datetime.now()}")

#             random.shuffle(CATEGORIES)

#             for q in CATEGORIES:
#                 if datetime.now() >= end_time:
#                     print("One-hour limit reached. Stopping...")
#                     break

#                 page_num = 1

#                 while True:
#                     if datetime.now() >= end_time:
#                         break

#                     search_url = f"https://www.amazon.in/s?k={q}&page={page_num}"
#                     if not await safe_goto(page, search_url):
#                         print("Skipping category due to page load failure.")
#                         break

#                     await page.evaluate(
#                         "window.scrollBy(0, document.body.scrollHeight)"
#                     )
#                     await asyncio.sleep(2)

#                     links = await page.query_selector_all(
#                         "a.a-link-normal.s-no-outline"
#                     )
#                     urls = []

#                     for l in links:
#                         href = await l.get_attribute("href")
#                         if href and "/dp/" in href:
#                             dp = href.split("/dp/")[1].split("/")[0]
#                             urls.append(f"https://www.amazon.in/dp/{dp}")

#                     new_products = [
#                         u for u in urls if u.split("/dp/")[1] not in scraped_ids
#                     ]

#                     if not new_products:
#                         break

#                     random.shuffle(new_products)

#                     for u in new_products:
#                         if datetime.now() >= end_time:
#                             break

#                         product_id = u.split("/dp/")[1]

#                         if not await safe_goto(page, u):

#                             continue

#                         title, price, rating, desc, img = await scrape_amazon_item(page)

#                         long_aff = (
#                             f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
#                         )
#                         short = shorten_link(long_aff)

#                         text = (
#                             f"<b>{title}</b>\n\n<b>💰 Price:</b> {price}\n"
#                             f"<b>⭐ Rating:</b> {rating}\n\n{desc[:600]}...\n\n<b>🔗 Buy Now:</b> {short}"
#                         )

#                         send_to_telegram(text, img)

#                         save_product(
#                             {
#                                 "title": title,
#                                 "price": price,
#                                 "rating": rating,
#                                 "affiliate_link": short,
#                                 "time": str(datetime.now()),
#                             }
#                         )

#                         scraped_ids.add(product_id)
#                         await asyncio.sleep(8)

#                     page_num += 1
#             # await asyncio.sleep(300)


# asyncio.run(main())

# SCRAPED_FILE = "products.txt"
# scraped_ids = set()

# # Load already scraped products to avoid duplicates
# if os.path.exists(SCRAPED_FILE):
#     with open(SCRAPED_FILE, "r", encoding="utf-8") as f:
#         for line in f:
#             try:
#                 pid = eval(line).get("affiliate_link").split("/dp/")[1].split("/")[0]
#                 scraped_ids.add(pid)
#             except:
#                 pass

# def shorten_link(long_url):
#     try:
#         r = requests.get("https://tinyurl.com/api-create.php", params={"url": long_url})
#         if r.status_code == 200:
#             return r.text
#         return long_url
#     except Exception:
#         return long_url

# def send_to_telegram(text, image_url=None):
#     try:
#         url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
#         payload = {"chat_id": CHAT_ID, "caption": text, "parse_mode": "HTML"}
#         files = {"photo": requests.get(image_url).content} if image_url else None
#         r = requests.post(url, data=payload, files=files)
#     except Exception as e:
#         print("Telegram send error:", e)

# def save_product(data):
#     with open(SCRAPED_FILE, "a", encoding="utf-8") as f:
#         f.write(str(data) + "\n")

# async def safe_goto(page, url, tries=3):
#     for attempt in range(tries):
#         try:
#             await page.goto(url, timeout=60000)
#             return True
#         except Exception:
#             if attempt == tries - 1:
#                 return False
#             await asyncio.sleep(3)

# async def scrape_amazon_item(page):
#     async def safe(selectors):
#         for sel in selectors:
#             try:
#                 txt = await page.inner_text(sel)
#                 if txt.strip():
#                     return txt.strip()
#             except:
#                 continue
#         return "Not Available"

#     title = await safe(["#productTitle"])
#     price = await safe([".a-price .a-offscreen", ".priceToPay .a-offscreen", "#corePrice_feature_div .a-offscreen"])
#     rating = await safe(["span.a-icon-alt", "#acrPopover"])
#     desc = await safe(["#feature-bullets"])

#     img = None
#     for sel in ["#landingImage", ".imgTagWrapper img", ".a-dynamic-image"]:
#         try:
#             img = await page.get_attribute(sel, "src")
#             if img:
#                 break
#         except:
#             pass

#     return title, price, rating, desc, img

# async def main():
#     async with async_playwright() as p:
#         browser = await p.firefox.launch(headless=True)
#         page = await browser.new_page(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#         )

#         start_time = datetime.now()
#         # Yahan use ho raha hai EXECUTION_HOURS variable jo upar define kiya hai
#         end_time = start_time + timedelta(hours=EXECUTION_HOURS)
#         products_posted_count = 0

#         print(f"🚀 Script started. Ends at: {end_time} OR after {MAX_PRODUCTS} products.")

#         while datetime.now() < end_time and products_posted_count < MAX_PRODUCTS:

#             random.shuffle(CATEGORIES)

#             for q in CATEGORIES:
#                 # 1. Global Time & Limit Check inside Category Loop
#                 if datetime.now() >= end_time:
#                     print("⏰ Time limit reached. Exiting...")
#                     break

#                 if products_posted_count >= MAX_PRODUCTS:
#                     print(f"✅ Limit reached: {products_posted_count} products posted. Exiting...")
#                     break

#                 page_num = 1

#                 # Check limited pages per category to switch categories faster
#                 while page_num <= 3:
#                     # 2. Check limits again inside Page Loop
#                     if datetime.now() >= end_time or products_posted_count >= MAX_PRODUCTS:
#                         break

#                     print(f"🔎 Searching: {q} | Page: {page_num}")
#                     search_url = f"https://www.amazon.in/s?k={q}&page={page_num}"

#                     if not await safe_goto(page, search_url):
#                         print("Skipping category due to page load failure.")
#                         break

#                     await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
#                     await asyncio.sleep(2)

#                     links = await page.query_selector_all("a.a-link-normal.s-no-outline")
#                     urls = []

#                     for l in links:
#                         href = await l.get_attribute("href")
#                         if href and "/dp/" in href:
#                             dp = href.split("/dp/")[1].split("/")[0]
#                             urls.append(f"https://www.amazon.in/dp/{dp}")

#                     new_products = [u for u in urls if u.split("/dp/")[1] not in scraped_ids]

#                     if not new_products:
#                         print("No new products found on this page.")
#                         break # Move to next category if no new products

#                     random.shuffle(new_products)

#                     for u in new_products:
#                         # 3. Check limits again inside Product Loop (Most Critical)
#                         if datetime.now() >= end_time:
#                             break
#                         if products_posted_count >= MAX_PRODUCTS:
#                             break

#                         product_id = u.split("/dp/")[1]

#                         print(f"Processing: {product_id}")
#                         if not await safe_goto(page, u):
#                             continue

#                         title, price, rating, desc, img = await scrape_amazon_item(page)

#                         # Skip if price is not available
#                         if "Not Available" in price:
#                             continue

#                         long_aff = f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
#                         short = shorten_link(long_aff)

#                         text = (
#                             f"<b>{title}</b>\n\n<b>💰 Price:</b> {price}\n"
#                             f"<b>⭐ Rating:</b> {rating}\n\n{desc[:300]}...\n\n<b>🔗 Buy Now:</b> {short}"
#                         )

#                         send_to_telegram(text, img)

#                         # Increment Count
#                         products_posted_count += 1
#                         print(f"✅ Posted Product #{products_posted_count}/{MAX_PRODUCTS}")

#                         save_product({
#                             "title": title, "price": price, "rating": rating,
#                             "affiliate_link": short, "time": str(datetime.now())
#                         })

#                         scraped_ids.add(product_id)

#                         # Wait between posts to avoid spamming/ban
#                         await asyncio.sleep(10)

#                     page_num += 1

#             # End of Categories list, small sleep before restarting categories
#             await asyncio.sleep(5)

#         await browser.close()
#         print(f"🏁 Script Finished. Total Posted: {products_posted_count}")

# asyncio.run(main())


# EXECUTION_HOURS = 5
# MAX_PRODUCTS = 100

# SCRAPED_FILE = "products.txt"
# scraped_ids = set()
# if os.path.exists(SCRAPED_FILE):
#     with open(SCRAPED_FILE, "r", encoding="utf-8") as f:
#         for line in f:
#             try:
#                 pid = eval(line)["id"]
#                 scraped_ids.add(pid)
#             except:
#                 pass


# def shorten_link(url):
#     try:
#         r = requests.get("https://tinyurl.com/api-create.php", params={"url": url})
#         return r.text
#     except:
#         return url


# def send_to_telegram(text, image_url):
#     try:
#         url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

#         payload = {"chat_id": CHAT_ID, "caption": text, "parse_mode": "HTML"}

#         files = {"photo": requests.get(image_url).content}

#         requests.post(url, data=payload, files=files)

#     except Exception as e:
#         print("Telegram Error:", e)


# def save_product(data):
#     with open(SCRAPED_FILE, "a", encoding="utf-8") as f:
#         f.write(str(data) + "\n")


# async def safe_goto(page, url):
#     try:
#         await page.goto(url, timeout=60000)
#         return True
#     except:
#         return False


# async def scrape_product(page):

#     async def safe(selector):
#         try:
#             txt = await page.inner_text(selector)
#             return txt.strip()
#         except:
#             return "Not Available"

#     title = await safe("#productTitle")

#     price = await safe(".a-price .a-offscreen")

#     rating = await safe("span.a-icon-alt")

#     desc = await safe("#feature-bullets")

#     img = None

#     for sel in ["#landingImage", ".a-dynamic-image"]:
#         try:
#             img = await page.get_attribute(sel, "src")
#             if img:
#                 break
#         except:
#             pass

#     return title, price, rating, desc, img


# async def main():

#     async with async_playwright() as p:

#         browser = await p.firefox.launch(headless=True)

#         page = await browser.new_page()

#         start_time = datetime.now()
#         end_time = start_time + timedelta(hours=EXECUTION_HOURS)

#         products_posted = 0

#         print("Script Started")

#         while datetime.now() < end_time and products_posted < MAX_PRODUCTS:

#             random.shuffle(CATEGORIES)

#             for q in CATEGORIES:

#                 page_num = 1

#                 while page_num <= 3:

#                     search_url = f"https://www.amazon.in/s?k={q}&i=electronics&p_n_deal_type=26921224031&p_n_pct-off-with-tax=2665400031&page={page_num}"

#                     print("Searching:", q, "Page:", page_num)

#                     ok = await safe_goto(page, search_url)

#                     if not ok:
#                         break

#                     await page.evaluate(
#                         "window.scrollBy(0, document.body.scrollHeight)"
#                     )

#                     await asyncio.sleep(2)

#                     links = await page.query_selector_all(
#                         "a.a-link-normal.s-no-outline"
#                     )

#                     urls = []

#                     for l in links:
#                         href = await l.get_attribute("href")

#                         if href and "/dp/" in href:
#                             pid = href.split("/dp/")[1].split("/")[0]

#                             if pid not in scraped_ids:
#                                 urls.append(f"https://www.amazon.in/dp/{pid}")

#                     if not urls:
#                         break

#                     random.shuffle(urls)

#                     for u in urls:

#                         if products_posted >= MAX_PRODUCTS:
#                             break

#                         product_id = u.split("/dp/")[1]

#                         print("Opening:", product_id)

#                         ok = await safe_goto(page, u)

#                         if not ok:
#                             continue

#                         title, price, rating, desc, img = await scrape_product(page)

#                         if "Not Available" in price:
#                             continue

#                         aff = (
#                             f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
#                         )

#                         short = shorten_link(aff)

#                         text = (
#                             f"🔥 <b>Deal Alert</b>\n\n"
#                             f"<b>{title}</b>\n\n"
#                             f"💰 <b>Price:</b> {price}\n"
#                             f"⭐ <b>Rating:</b> {rating}\n\n"
#                             f"{desc[:200]}...\n\n"
#                             f"🛒 <b>Buy Now:</b> {short}"
#                         )

#                         send_to_telegram(text, img)

#                         save_product(
#                             {
#                                 "id": product_id,
#                                 "title": title,
#                                 "price": price,
#                                 "time": str(datetime.now()),
#                             }
#                         )

#                         scraped_ids.add(product_id)

#                         products_posted += 1

#                         print("Posted:", products_posted)

#                         await asyncio.sleep(10)

#                     page_num += 1

#         await browser.close()

#         print("Finished")


# asyncio.run(main())

MAX_PRODUCTS = 50
EXECUTION_HOURS = 2
SCRAPED_FILE = "products.txt"
PRICE_FILE = "prices.txt"

scraped_ids = set()
price_cache = {}

CATEGORIES = [
    "Mobile Phones",
    "smartphone deals",
    "Mobile Accessories",
    "earbuds deals",
    "Audio & Headphones",
    "smartwatch deals",
    "Smartwatches",
    "power bank deals",
    "Chargers & Power Banks",
    "bluetooth speaker deals",
    "Laptops",
    "laptop deals",
    "Gaming Accessories",
    "ssd deals",
    "wifi router deals",
    "monitor deals",
    "Smart Home",
    "Networking Devices",
]

# ----------------------------------------

if os.path.exists(SCRAPED_FILE):
    with open(SCRAPED_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                scraped_ids.add(eval(line)["id"])
            except:
                pass

if os.path.exists(PRICE_FILE):
    with open(PRICE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                d = eval(line)
                price_cache[d["id"]] = d["price"]
            except:
                pass


def shorten_link(url):
    try:
        r = requests.get("https://tinyurl.com/api-create.php", params={"url": url})
        return r.text
    except:
        return url


def extract_price(p):
    try:
        num = re.sub(r"[^\d]", "", p)
        return int(num)
    except:
        return 0


def send_to_telegram(text, image_url):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        payload = {"chat_id": CHAT_ID, "caption": text, "parse_mode": "HTML"}
        files = {"photo": requests.get(image_url).content} if image_url else None
        requests.post(url, data=payload, files=files)
    except:
        pass


def save_product(data):
    with open(SCRAPED_FILE, "a", encoding="utf-8") as f:
        f.write(str(data) + "\n")


def save_price(data):
    with open(PRICE_FILE, "a", encoding="utf-8") as f:
        f.write(str(data) + "\n")


async def safe_goto(page, url):
    try:
        await page.goto(url, timeout=60000)
        return True
    except:
        return False


async def scrape_product(page):

    async def safe(selector):
        try:
            txt = await page.inner_text(selector)
            return txt.strip()
        except:
            return "Not Available"

    title = await safe("#productTitle")
    price = await safe(".a-price .a-offscreen")
    rating = await safe("span.a-icon-alt")
    desc = await safe("#feature-bullets")

    img = None
    for sel in ["#landingImage", ".a-dynamic-image"]:
        try:
            img = await page.get_attribute(sel, "src")
            if img:
                break
        except:
            pass

    discount = await safe(".savingsPercentage")

    return title, price, rating, desc, img, discount


def make_hashtags(title):
    words = re.findall(r"\b[A-Za-z]{4,}\b", title)
    tags = words[:5]
    return " ".join([f"#{w}" for w in tags])


async def main():
    await asyncio.sleep(random.randint(12, 20))

    async with async_playwright() as p:

        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()

        start = datetime.now()
        end = start + timedelta(hours=EXECUTION_HOURS)

        posted = 0

        while datetime.now() < end and posted < MAX_PRODUCTS:

            random.shuffle(CATEGORIES)

            for q in CATEGORIES:

                page_num = 1

                while page_num <= 3:

                    if posted >= MAX_PRODUCTS:
                        break

                    search_url = f"https://www.amazon.in/s?k={q}&i=electronics&p_n_deal_type=26921224031&p_n_pct-off-with-tax=2665400031&page={page_num}"

                    product_page = await browser.new_page()

                    ok = await safe_goto(page, search_url)
                    if not ok:
                        continue

                    title, price, rating, desc, img, discount = await scrape_product(
                        product_page
                    )

                    await product_page.close()

                    await page.evaluate(
                        "window.scrollBy(0, document.body.scrollHeight)"
                    )
                    await asyncio.sleep(2)

                    links = await page.query_selector_all(
                        "a.a-link-normal.s-no-outline"
                    )

                    urls = []

                    for l in links:
                        href = await l.get_attribute("href")
                        if href and "/dp/" in href:
                            pid = href.split("/dp/")[1].split("/")[0]
                            if pid not in scraped_ids:
                                urls.append(f"https://www.amazon.in/dp/{pid}")

                    if not urls:
                        break

                    random.shuffle(urls)

                    for u in urls:

                        if posted >= MAX_PRODUCTS:
                            break

                        product_id = u.split("/dp/")[1]

                        ok = await safe_goto(page, u)
                        if not ok:
                            continue

                        title, price, rating, desc, img, discount = (
                            await scrape_product(page)
                        )

                        if "Not Available" in price:
                            continue

                        price_val = extract_price(price)

                        # PRICE DROP DETECTION
                        price_drop = ""
                        if product_id in price_cache:
                            old = price_cache[product_id]
                            if price_val < old:
                                price_drop = "📉 <b>Price Drop Alert!</b>\n"
                        price_cache[product_id] = price_val
                        save_price({"id": product_id, "price": price_val})

                        # LIGHTNING DEAL DETECTION
                        lightning = ""
                        if "Lightning Deal" in desc or "Limited time deal" in desc:
                            lightning = "⚡ <b>Lightning Deal</b>\n"

                        # 50% DEAL DETECTION
                        heavy = ""
                        if "%" in discount:
                            try:
                                d = int(re.sub(r"[^\d]", "", discount))
                                if d >= 50:
                                    heavy = "🔥 <b>50%+ OFF DEAL</b>\n"
                            except:
                                pass

                        aff = (
                            f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
                        )
                        short = shorten_link(aff)

                        hashtags = make_hashtags(title)

                        text = (
                            f"{heavy}{lightning}{price_drop}"
                            f"🛍 <b>{title}</b>\n\n"
                            f"💰 <b>Price:</b> {price}\n"
                            f"⭐ <b>Rating:</b> {rating}\n\n"
                            f"{desc[:200]}...\n\n"
                            f"🛒 <b>Buy Now:</b> {short}\n\n"
                            f"{hashtags}\n"
                            f"#Deals #AmazonDeals #TechDeals"
                        )

                        send_to_telegram(text, img)

                        save_product(
                            {
                                "id": product_id,
                                "title": title,
                                "price": price,
                                "time": str(datetime.now()),
                            }
                        )

                        scraped_ids.add(product_id)

                        posted += 1

                        await asyncio.sleep(10)

                    page_num += 1

        await browser.close()


asyncio.run(main())
