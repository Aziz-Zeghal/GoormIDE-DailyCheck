from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class AutomatedCheckIn:
    __slots__ = 'driver', 'email', 'password', 'url'
    def __init__(self, email, password, url):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        
        self.email = email
        self.password = password
        self.url = url
        # Open the URL as part of the initialization
        self.driver.get(self.url)
        sleep(1)

    def login(self):
        # Using WebDriverWait instead of sleep
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="emailInput"]'))
        )
        password_input = self.driver.find_element(By.XPATH, '//*[@id="passwordInput"]')
        login_button = self.driver.find_element(By.XPATH, '//*[@id="app"]/section/div[4]/button/span/span/span')

        email_input.send_keys(self.email)
        password_input.send_keys(self.password)
        login_button.click()
        sleep(1)
        
        # If the login button is still there, login unsuccessful
        try:
            self.driver.find_element(By.XPATH, '//*[@id="app"]/section/div[4]/button/span/span/span')
            print("Login unsuccessful, check your credentials !")
            self.driver.close()
            self.driver.quit()
            # Throw an exception to stop the program
            raise Exception("Exit please")
        except:
            raise Exception("Login unsuccessful")

    def check_in(self):
        sleep(1)
        # Handle popup if it exists
        try:
            self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div[3]/div/button').click()
        except:
            print("No popup!")

        # Daily check-in button click
        sleep(0.5)
        self.driver.find_element(By.XPATH, '//*[@id="AttendanceFloatingButton_tooltipId"]').click()

        # Confirm the daily check-in
        sleep(0.5)
        checkinButton = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div[1]/div/div/div/div[2]/div/button')

        # Did we already do a check-in ?
        if checkinButton.text.startswith("Daily check-in completed"):
            print("Already checked-in !")
        else:
            checkinButton.click()
            sleep(0.5)
    def close(self):
        self.driver.close()
        self.driver.quit()

if __name__ == "__main__":
    email = "PUT EMAIL"
    password = "PUT PASSWORD"
    url = "https://ide.goorm.io/my/dashboard#/containers"

    check_in_bot = AutomatedCheckIn(email, password, url)
    check_in_bot.login()
    check_in_bot.check_in()
    check_in_bot.close()
