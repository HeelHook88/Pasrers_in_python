from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class mail_ru_parser():

    def __init__(self, login, password, mongoClient):
        self.IsEnd = False
        self.mailIdCurrent = 'A'
        self.mailIdLast = 'B'
        self._login = login
        self._password = password
        self.driver = webdriver.Chrome()
        self.driver.get('https://mail.ru/')
        assert "Mail.ru:" in self.driver.title

        self.client = mongoClient
        self.db = self.client['MailsDB']
        self.db_mails = self.db.mails
        self.mails = []

        self._driver_login_element = 'mailbox:login'
        self._driver_password_element = 'mailbox:password'

        self._driver_submit_element = 'mailbox:submit'
        self._driver_navigate_folder_element = 'nav__folder'

        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        elem = self.driver.find_element_by_id(self._driver_login_element)
        elem.send_keys(self._login)  # 'study.ai_172@mail.ru'

        elem = self.driver.find_element_by_id(self._driver_submit_element)
        elem.click()

        elem = self.wait.until(EC.element_to_be_clickable((By.ID, self._driver_password_element)))

        elem = self.driver.find_element_by_id(self._driver_password_element)
        elem.send_keys(self._password)  # 'NewPassword172'

        elem = self.driver.find_element_by_id(self._driver_submit_element)
        elem.click()

        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, self._driver_navigate_folder_element)))

        self.mover()

    def mover(self):

        action = ActionChains(self.driver)
        action.key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).perform()
        action.key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()
        window = self.driver.window_handles
        self.driver.switch_to.window(window[1])

        self.mailIdLast = self.mailIdCurrent

    def mail_parser(self):
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, self._driver_navigate_folder_element)))
        self.mailIdCurrent = self.driver.find_element_by_xpath("//div[@data-id]").get_attribute('data-id')
        mail_elems = {}

        mail_elems['From'] = self.driver.find_element_by_xpath("//span[@class='letter-contact']").get_attribute('title')
        mail_elems['Time'] = self.driver.find_element_by_xpath("//div[@class='letter__date']").text
        mail_elems['Text'] = self.driver.find_element_by_xpath("//h2[@class='thread__subject thread__subject_pony-mode']").text
        full_text = self.driver.find_elements_by_xpath("//td[@align='left']/span |//tr[@align='left']/td |//td/p |//div/p")

        result = []
        for x in full_text:
            temp = x.text + '\n'
            result.append(temp)

        mail_elems['Full_text'] = result

        self.driver.close()
        self.mails.append(mail_elems)
        window = self.driver.window_handles
        self.driver.switch_to.window(window[0])

        if self.mailIdCurrent is self.mailIdLast:
            self.IsEnd = True

        return self.mails, self.mailIdCurrent

    def add_to_db(self):
        self.db_mails.insert_one(self.mail)

