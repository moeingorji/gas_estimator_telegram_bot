import time

import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio

from selenium.webdriver.common.by import By


async def check_gas_value():
    # Set up Selenium options
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')

    # Load page with Selenium and wait for it to fully load
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.blocknative.com/gas-estimator')
    time.sleep(1)  # Wait for page to fully load with JavaScript executing

    # Extract gas value from page
    gas_value_str = driver.find_element(By.CSS_SELECTOR,'.gas-info-heading.base-fee-value.primary-text-gradient').text.strip()
    gas_value = float(gas_value_str.split()[0])

    # Check if gas value is below 25 and send message to Telegram channel
    if gas_value < 25:
        bot = telegram.Bot(token='xxx')
        chat_id = '@Cxxxx'
        message = f"Gas value is below 25: {gas_value}"
        await bot.send_message(chat_id=chat_id, text=message)

    driver.quit()


async def main():
    while True:
        await check_gas_value()
        await asyncio.sleep(300)  # Wait for 5 minutes


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
