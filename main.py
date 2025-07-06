import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Create output folder
OUTPUT_FOLDER = "data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Configure Selenium
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

def get_page_url(jud_code, page_num):
    return f"https://evaluare.edu.ro/Evaluare/CandFromJudAlfa.aspx?Jud={jud_code}&PageN={page_num}"

def extract_headers(table):
    header_rows = table.find_all("tr")[:2]
    first_row_cells = header_rows[0].find_all(["td", "th"])
    second_row_cells = header_rows[1].find_all(["td", "th"])
    final_headers = []
    second_row_index = 0
    for cell in first_row_cells:
        colspan = int(cell.get("colspan", 1))
        main_text = cell.get_text(strip=True)
        if colspan == 1:
            final_headers.append(main_text)
        else:
            for _ in range(colspan):
                sub_text = second_row_cells[second_row_index].get_text(strip=True)
                full_header = f"{main_text} - {sub_text}"
                final_headers.append(full_header)
                second_row_index += 1
    return final_headers

def extract_judet_name(soup):
    span = soup.find("span", id="ContentPlaceHolderBody_LabelTitle")
    if not span:
        return "UNKNOWN"
    text = span.get_text(strip=True).upper()

    # Known prefixes to strip
    prefixes = [
        "LISTA CANDIDAȚILOR DIN JUDEȚUL",
        "LISTA CANDIDAŢILOR DIN JUDEŢUL",
        "LISTA CANDIDAȚILOR DIN JUDEȚ",
        "LISTA CANDIDAŢILOR DIN JUDEŢ",
        "LISTA CANDIDAŢILOR DIN MUNICIPIUL",
        "LISTA CANDIDAȚILOR DIN MUNICIPIUL"
    ]
    for prefix in prefixes:
        if text.startswith(prefix):
            return text[len(prefix):].strip()
    return text  # Fallback in case format differs

def scrape_jud(jud_code):
    print(f"\n🔍 Scraping JUD_CODE={jud_code}")
    all_data = []
    headers = []
    page_num = 1
    judet_name = None

    while True:
        url = get_page_url(jud_code, page_num)
        print(f"  🔄 Page {page_num} - {url}")
        driver.get(url)
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", class_="mainTable")

        # Stop if page has no results table
        if not table:
            if page_num == 1:
                print(f"  ❌ No data for Jud={jud_code}. Skipping.")
            else:
                print(f"  ✅ Finished all pages for {judet_name} ({jud_code})")
            break

        # Extract county name from first page
        if not judet_name:
            judet_name = extract_judet_name(soup)

        # Extract headers once
        if not headers:
            headers = extract_headers(table)
            headers.append("Județul")

        rows_found = False
        for row in table.find_all("tr")[2:]:
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if cols:
                cols.append(judet_name)
                all_data.append(cols)
                rows_found = True

        if not rows_found:
            break

        page_num += 1

    return headers, all_data, judet_name

# Loop over all Jud codes
for jud_code in range(1, 100):  # go until non-existent
    headers, data, judet_name = scrape_jud(jud_code)
    if not data:
        continue

    df = pd.DataFrame(data, columns=headers)
    safe_name = judet_name.replace(" ", "_").replace("-", "_")
    filename = f"{OUTPUT_FOLDER}/evaluare_{jud_code:02d}_{safe_name}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"  💾 Saved {len(df)} rows to {filename}")

driver.quit()
print("\n✅ All counties processed.")
