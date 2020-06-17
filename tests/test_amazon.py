from selenium import webdriver
import unittest, os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

'''
Selenium WebDriver with Python exercise
1. Go to www.amazon.com
2. Enter 'ipad air 2 case' into the search box
3. Click on search button
4. Under Case Material, filter 'Plastic'
5. Narrow search to $20 - $100 range and click 'Go'
6. Extract the first five items
7. Sort items by price and print result
'''


class SearchAmazonTest(unittest.TestCase):
    def setUp(self):
        global options
        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        chrome_path = os.path.join(project_path, 'drivers/chromedriver')
        self.driver = webdriver.Chrome(options=options, executable_path=chrome_path)
        self.driver.implicitly_wait(2)
        self.driver.delete_all_cookies()
        self.driver.maximize_window()

    def test_search_amazon(self):
        # Step 1: Go to www.amazon.com
        self.driver.get('https://www.amazon.com/')

        # Step 2: Search for 'ipad air 2 case' into the search box
        self.driver.find_element(By.ID, 'twotabsearchtextbox').send_keys('ipad air 2 case')

        # Step 3: Click on search button
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Step 4: Under Case Material, filter 'Plastic'
        self.driver.execute_script("window.scrollTo(0, 800)")
        self.driver.find_element(By.XPATH,
                                 '//div[@id="filters"]/ul[4]/li[@aria-label="Plastic"]//i').click()

        # Step 5: Narrow search to $20 - $100 range and click 'Go'
        self.driver.find_element(By.ID, 'low-price').send_keys('20')
        self.driver.find_element(By.ID, 'high-price').send_keys('100')
        self.driver.find_element(By.XPATH, '//span[@id="a-autoid-1-announce"]//preceding-sibling::input').click()

        # Step 6: Extract the first five items and store name/price in dict 'result'
        result = {}
        for i in range(1, 6):
            product = self.driver.find_element(
                By.XPATH,
                '//div[@data-index="{}"]//div[2]/h2/a/span'.format(i)).text
            try:
                dollars = self.driver.find_element(
                    By.XPATH,
                    '//div[@data-index="{}"]//div[4]/div[2]/div/a//span[@class="a-price-whole"]'.format(i)).text
                cents = self.driver.find_element(
                    By.XPATH,
                    '//div[@data-index="{}"]//div[4]/div[2]/div/a//span[@class="a-price-fraction"]'.format(i)).text
                price = float('%d.%d' % (int(dollars), int(cents)))
            # If there is no price displayed in the results, click on the product and retrieve the first available
            # price under 'New and Used'
            except NoSuchElementException:
                self.driver.find_element(By.XPATH, '//div[@data-index="{}"]//div[2]//a'.format(i)).click()
                price = self.driver.find_element(By.XPATH, '//span[@class="a-color-price"]').text
                price = float(price[1:])
                self.driver.back()
            result[product] = price

        # Step 7: Sort items by price and print result
        sorted_result = sorted(result.items(), key=lambda x: x[1])
        for k in sorted_result:
            print('Product {}: {}'.format(((list(sorted_result).index(k)) + 1), k[0]))
            print('Price: ${}\n'.format(k[1]))

        # # Step 8: Sort items by name and print result
        # sorted_result = {k: result[k] for k in sorted(result)}
        # for k in sorted_result:
        #     print('Product {}: {}'.format(((list(sorted_result).index(k)) + 1), k))
        #     print('Price: ${}\n'.format(sorted_result[k]))

    def tearDown(self):
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
