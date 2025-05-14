from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
service = Service(ChromeDriverManager("133.0.6943.127").install())
# Amazon URL (Change this to the product page you want to scrape)
AMAZON_URL = "https://www.amazon.com/Nike-Sportswear-Fleece-Windrunner-Full-Zip/dp/B0C4PH51YL/ref=sr_1_1?crid=244ODAGGL3Q75&dib=eyJ2IjoiMSJ9.FViZ-Qov5JivjPjgxv6ZUVDCGL_i_GFpcXBeTr7nTB7npDyIcKgQndjsvXUq3VuKkl71Xjsb4SgouX7zWJaMBVjO_6DnF6HSgrLPgb17cvKKscJvMgUK83HpXxcqgyXB0UOEPgSdae3vrX285TIRKRpjoFNb4sOg-q9TIctPcgVNzOAHviaCQGAioOymBt-FDxS6vlcCIrSzkWcbnxMbrJ0BcNb98yNSH8X3oyWpSdw-7CouEYPUNIPqvzYQSLjLYBENvJBqm9QRxM5tjnHF2OnP2W3ALsDOLa-wyZfvzXgU9u8bH86pe-ygHchJmTYlRj7HS8xszZJAkyCylq4iYvmzjn7cndLNcGNiQEZ_9bCiwMFv_C6owzlJcy16y5TyvLmVv5ONn_Sy6IJ6M-VnV520fmfq7HAwB96ukcF6I47H4n8zs0K9eqPlef9e0yW4.JQEOpIqS14f1XhE79xL9ymz1yTdLxXJyYhODFwW4Gwo&dib_tag=se&keywords=nike%2Btech&qid=1740000636&sprefix=nike%2Btech%2Caps%2C104&sr=8-1&th=1&psc=1"  # Example URL


def get_amazon_price(url):
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
    options.add_argument("start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        # Wait until the price element is loaded
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        price_element = wait.until(EC.presence_of_element_located((By.ID, "priceblock_ourprice")))

        price = price_element.text
        print(f"Amazon Price: {price}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()  # Ensure the browser is closed


# Run the scraper
get_amazon_price(AMAZON_URL)

