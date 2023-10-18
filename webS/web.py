import speech_recognition as sr
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, WebDriverException
from selenium.webdriver.common.keys import Keys
import time

r = sr.Recognizer()


def open_browser():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.maximize_window()
    return driver


def navigate_to_website(driver, url):
    driver.get(url)


def search_on_google(driver, query):
    driver.get("https://www.google.com")
    search_bar = driver.find_element_by_name("q")
    search_bar.send_keys(query)
    search_bar.submit()


def close_browser(driver):
    driver.quit()


def speak(text):
    print(text)


def handle_command(command, driver):
    if "open browser" in command:
        driver = open_browser()
        speak("Browser opened")

    elif "close browser" in command:
        close_browser(driver)
        speak("Browser closed")
        return None

    elif "go to" in command:
        url = command.split("go to ")[1]
        if "." not in url:
            url = url.replace(" ", "") + ".com"
        if "www." not in url:
            url = "www." + url
        navigate_to_website(driver, "https://" + url)
        speak("Navigating to: " + url)

    elif "search for" in command:
        query = command.split("search for ")[1]
        search_on_google(driver, query)
        speak("Searching for: " + query)

    elif "go down" in command:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        speak("Scrolled down")

    elif "go up" in command:
        driver.execute_script("window.scrollTo(0, 0);")
        speak("Scrolled up")

    else:
        speak("Sorry, I didn't understand that command.")

    return driver


def main():
    driver = None

    while True:
        with sr.Microphone() as source:
            speak("Say a command:")
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio).lower()
            speak("You said: " + command)
            driver = handle_command(command, driver)

        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that command.")

        except (ElementNotVisibleException, WebDriverException) as e:
            speak("An error occurred: {}".format(str(e)))

        except Exception as e:
            speak("An unexpected error occurred: {}".format(str(e)))

        if driver is None:
            driver = None
            break


if __name__ == '__main__':
    main()
