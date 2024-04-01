import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import Select
from datetime import datetime




def get_name(standard_symbol):
    driver.get("https://www.11meigui.com/tools/currency")

    symbol = driver.find_element(By.XPATH, f"//td[contains(text(), '{standard_symbol}')]")
    parent_row = symbol.find_element(By.XPATH, "./..")
    chinese_text = parent_row.find_element(By.XPATH, "./td[2]").text

    return chinese_text

def format_date(date_string):
    date_obj = datetime.strptime(date_string, '%Y%m%d')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date



def get_price(date, standard_symbol):

    name = get_name(standard_symbol)
    formatted_input_date = format_date(date)

    driver.get("https://srh.bankofchina.com/search/whpj/search_cn.jsp")


    date_input = driver.find_element(By.XPATH, "/html/body/div[1]/form[1]/div/table/tbody/tr/td[2]/div/input")
    date_input.clear()
    date_input.send_keys(formatted_input_date)

    currency_select = Select(driver.find_element(By.XPATH, '//*[@id="pjname"]'))
    currency_select.select_by_visible_text(name)

    search_button = driver.find_element(By.XPATH, "/html/body/div/form[1]/div/table/tbody/tr/td[7]/input")
    search_button.click()

    symbol = driver.find_element(By.XPATH, f"//td[contains(text(), '{name}')]")
    parent_row = symbol.find_element(By.XPATH, "./..")
    sell_value = parent_row.find_element(By.XPATH, "./td[4]").text

    # return sell_value
    with open("result.txt", "w") as file:
        file.write(f"Price for {standard_symbol} on {formatted_input_date}: {sell_value}\n")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 yourcode.py <date> <standard_symbol>")
        sys.exit(1)
    
    input_date = sys.argv[1]
    input_standard_symbol = sys.argv[2]

    # firefox_options = webdriver.FirefoxOptions()
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    get_price(input_date, input_standard_symbol)
    driver.quit()

