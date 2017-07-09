from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

import time

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=r'd:\Users\Z&B\PycharmProjects\geckodriver.exe')
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it(self):

        # check homepage address
        self.browser.get('http://localhost:8000')
        # check page title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # invitation to enter to-do item in text box
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # entered 'Buy peacock feathers' into text box
        inputbox.send_keys('Buy peacock feathers')

        # page updates on ENTER
        inputbox.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(1)
       # time.sleep(10)

        # now page lists '1. Buy peacock feathers'
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

        # there is still invitation to enter next to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        # entered 'Use peacock feathers to make a fly'
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(1)
        # page updates and shows two items
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])
        # this list have unique URL to be accessed later
        # check this URL
        self.fail('Finish the test')
if __name__ == '__main__':
    unittest.main()