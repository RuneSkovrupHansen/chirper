import datetime
import os
import sys
import time
import logging
import random
import re
import configparser
from datetime import  datetime
from datetime import timedelta

from twilio.rest import Client

class Component:

    """Load a list of strings to be used as a component of a template
    
    The get() method returns a random string from the list
    """

    def __init__(self, file=None, list=[]) -> None:
        
        if file and list:
            logging.warning("__init__(), both file and list specified, file takes precedence")

        if file and self.load_file(file):
            return

        self.list = list

    def load_file(self, file) -> bool:

        if not os.path.exists(file):
            logging.warning(f"load_file(), file does not exist, file: {file}")
            return False

        with open(file) as f:
            self.list = f.read().splitlines()

        return True

    def get(self) -> str:

        if not self.list:
            logging.warning("get(), list is empty")
            return ""

        return random.choice(self.list)


class Template(Component):

    """Load a list of strings to be used as templates

    substitutes is a dict containing key-value pairs of
    placeholder strings and components from which to get their
    replacement
    
    The get() method returns a random template string with 
    replaced placeholders
    """

    def __init__(self, substitutes, file=None, list=[]) -> None:
        super().__init__(file=file, list=list)

        self.substitutes: dict = substitutes
        
    def get(self) -> str:
        
        # Initialize template
        template = super().get()

        # Check for substitutes
        if not self.substitutes:
            return template

        # Replace all substitutions 
        for key, component in self.substitutes.items():

            # Find all occurences of key in the template
            matches = list(re.finditer(key, template))

            # Reverse list to preserve indices when iterating through it
            matches.reverse()

            # Replace all matches of the key with a component item
            for match in matches:

                # Fix replacement capitalization
                replacement = component.get()
                if match.start() == 0 or template[match.start()-1] in [".", ":", "!", "?"]:
                    replacement = replacement.capitalize()

                template = template[:match.start()] + replacement + template[match.end():]

        return template


class Chirper:

    def __init__(self, account_sid, auth_token, service_sid, recepient, templates) -> None:

        self.client = Client(account_sid, auth_token)
        self.service_sid = service_sid
        self.recipient = recepient
        self.templates: Template = templates


    def _send(self, message):

        """Send message to recipient"""

        message = self.client.messages.create(
            messaging_service_sid=self.service_sid,
            body=message,
            to=self.recipient
        )


    def chirp(self):

        """Send random template message"""

        message = self.templates.get()
        self._send(message)


    def interval_chirp(self, earliest_hour, latest_hour):

        """Call chirp at a random time in a specified interval once per day"""

        # Check if chirp can be sent today
        current = datetime.now()

        # Get random time in interval
        hour = random.randint(earliest_hour, latest_hour)
        minute = random.randint(0, 59)

        target = datetime(current.year, current.month, current.day, hour, minute)

        if (target-current).total_seconds() > 0:
            sleep_until_datetime(target)
            self.chirp()

        while True:

            # Get random time in interval
            hour = random.randint(earliest_hour, latest_hour)
            minute = random.randint(0, 59)

            target = datetime(target.year, target.month, target.day, hour, minute) + timedelta(days=1)

            sleep_until_datetime(target)
            self.chirp()


def sleep_until_datetime(target: datetime):

    """Sleep until datetime"""

    current = datetime.now()
    difference = (target-current).total_seconds()

    logging.info(f"interval_chirp(), sleeping until {target}")

    if difference > 0:
        time.sleep(difference)


def load_config(file="config.ini"):

    """Load configuration file"""

    if not os.path.exists(file):
        logging.warning("load_config(), could not load config")
        return None

    config = configparser.ConfigParser()
    config.read(file)

    return config


def main():
    # Configure logging
    logging.basicConfig(format='[ %(levelname)s ] F: %(module)s L: %(lineno)d M: %(message)s', level=logging.INFO, stream=sys.stdout)

    # Set Twilio logging level
    twilio_logger = logging.getLogger('twilio.http_client')
    twilio_logger.setLevel(logging.WARNING)

    # Load components
    adjectives = Component("data/adjectives.txt")
    nicknames = Component("data/nicknames.txt")
    appearance = Component("data/appearance.txt")
    food = Component("data/food.txt")

    # Build substitute dict
    substitues = {
        "<adjective>":adjectives,
        "<nickname>":nicknames,
        "<appearance>":appearance,
        "<food>":food
    }

    # Load templates
    templates = Template(substitues, "data/templates.txt")

    # Check environment variables
    for key in ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_SERVICE_SID"]:
        if not key in os.environ:
            print(f"main(), unable to find {key} in environment")
            return

    # Load environment variables
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    service_id = os.environ["TWILIO_SERVICE_SID"]

    # Check config
    config = load_config()
    if not config:
        logging.error("main(), unable to load config, did you run create_config.sh?")
        return

    # Load recipient and time from config
    recipient = config.get("chirper", "recipient")
    earliest_hour = config.getint("chirper", "earliest_hour") # The earliest hour to chirp
    latest_hour = config.getint("chirper", "latest_hour") # The latest hour to chirp

    # Check recipient
    if not recipient:
        logging.error("main(), recipient empty, did you overwrite default in config.ini?")
        return

    if earliest_hour > latest_hour:
        logging.error("main(), latest hour is earlier than earliest hour")
        return

    # Initialize Chirper
    chirper = Chirper(account_sid, auth_token, service_id, recipient, templates)

    # Start interval chirp
    chirper.interval_chirp(earliest_hour, latest_hour)


if __name__ == "__main__":
    main()
