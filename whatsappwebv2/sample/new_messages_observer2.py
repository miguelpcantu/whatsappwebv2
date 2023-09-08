import os
import sys
import time

from webwhatsapi import WhatsAPIDriver


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath("__file__"))))
sys.path.insert(0, BASE_DIR)

from flask import Flask, send_file, request, abort, g, jsonify
from flask.json import JSONEncoder
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from selenium.common.exceptions import WebDriverException
from werkzeug.utils import secure_filename
from webwhatsapi import MessageGroup, WhatsAPIDriver, WhatsAPIDriverStatus
from webwhatsapi.objects.whatsapp_object import WhatsappObject
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import chromedriver_binary


CHROME_IS_HEADLESS = True
CHROME_CACHE_PATH = BASE_DIR + "/sample/flask/chrome_cache/"
CHROME_DISABLE_GPU = True
CHROME_WINDOW_SIZE = "910,512"

profile_path = CHROME_CACHE_PATH + str("remote")
if not os.path.exists(profile_path):
    os.makedirs(profile_path)


chrome_options = [
    "window-size=" + CHROME_WINDOW_SIZE,
    "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36",
]


def run():
#    print("Environment", os.environ)
#    try:
#        os.environ["SELENIUM"]
#    except KeyError:
#        print("Please set the environment variable SELENIUM to Selenium URL")
#        sys.exit(1)

#    driver = WhatsAPIDriver(client="remote", command_executor=os.environ["SELENIUM"])
    driver = WhatsAPIDriver(
        username="remote",
        profile=profile_path,
        client="chrome",
        chrome_options=chrome_options
    )
#    return driver



    print("Waiting for QR")
    driver.wait_for_login()
    print("Bot started")

    driver.subscribe_new_messages(NewMessageObserver())
    print("Waiting for new messages...")

    """ Locks the main thread while the subscription in running """
    while True:
        time.sleep(60)


class NewMessageObserver:
    def on_message_received(self, new_messages):
        for message in new_messages:
            if message.type == "chat":
                print(
                    "New message '{}' received from number {}".format(
                        message.content, message.sender.id
                    )
                )
            else:
                print(
                    "New message of type '{}' received from number {}".format(
                        message.type, message.sender.id
                    )
                )


if __name__ == "__main__":
    run()
