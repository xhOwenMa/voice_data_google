import time
import random
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# test


def initialize_driver():
    chromedriver_path = '/Users/owenma/Desktop/527final/chromedriver'
    service = webdriver.chrome.service.Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    # Loading profile
    # options.add_argument('user-data-dir=/Users/owenma/Library/Application Support/Google/Chrome')
    # options.add_argument('profile-directory=Profile 4')
    options.add_argument('--disable-extensions')
    # Adding argument to disable the AutomationControlled flag
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Exclude the collection of enable-automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Turn-off userAutomationExtension
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1400, 750)
    driver.set_page_load_timeout(10)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


class WebSearchBot:
    def __init__(self):
        self.driver = initialize_driver()

    def perform_google_search(self, query):
        self.driver.get("http://www.google.com")
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        time.sleep(1)
        search_box.submit()
        # time.sleep(3)

    def wait_for_links_and_get_them(self, xpath, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
            return self.driver.find_elements(By.XPATH, xpath)
        except TimeoutException:
            print(f"Timeout waiting for links to load.")
            return []

    def scroll_page_randomly(self, times=10):
        for _ in range(times):
            scroll_amount = random.randint(150, 250)
            time_interval = random.uniform(0.3, 0.4)
            self.driver.execute_script(f"window.scrollBy(0,{scroll_amount})", "")
            time.sleep(time_interval)

    def handle_cookie_consent(self):
        try:
            cookie_consent = self.driver.find_element(By.XPATH, "//a[@role='button']")
            if "accept" in cookie_consent.text.lower():
                print("cookie consent accepted")
                cookie_consent.click()
                time.sleep(2)
        except:
            print("no cookie consent found")

    def open_link_in_new_tab(self, url):
        # Open the link in a new tab
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(1)

        # Switch to the new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_current_tab(self):
        # Close the current tab
        self.driver.close()

        # Switch back to the first tab
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(2)

    def process_link(self, link, counter):
        try:
            url = link.get_attribute("href")
            print(urlparse(url).netloc)
            try:
                self.open_link_in_new_tab(url)

                # Perform necessary actions in the new tab
                self.scroll_page_randomly()
                self.handle_cookie_consent()

                # Close the new tab and switch back to the original tab
                self.close_current_tab()
                counter += 1
            except TimeoutException:
                print(f"Timeout occurred for {url}")
            finally:
                time.sleep(1)
        except:
            print(f"failed to get url from anchor")
        finally:
            return counter

    def switch_to_new_window(self):
        # Get a list of all open windows
        all_windows = self.driver.window_handles

        # Switch to the new window (assuming it is the last one opened)
        if len(all_windows) > 1:
            new_window = all_windows[-1]
            self.driver.switch_to.window(new_window)
            print("Switched to the new window.")
        else:
            print("No new window found.")

    def quit(self):
        self.driver.quit()


def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()


def main():
    bot = WebSearchBot()
    # time.sleep(30)  # Allow time for manual sign in
    bot.switch_to_new_window()  # switch to the new signed in window

    queries = read_queries_from_file('queries.txt')
    for query in queries:
        print(f"Processing query: '{query}'")
        bot.perform_google_search(query)

        # links = bot.driver.find_elements(By.XPATH, "//a[@jsname='UWckNb']")
        # Wait for links to be present and retrieve them
        links_xpath = "//a[@jsname='UWckNb']"
        links = bot.wait_for_links_and_get_them(links_xpath)
        print(f"found {len(links)} links")

        counter = 0
        for link in links:
            counter = bot.process_link(link, counter)
            print(counter)
            if counter > 2:
                break

    bot.quit()


if __name__ == "__main__":
    main()
