from autoscab.constants.locators import ApplicationLocator
from autoscab.constants.location import get_search_url
from autoscab.postbot import PostBot

url = get_search_url()

bot = PostBot(url, locator_dict=dict(ApplicationLocator.__dict__), headless=False)