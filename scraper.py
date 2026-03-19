from ddgs import DDGS
import requests
import os
import time

# 1. Folder Setup
search_query = "powdery mildew leaf disease close up"
folder_name = "Dataset/powdery_mildew"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Created folder: {folder_name}")

# 2. Searching images
print(f"Scraping the web for '{search_query}'...")
image_urls = []

try:
    # Using the new DDGS library
    with DDGS() as ddgs:
        results = list(ddgs.images(search_query, max_results=50))
        for res in results:
            image_urls.append(res['image'])
            
    print(f"Found {len(image_urls)} image links. Starting download...")

except Exception as e:
    print(f"\n🛑 SCRAPE FAILED: {e}")
    print("DuckDuckGo blocked the request. Please connect to a mobile hotspot or wait 15 minutes, then try again.")
    exit() # Stops the script gracefully

# 3. Download the images
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

success_count = 0
for i, url in enumerate(image_urls):
    file_path = os.path.join(folder_name, f"powdery_mildew_{i+1}.jpg")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded {i+1}/50")
            success_count += 1
        else:
            print(f"❌ Failed {i+1}: Status code {response.status_code}")
    except Exception as e:
        print(f"❌ Error on {i+1}: {e.__class__.__name__}")
        
    # Adding a tiny 0.5 second pause between downloads to play nice with servers
    time.sleep(0.5) 

print(f"\nDone! Successfully downloaded {success_count} images to the '{folder_name}' folder.")