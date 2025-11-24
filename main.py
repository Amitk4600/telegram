import asyncio
from playwright.async_api import async_playwright
import requests
from datetime import datetime, timezone, timedelta
import os
import random

MAX_PRODUCTS = 50  # Maximum 50 products post karega
EXECUTION_HOURS = 1

# Run only during allowed window (9 AM UTC)
current_hour = datetime.now(timezone.utc).hour
print(f"Current UTC hour: {current_hour}")
if current_hour != 9:
    print(f"⏭️ Not running. Allowed only at 9 AM UTC.")
    exit(0)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")

CATEGORIES = [
    # --- Vitamins, Minerals & Supplements ---
    "vitamins and supplements",
    "multivitamin",
    "vitamin c tablets",
    "vitamin d3 supplement",
    "vitamin b complex",
    "vitamin e supplements",
    "vitamin k supplement",
    "omega 3 fish oil",
    "omega 3 for kids",
    "cod liver oil",
    "calcium supplements",
    "magnesium supplement",
    "zinc supplement",
    "iron supplement",
    "iron + folic acid",
    "biotin supplements",
    "collagen supplements",
    "hyaluronic acid supplements",
    "probiotic supplements",
    "prebiotic supplements",
    "digestive enzymes",
    "fiber supplements",
    "turmeric curcumin",
    "glucosamine chondroitin",
    "coq10 supplements",
    "melatonin sleep aid",
    "sleep supplements",
    "melatonin gummies",
    "herbal sleep support",
    "ashwagandha",
    "shilajit",
    "giloy",
    "ashwagandha capsules (stress)",
    "herbal supplements",
    "ayurvedic tonic",
    "immunity booster",
    "immunity gummies",
    "elderberry syrup",
    "echinacea supplements",
    "green tea extract",
    "apple cider vinegar gummies",
    "weight loss supplements",
    "fat burner",
    "keto products",
    "keto snacks",
    "keto shakes",
    "appetite suppressant",
    "metabolism booster",
    "protein powder",
    "whey protein",
    "plant based protein",
    "pea protein",
    "casein protein",
    "mass gainer",
    "creatine supplement",
    "bcaa",
    "pre workout",
    "post workout recovery",
    "protein bars",
    "protein cookies",
    "meal replacement shakes",
    "collagen powder",
    "beauty supplements",
    "hair growth supplements",
    "skin brightening supplements",
    "nail health supplements",
    "menopause supplements",
    "hormonal balance supplements",
    "prostate health supplements",
    "testosterone booster",
    "sexual stamina herbal",
    "male enhancement capsules",
    "fertility supplements (male)",
    "fertility supplements (female)",
    "prenatal vitamins",
    "postnatal supplements",
    "iron supplement for women",
    "calcium + vitamin d tablets",
    "pcos supplements",
    "pcod supplements",
    # --- Personal Care & Daily Essentials ---
    "personal care",
    "skincare",
    "face wash",
    "moisturizer",
    "sunscreen",
    "serums",
    "anti acne treatments",
    "body wash",
    "hand wash",
    "hand sanitizer",
    "oral care",
    "toothpaste",
    "mouthwash",
    "toothbrush electric",
    "hair care",
    "shampoo",
    "conditioner",
    "hair oil",
    "hair serum",
    "beard oil",
    "beard growth serum",
    "hair removal cream",
    "razors",
    "bikini trimmer",
    "deodorant",
    "intimate deodorant",
    "intimate wipes",
    "intimate cream",
    "women intimate wash",
    "male intimate wash",
    "pH balancing wash",
    "intimate hygiene wipes",
    "daily essentials (sanitary pads)",
    "sanitary pads",
    "tampons",
    "menstrual cup",
    "period underwear",
    "heating pad reusable",
    "reusable heat pack",
    "nappy rash creams (if relevant)",
    "first aid supplies",
    "disinfectant spray",
    # --- Healthcare Devices & Gadgets ---
    "smart health gadgets",
    "fitness tracker",
    "activity tracker",
    "digital weighing scale",
    "body composition analyzer",
    "blood pressure monitor",
    "glucometer",
    "oximeter",
    "nebulizer",
    "thermometer digital",
    "infrared thermometer",
    "tens unit (pain relief)",
    "posture corrector",
    "cervical pillow",
    "orthopedic supports (knee/back)",
    "back support belt",
    "knee cap support",
    "body massager",
    "neck massager",
    "foot massager",
    "handheld massager",
    "massage gun",
    "cold therapy wrap",
    "hot & cold gel pack",
    "TENS device",
    "cpap accessories (if relevant)",
    "hearing aid accessories (if relevant)",
    # --- Fitness & Rehab ---
    "yoga mat",
    "resistance bands",
    "kettlebell",
    "dumbbells",
    "exercise ball",
    "foam roller",
    "kegel exercise balls",
    "pilates ring",
    "postnatal recovery aids",
    "rehab supports",
    # --- Pain Relief & Mobility ---
    "pain relief spray",
    "pain relief gel",
    "pain relief patches",
    "muscle rub",
    "sciatica support pillow",
    "copper compression gloves",
    "arthritis support",
    "orthotic insoles",
    # --- Ayurvedic & Herbal ---
    "ayurvedic products",
    "herbal tonics",
    "natural remedies",
    "giloy products",
    "holy basil (tulsi) supplements",
    "triphala",
    "chyawanprash",
    "ayurvedic immunity powders",
    # --- Diagnostics & Testing ---
    "pregnancy test kit",
    "ovulation kit",
    "ovulation strips",
    "fertility test kits",
    "at home hormone test",
    "home covid test (if relevant and legal)",
    "stool test kits (home)",
    "urine test strips",
    "hemoglobin test strips",
    "urine pregnancy test",
    # --- Sexual Wellness — Male ---
    "male condoms",
    "extra thin condoms",
    "ribbed condoms",
    "dotted condoms",
    "flavoured condoms",
    "latex free condoms",
    "male lubricants",
    "water based lube",
    "silicone based lube",
    "hybrid lubricants",
    "anal lubricants",
    "delay spray",
    "delay cream",
    "performance booster supplements (male)",
    "male sexual stamina herbal",
    "male enhancement capsules",
    "testosterone booster",
    "penis pump",
    "penis sleeve",
    "cock ring",
    "erection gel",
    "stamina delay condoms",
    "male intimate wash",
    "male sexual wellness devices",
    "penis health oils (non-explicit therapeutic)",
    # --- Sexual Wellness — Female ---
    "female condoms",
    "female lubricants",
    "women intimate wash",
    "vaginal wash",
    "vaginal tightening gel",
    "intimate cream for women",
    "pms relief",
    "period pain relief",
    "hormonal balance supplements",
    "intimate wipes (women)",
    "kegel exercisers/weights",
    "vibrators (bullet, wand, rabbit, wand-style)",
    "female sexual wellness devices",
    "clitoral stimulators",
    "suction stimulators",
    "lubricant for sensitive skin",
    "arousal gel for women",
    "female arousal oil (massage safe)",
    "menstrual cups and accessories",
    "ovulation kits",
    "fertility supplements (female)",
    # --- Couple / Shared Products ---
    "couple massager",
    "couple vibe sets",
    "edible lubricants",
    "massage oils (sensual)",
    "intimacy games for couples (adult board games)",
    "lubricant + condom combos",
    "couple kits (starter sexual wellness kits)",
    # --- Sex Toys & Pleasure Devices (Allowed non-graphic wellness items) ---
    "vibrators",
    "bullet vibrators",
    "wand massagers (for personal pleasure)",
    "rabbit vibrators",
    "suction stimulators",
    "penis rings (vibe rings)",
    "anal plugs (beginner to advanced)",
    "sex toy cleaners",
    "toy storage and discretion pouches",
    "toy batteries and chargers",
    "waterproof sex toys",
    "rechargeable sex toys",
    "silicone sex toys (body-safe)",
    # --- Contraception & Reproductive Health ---
    "contraceptive pills (OTC/consult required)",
    "emergency contraception (where legal)",
    "iud care products (post-insertion gels/cleansers)",
    "condom storage",
    "contraception info/guides (books)",
    # --- Pregnancy & Fertility Support ---
    "ovulation kits",
    "pregnancy test kit",
    "prenatal vitamins",
    "fertility support supplements",
    "sperm health supplements",
    "fertility monitors",
    "basal body temperature thermometers",
    # --- Hygiene & Aftercare ---
    "intimate hygiene sprays",
    "aftercare wound wash",
    "post-sex hygiene wipes",
    "antibacterial intimate wash",
    "moisturizing intimate creams",
    # --- Packaging / Discreet Delivery Items (for affiliate postings) ---
    "discreet packaging options",
    "travel sized sexual wellness items",
    "sample packs",
    "trial size supplements",
    # --- Misc / Giftable & Niche ---
    "sexual wellness gift boxes",
    "self care kits",
    "wellness subscription boxes",
    "detox cleanse kits",
    "detox tea",
    "detox foot pads",
    "herbal teas for wellness",
    "sugar substitutes for diet (stevia, erythritol)",
    "gut health kits",
    # --- Educational / Books / Guides ---
    "sexual health books",
    "relationship & intimacy books",
    "yoga for sexual health",
    "meditation guides for libido",
    "cookbooks (keto, low-calorie)",
    # --- NEW ITEMS ADDED ---
    "spirulina supplements",
    "chlorella supplements",
    "astaxanthin capsules",
    "resveratrol supplements",
    "l-theanine capsules",
    "rhodiola rosea capsules",
    "ginkgo biloba capsules",
    "msm joint support",
    "boswellia serrata capsules",
    "brain health supplements",
    "eye health supplements",
    "adaptogen blends",
    "face masks",
    "lip balm",
    "body scrubs",
    "essential oils",
    "makeup removers",
    "hair styling products",
    "dry shampoo",
    "anti-aging creams",
    "adjustable dumbbells",
    "exercise sliders",
    "jump ropes",
    "smart water bottles",
    "recovery boots",
    "pain relief gels (cooling/warming)",
    "back & neck massagers",
    "libido enhancers (herbal)",
    "male masturbators (wellness-safe)",
    "g-spot stimulators (wellness-focused)",
    "travel intimacy products",
]


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

SCRAPED_FILE = "products.txt"
scraped_ids = set()

# Load already scraped products to avoid duplicates
if os.path.exists(SCRAPED_FILE):
    with open(SCRAPED_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                pid = eval(line).get("affiliate_link").split("/dp/")[1].split("/")[0]
                scraped_ids.add(pid)
            except:
                pass

def shorten_link(long_url):
    try:
        r = requests.get("https://tinyurl.com/api-create.php", params={"url": long_url})
        if r.status_code == 200:
            return r.text
        return long_url
    except Exception:
        return long_url

def send_to_telegram(text, image_url=None):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        payload = {"chat_id": CHAT_ID, "caption": text, "parse_mode": "HTML"}
        files = {"photo": requests.get(image_url).content} if image_url else None
        r = requests.post(url, data=payload, files=files)
    except Exception as e:
        print("Telegram send error:", e)

def save_product(data):
    with open(SCRAPED_FILE, "a", encoding="utf-8") as f:
        f.write(str(data) + "\n")

async def safe_goto(page, url, tries=3):
    for attempt in range(tries):
        try:
            await page.goto(url, timeout=60000)
            return True
        except Exception:
            if attempt == tries - 1:
                return False
            await asyncio.sleep(3)

async def scrape_amazon_item(page):
    async def safe(selectors):
        for sel in selectors:
            try:
                txt = await page.inner_text(sel)
                if txt.strip():
                    return txt.strip()
            except:
                continue
        return "Not Available"

    title = await safe(["#productTitle"])
    price = await safe([".a-price .a-offscreen", ".priceToPay .a-offscreen", "#corePrice_feature_div .a-offscreen"])
    rating = await safe(["span.a-icon-alt", "#acrPopover"])
    desc = await safe(["#feature-bullets"])

    img = None
    for sel in ["#landingImage", ".imgTagWrapper img", ".a-dynamic-image"]:
        try:
            img = await page.get_attribute(sel, "src")
            if img:
                break
        except:
            pass

    return title, price, rating, desc, img

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        start_time = datetime.now()
        # Yahan use ho raha hai EXECUTION_HOURS variable jo upar define kiya hai
        end_time = start_time + timedelta(hours=EXECUTION_HOURS) 
        products_posted_count = 0

        print(f"🚀 Script started. Ends at: {end_time} OR after {MAX_PRODUCTS} products.")

        while datetime.now() < end_time and products_posted_count < MAX_PRODUCTS:
            
            random.shuffle(CATEGORIES)

            for q in CATEGORIES:
                # 1. Global Time & Limit Check inside Category Loop
                if datetime.now() >= end_time:
                    print("⏰ Time limit reached. Exiting...")
                    break
                
                if products_posted_count >= MAX_PRODUCTS:
                    print(f"✅ Limit reached: {products_posted_count} products posted. Exiting...")
                    break

                page_num = 1
                
                # Check limited pages per category to switch categories faster
                while page_num <= 3: 
                    # 2. Check limits again inside Page Loop
                    if datetime.now() >= end_time or products_posted_count >= MAX_PRODUCTS:
                        break

                    print(f"🔎 Searching: {q} | Page: {page_num}")
                    search_url = f"https://www.amazon.in/s?k={q}&page={page_num}"
                    
                    if not await safe_goto(page, search_url):
                        print("Skipping category due to page load failure.")
                        break

                    await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                    await asyncio.sleep(2)

                    links = await page.query_selector_all("a.a-link-normal.s-no-outline")
                    urls = []

                    for l in links:
                        href = await l.get_attribute("href")
                        if href and "/dp/" in href:
                            dp = href.split("/dp/")[1].split("/")[0]
                            urls.append(f"https://www.amazon.in/dp/{dp}")

                    new_products = [u for u in urls if u.split("/dp/")[1] not in scraped_ids]

                    if not new_products:
                        print("No new products found on this page.")
                        break # Move to next category if no new products

                    random.shuffle(new_products)

                    for u in new_products:
                        # 3. Check limits again inside Product Loop (Most Critical)
                        if datetime.now() >= end_time:
                            break
                        if products_posted_count >= MAX_PRODUCTS:
                            break

                        product_id = u.split("/dp/")[1]
                        
                        print(f"Processing: {product_id}")
                        if not await safe_goto(page, u):
                            continue

                        title, price, rating, desc, img = await scrape_amazon_item(page)

                        # Skip if price is not available
                        if "Not Available" in price:
                            continue

                        long_aff = f"https://www.amazon.in/dp/{product_id}?tag={AFFILIATE_TAG}"
                        short = shorten_link(long_aff)

                        text = (
                            f"<b>{title}</b>\n\n<b>💰 Price:</b> {price}\n"
                            f"<b>⭐ Rating:</b> {rating}\n\n{desc[:300]}...\n\n<b>🔗 Buy Now:</b> {short}"
                        )

                        send_to_telegram(text, img)
                        
                        # Increment Count
                        products_posted_count += 1
                        print(f"✅ Posted Product #{products_posted_count}/{MAX_PRODUCTS}")

                        save_product({
                            "title": title, "price": price, "rating": rating,
                            "affiliate_link": short, "time": str(datetime.now())
                        })

                        scraped_ids.add(product_id)
                        
                        # Wait between posts to avoid spamming/ban
                        await asyncio.sleep(10) 

                    page_num += 1

            # End of Categories list, small sleep before restarting categories
            await asyncio.sleep(5) 

        await browser.close()
        print(f"🏁 Script Finished. Total Posted: {products_posted_count}")

asyncio.run(main())