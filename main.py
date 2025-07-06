from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

JUD_CODE = 38
START_PAGE = 1

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

all_data = []
headers = []

def get_page_url(page_num):
    return f"https://evaluare.edu.ro/Evaluare/CandFromJudAlfa.aspx?Jud={JUD_CODE}&PageN={page_num}"

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

page_num = START_PAGE
while True:
    url = get_page_url(page_num)
    print(f"🔄 Loading page {page_num}: {url}")
    driver.get(url)
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", class_="mainTable")

    if not table:
        print(f"❌ No data found on page {page_num}. Stopping.")
        break

    if not headers:
        headers = extract_headers(table)

    rows_found = False
    for row in table.find_all("tr")[2:]:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols:
            all_data.append(cols)
            rows_found = True

    if not rows_found:
        print(f"✅ No rows on page {page_num}. Done.")
        break

    page_num += 1

driver.quit()

# Save to CSV
df = pd.DataFrame(all_data, columns=headers)
filename = f"evaluare_jud{JUD_CODE}_all_pages.csv"
df.to_csv(filename, index=False, encoding="utf-8-sig")
print(f"✅ Finished! Data saved to '{filename}' with {len(all_data)} rows from {page_num - 1} pages.")
