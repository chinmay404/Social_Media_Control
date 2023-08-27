from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(username, password, password2):
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1200,800')
    chrome_options.executable_path = 'chromedriver.exe'
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.instagram.com/accounts/login/")

        username_input = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[aria-label="Phone number, username or email address"]')))
        username_input.send_keys(username)

        password_input = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[aria-label="Password"]')))
        password_input.send_keys(password)

        login_button = driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()

        wait.until(EC.url_contains("instagram.com"))

        if "instagram.com" in driver.current_url:
            print("Login successful!\nReally Want To Change The Pass [y/n]: ")
            choice = input()
            if choice == 'y':
                change_pass(driver, password2 ,password)
            elif choice == 'n':
                print('Canceling Operation')
                driver.quit()
        else:
            print("Login failed!")

    except Exception as e:
        print("Error occurred during login:", e)
        driver.quit()


# cppConfirmPassword

def change_pass(driver, new_pass,old_pass):
    driver.get('https://www.instagram.com/accounts/password/change/')

    try:
        wait = WebDriverWait(driver, 10)

        old_password_input = wait.until(EC.element_to_be_clickable(
            (By.ID, 'cppOldPassword')))
        old_password_input.send_keys(old_pass)

        new_password_input = wait.until(EC.element_to_be_clickable(
            (By.ID, 'cppNewPassword')))
        new_password_input.send_keys(new_pass)
        
        
        confirm_password_input = wait.until(EC.element_to_be_clickable(
            (By.ID, 'cppConfirmPassword')))
        confirm_password_input.send_keys(new_pass)
        
        
        change_password_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[text()="Change Password"]')))
        change_password_button.click()
        
        wait.until(EC.staleness_of(old_password_input))
    except Exception as e:
        print("Error occurred during password change:", e)


# if __name__ == "__main__":
#     username = "addition_control_project_test"
#     password1 = "sirius12121718"
#     password2 = 'sirius1718'

#     login(username, password1, password2)
