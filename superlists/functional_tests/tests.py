from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=r'..\..\geckodriver.exe')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it(self):

        # check homepage address
        self.browser.get(self.live_server_url)
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
        time.sleep(3)
        # now page lists '1. Buy peacock feathers'
        # this list have unique URL to be accessed later
        alice_list_url = self.browser.current_url
        self.assertRegex(alice_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # there is still invitation to enter next to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        # entered 'Use peacock feathers to make a fly'
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        # page updates and shows two items
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # new browser session for new client (to make sure no info on previous user left)
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path=r'..\..\geckodriver.exe')
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        #Bob (new user) starts new list by entering new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        #Bob get own unique list URL
        bob_list_url = self.browser.current_url
        self.assertRegex(bob_list_url, '/lists/.+')
        self.assertNotEqual(bob_list_url, alice_list_url)

        #checking that alice list not here
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        self.assertNotIn('Buy peacock feathers')
        self.fail('Finish the test')
