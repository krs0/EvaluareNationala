from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # optional: run in background
driver = webdriver.Chrome(options=options)

driver.get("https://www.google.com")
print("Page title:", driver.title)

driver.quit()