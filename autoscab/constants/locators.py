from selenium.webdriver.common.by import By

class ApplicationLocator:
    # login stuff
    positions = (By.CLASS_NAME, 'position-card')
    apply_button = (By.CLASS_NAME, 'position-apply-button')
    new_account = (By.CSS_SELECTOR, '.bottomLink > a')

    newacct_email = (By.ID, 'fbclc_userName')
    newacct_email_conf = (By.ID, 'fbclc_emailConf')
    newacct_pass = (By.ID, 'fbclc_pwd')
    newacct_pass_conf = (By.ID, 'fbclc_pwdConf')
    newacct_first = (By.ID, 'fbclc_fName')
    newacct_last = (By.ID, 'fbclc_lName')
    newacct_country = (By.ID, 'fbclc_country')
    newacct_us = (By.CSS_SELECTOR, '#fbclc_country > option[value=US]')
    newacct_create = (By.ID, 'fbclc_createAccountButton')
    newacct_privacy = (By.ID, 'dataPrivacyId')
    newacct_privacy_accept = (By.CSS_SELECTOR, '.modal-footer .globalPrimaryButton')

    apply_email = (By.ID, 'username')
    apply_password = (By.ID, 'password')

    login_btn        = (By.CLASS_NAME, "StaticLoggedOutHomePage-buttonLogin")
    username         = (By.CLASS_NAME, "js-username-field")
    password         = (By.CLASS_NAME, "js-password-field")

    # tweet stuff
    #outer_tweet_box  = (By.CLASS_NAME, 'public-DraftStyleDefault-block')
    outer_tweet_box  = (By.CLASS_NAME, 'DraftEditor-root')
    tweet_box        = (By.CLASS_NAME, "public-DraftEditor-content")
    tweet_btn        = (By.XPATH, "//*[@data-testid='toolBar']//div[2]//div[3]")

    # poll stuff
    poll_btn         = (By.XPATH, '//div[@aria-label="Add poll"]')
    option_one       = (By.NAME, 'Choice1')
    option_two       = (By.NAME, 'Choice2')

    # etc.
    search_input     = (By.ID, "search-query")
    like_btn         = (By.CLASS_NAME, "HeartAnimation")
    latest_tweets    = (By.PARTIAL_LINK_TEXT, 'Latest')