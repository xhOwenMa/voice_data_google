import os
import sys
sys.path.append(os.path.join(os.getcwd(), "../"))
from profile.query_bot import *

bot = WebSearchBot()
# time.sleep(30)  # Allow time for manual sign in
bot.switch_to_new_window()  # switch to the new signed in window

queries = read_queries_from_file('male_queries.txt')
for query in queries:
    print(f"Processing query: '{query}'")
    bot.perform_google_search(query)

    # links = bot.driver.find_elements(By.XPATH, "//a[@jsname='UWckNb']")
    # Wait for links to be present and retrieve them
    links_xpath = "//a[@jsname='UWckNb']"
    links = bot.wait_for_links_and_get_them(links_xpath)
    print(f"found {len(links)} links")

    bot.process_links(links)

    # counter = 0
    # for link in links:
    #     counter = bot.process_link(link, counter)
    #     print(counter)
    #     if counter > 2:
    #         break

bot.quit()



