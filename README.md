# Chirper
Repository for Chirper - a complimentary experiment with Python and Twilio

Chirper is a fun experiment designed to try and send compliments via sms using Python and Twilio. Compliments are generated from templates with the option to specify placeholder values which can be randomly filled in from a specified list. Example:

Hey, I think that you're \<adjective\>.

Where \<adjective\> would be filled in with a random adjective from a specified list.

As mentioned above, this is just a fun experiment, there are many possible improvements which could still be made.

### Setup

Install Python requirements using command ``pip install -r requirements.txt``

To use Chirper a Twilio account is required, learn more about Twilio in the section below. Chirper requires *ACCOUNT SID*, *AUTH TOKEN*, and a *SERVICE SID*.

Twilio recommends using environment variables to store secrets such as auth tokens. Check out [this article](https://www.twilio.com/blog/protect-phishing-auth-token-fraud) for best practices. The example in chirper.py main() expects variables to be stored using the following keys: *TWILIO_ACCOUNT_SID*, *TWILIO_AUTH_TOKEN*, *TWILIO_SERVICE_SID*.

Check out [this article](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) on how to store environment variables, and if you're on linux you can also check out [this article](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/) from Linuxize.

The example in chirper.py main() also expects a config file containing, config.ini. To create a default config file run create_config.sh.

### Twilio

Twilio is a cloud communications platform as a service. Twilio allows software developers to programmatically make and receive phone calls, send and receive text messages, and perform other communication functions using its web service APIs.

To learn more about Twilio go to [their website](https://www.twilio.com/).

### Data

Adjectives in 'adjectives.csv' gathered from [grammar.yourdictionary.com](https://grammar.yourdictionary.com/parts-of-speech/adjectives/list-of-positive-adjectives.html).

Some of the plain compliments without placeholders in 'templates.txt' gathered from [https://www.verywellmind.com/](https://www.verywellmind.com/positivity-boosting-compliments-1717559).