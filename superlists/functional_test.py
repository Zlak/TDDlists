from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=r'd:\Users\Z&B\PycharmProjects\geckodriver.exe')
        #self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it(self):

        #check homepage address
        self.browser.get('http://localhost:8000')
        #check page title
        self.assertIn('To-Do',self.browser.title)
        self.fail('Finish the test')
        #invitation to enter to-do item in text box

        #entered 'Buy peacock feathers' into text box

        #page updates on ENTER

        #now page lists '1. Buy peacock feathers'

        #there is still invitation to enter next to-do item

        #entered 'Use peacock feathers to nake a fly'
        #page updates and shows two items

        #this list have unique URL to be accessed later
        #check this URL

if __name__ == '__main__':
    unittest.main()