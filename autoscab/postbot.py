import time
import typing
import traceback
import random
from pathlib import Path

import requests
from faker import Faker

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils import random_email
from resume_faker import make_resume


class PostBot(object):

    def __init__(self, url:str, locator_dict:dict, headless:bool=True):
        self.locator_dictionary = dict(locator_dict)
        self.options = Options()
        # self.options.binary_location = '/usr/bin/google-chrome'
        #self.options.add_argument("start-maximized"); #// open Browser in maximized mode
        self.options.add_argument("disable-infobars") #// disabling infobars
        #self.options.add_argument("--disable-extensions"); #// disabling extensions
        #self.options.add_argument("--disable-gpu"); #// applicable to windows os only
        self.options.add_argument("--disable-dev-shm-usage") #// overcome limited resource problems
        self.options.add_argument("--no-sandbox") #// Bypass OS security model
        if headless:
            self.options.add_argument("--headless")
        # twitter's shit is too responsive and hides tweet box when window is small
        self.options.add_argument("--window-size=1920,1080")
        # debugging DevToolsActivePort file doesn't exist
        #self.options.add_argument("--disable-gpu")

        self.url = url
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)  # export PATH=$PATH:/path/to/chromedriver/folder
        self.timeout = 5
        self.browser.get(self.url)


        self.faker = Faker()
        self.fake_name = ['',''] # type: typing.List[str,str]
        self.fake_email = ''
        self.mail_sid = ''
        self.password = ''
        self.resume_path = Path() # type: Path
        self.new_fake_name()
        self.new_fake_email()
        self.new_fake_password()
        self.new_fake_resume()

    def apply(self):
        self.choose_position()
        self.make_account()


    def choose_position(self):
        self.positions.click()
        time.sleep(2)
        # stash current window handle
        current_window = self.browser.current_window_handle
        self.apply_button.click()
        time.sleep(5)
        # this opens a new tab.
        for handle in self.browser.window_handles:
            if handle != current_window:
                self.browser.switch_to.window(handle)
                break


    def make_account(self):
        self.new_account.click()
        self.random_sleep(3,5)
        self.newacct_email.send_keys(self.fake_email)
        self.random_sleep()
        self.newacct_email_conf.send_keys(self.fake_email)
        self.random_sleep()
        self.newacct_pass.send_keys(self.password)
        self.random_sleep()
        self.newacct_pass_conf.send_keys(self.password)
        self.random_sleep()
        self.newacct_first.send_keys(self.fake_name[0])
        self.random_sleep()
        self.newacct_last.send_keys(self.fake_name[1])
        self.random_sleep()
        self.newacct_us.click()
        self.random_sleep()
        self.newacct_privacy.click()
        self.random_sleep()
        self.newacct_privacy_accept.click()
        self.random_sleep()
        self.newacct_create.click()

    def random_sleep(self, min=0.5, max=2):
        time.sleep(random.random()*(max-min)+min)

    def new_fake_name(self):
        self.fake_name = [self.faker.first_name(), self.faker.last_name()]

    def new_fake_email(self, service:typing.Literal['guerilla', 'mailtm']='guerilla'):
        if service == 'guerilla':
            response = requests.get('https://api.guerrillamail.com/ajax.php?f=get_email_address').json()
            fake_email = response.get('email_addr')
            mail_sid = response.get('sid_token')
        elif service == 'mailtm':
            fake_email = requests.post('https://api.mail.tm/accounts', data='{"address":"' + random_email(
                self.fake_name[0] + ' ' + self.fake_name[1]) + '","password":" "}',
                                       headers={'Content-Type': 'application/json'}).json().get('address')
            mail_sid = requests.post('https://api.mail.tm/token',
                                     data='{"address":"' + fake_email + '","password":" "}',
                                     headers={'Content-Type': 'application/json'}).json().get('token')
        else:
            raise ValueError('Dont know what email service to use! try one of guerilla or mailtm')
        self.fake_email = fake_email
        self.mail_sid = mail_sid

    def new_fake_password(self):
        self.password = self.faker.password()

    def new_fake_resume(self):
        self.resume_path = make_resume(
            name = " ".join(self.fake_name),
            email = self.fake_email
        )

    #
    # def login(self, username=Constants.USERNAME, password=Constants.PASSWORD):
    #     self.login_btn.click()
    #     time.sleep(1)
    #     self.username.click()
    #     time.sleep(0.1)
    #     self.username.send_keys(username)
    #     time.sleep(0.1)
    #     self.password.click()
    #     time.sleep(0.1)
    #     self.password.send_keys(password)
    #     time.sleep(0.1)
    #     self.browser.find_elements_by_css_selector(".clearfix>.submit")[0].click()
    #     time.sleep(0.5)
    #     self.browser.get(URL.TWITTER_HOME)
    #     time.sleep(0.5)
    #
    # def tweet_poll(self, post_text):
    #
    #     # click the tweet box
    #     self.outer_tweet_box.click()
    #     time.sleep(1)
    #
    #     # type the tweet
    #     self.tweet_box.send_keys('\"' + post_text.lower() + '\" uohellno.com')
    #     time.sleep(1)
    #
    #     # make the poll
    #     self.poll_btn.click()
    #     time.sleep(0.1)
    #     self.option_one.click()
    #     time.sleep(0.1)
    #     self.option_one.send_keys('human schill')
    #     time.sleep(0.1)
    #     self.option_two.click()
    #     time.sleep(0.1)
    #     self.option_two.send_keys('robot schill')
    #     time.sleep(0.2)
    #
    #     # send the tweet
    #     self.tweet_btn.click()
    #     time.sleep(2)
    #
    # def search(self, q=Constants.GLOBAL_ENTRY_Q):
    #     self.search_input.send_keys(q)
    #     self.search_input.send_keys(Keys.ENTER)
    #
    # def view_latest_tweets(self):
    #     self.latest_tweets.click()
    #
    # def like_tweet(self):
    #     tweets = self.browser.find_elements(*self.locator_dictionary['tweets'])
    #     tweet = random.choice(tweets)
    #     like = tweet.find_element(*self.locator_dictionary['like_btn'])
    #     like.click()
    #     print("Liked Tweet: {}".format(tweet.text))

    def _find_element(self, *loc):
        return self.browser.find_element(*loc)

    def __getattr__(self, what):
        try:
            if what in self.locator_dictionary.keys():
                try:
                    element = WebDriverWait(self.browser, self.timeout).until(
                        EC.presence_of_element_located(self.locator_dictionary[what])
                    )
                except(TimeoutException, StaleElementReferenceException):
                    traceback.print_exc()

                try:
                    element = WebDriverWait(self.browser, self.timeout).until(
                        EC.visibility_of_element_located(self.locator_dictionary[what])
                    )
                except(TimeoutException, StaleElementReferenceException):
                    traceback.print_exc()
                # I could have returned element, however because of lazy loading, I am seeking the element before return
                return self._find_element(*self.locator_dictionary[what])
        except AttributeError:
            super(PostBot, self).__getattribute__("method_missing")(what)


    # def run(self, post_text):
    #     self.login()
    #     self.tweet_poll(post_text)
    #     self.browser.quit()