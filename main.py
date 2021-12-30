######################################################################################
# 1. Go to this URL - https://store.steampowered.com/
# 2. Print the Game Names from the Top Seller Section on the Console
# 3. From that section, categorize the games into: Free to Play, On Sale, Regular Price
# 4. Print the name of the games in the alphabetical order in a CSV file with four
#    attributes (name, release date, price and category)
######################################################################################

# Importing Dependencies
import csv
import os
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from locators import top_seller_xpath, game_name_xpath, game_release_date, discount_xpath, no_discount_xpath, \
    view_page_btn_xpath, year_drp_dwn_xpath


def main():
    category = "Null"
    flag = "N"
    game_dict = {}
    game_list = []

    # Creating the Output file
    if os.path.isfile('sorted_output.csv'):
        os.remove('sorted_output.csv')
    f = open('output.csv', 'w', newline="")
    writer = csv.writer(f)
    writer.writerow(["Name", "Release Date", "Category", "Price"])
    f.close()

    # Step 1: Create the driver object and the Webdriver Wait Object
    driver = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(driver, 10)

    # Step 2: Navigate to the URL and maximize window
    driver.get("https://store.steampowered.com/")
    driver.maximize_window()

    # Step 3: Get all Top Seller Games
    top_seller_games = driver.find_elements(By.XPATH, top_seller_xpath)

    # Step 4: Traversing  through each game in Top Seller section
    print("Top Seller Games")
    print("===================")
    for i in range(len(top_seller_games)):
        game_name = ""
        release_date = ""
        price = ""
        category = ""
        game = top_seller_xpath + "[" + str(i + 1) + "]"
        temp_ele = wait.until(EC.presence_of_element_located((By.XPATH, game)))
        disc_price = driver.find_elements(By.XPATH, game + discount_xpath)
        if len(disc_price) == 2:
            category = "On Sale"
            price = driver.find_element(By.XPATH, game + discount_xpath + "/div[2]").text
        elif len(disc_price) == 1:
            price_el = driver.find_element(By.XPATH, game + discount_xpath + "/div")
            price = price_el.text
            if "Free to Play" in price:
                game_ele = driver.find_element(By.XPATH, game)
                try:
                    disc = game_ele.find_element(By.XPATH, no_discount_xpath)
                    category = "Regular Price"
                except NoSuchElementException:
                    category = "Free to Play"
            else:
                category = "Regular Price"
        driver.find_element(By.XPATH, game).click()
        try:
            # Code to accept notification for Adult Games
            driver.find_element(By.XPATH, year_drp_dwn_xpath)
            select = Select(driver.find_element(By.XPATH, year_drp_dwn_xpath))
            select.select_by_value('1991')
            driver.find_element(By.XPATH, view_page_btn_xpath).click()
            flag = "Y"
            sleep(2)
        except NoSuchElementException:
            pass
        element = wait.until(EC.presence_of_element_located((By.XPATH, game_name_xpath)))
        game_name = element.text
        release_date = driver.find_element(By.XPATH, game_release_date).text

        # Print Name of Game on the Console
        print(str(i + 1) + ". " + game_name)

        # Append the Game information to the Output File
        with open('output.csv', 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([game_name, release_date, category, price])
        file.close()

        # Code to go back to the Main Page
        if flag == "N":
            driver.back()
        else:
            driver.back()
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Realistic")))
            driver.back()
            flag = "N"

    # Pandas Code to rearrange Dataframe alphabetically
    df = pd.read_csv('output.csv', delimiter=",", encoding="ISO-8859-1")
    sorted_df = df.sort_values("Name")
    sorted_df.to_csv('sorted_output.csv', index=False)
    os.remove("output.csv")


if __name__ == "__main__":
    main()
