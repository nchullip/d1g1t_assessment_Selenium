# d1g1t_assessment_Selenium
This contains solution to d1g1t assessment on Selenium

### Problem Statement
* Go to this URL - https://store.steampowered.com/
* Print the Game Names from the Top Seller Section on the Console
* From that section, categorize the games into: Free to Play, On Sale, Regular Price
* Print the name of the games in the alphabetical order in a CSV file with four attributes (name, release date, price and category)

### Required Python Packages
* pandas
* csv
* os
* selenium

### Solution
* All the locators are saved in the file ***locators.py***
* Run the file ***main.py***
* The script navigates to the website (store.steampowered.com) and traverses through each game in the Top Seller section collecting all relevant information.
* The script prints the name of the game on the console. This is **NOT** arranged alphabetically.
* The games are arranged alphabetically and stored in the output file (***sorted_output.csv***) with the attributes **Name, Release Date, Category, Price**
* Please Note, in the Output file, data in the Name is encoded and displayed.

