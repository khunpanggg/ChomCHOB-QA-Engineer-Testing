"""
===============================================
Section 2: Automate Testing WEB Skills
===============================================

This script is written by Nichapat.

Features:
- Language: Python 3.12.1
- Library: Selenium 4.17.2
- Framework: Pytest 8.0.1

===============================================
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.common.exceptions import TimeoutException

import time
import pytest

""" For running tests with Chrome web driver """
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=options)

""" For running tests with Edge web driver """
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Edge(options=options)

def test_open_browser():
    """ 
    TC-001: Open browser.
    """
    driver.get("https://www.nejavu.com")

def test_close_popup():
    """
    TC-002: Close Pop-up.
    """
    popup_element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@class='close-modal']")))
    assert popup_element
    popup_element.click()

def test_click_link_cartoon():
    """
    TC-003: Click link cartoon page.
    """
    try:
        # Wait for the overlay to disappear
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-overlay")))
        # Click accept cookie
        accept_cookie_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='top']/main/div[4]/div/small/small/div/div[1]/button/a[text()='ยอมรับ']")))
        accept_cookie_element.click()
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "cookie-policy show")))
        # Click link cartoon page
        link_element = driver.find_element(By.XPATH, "//a[@href='https://www.nejavu.com/cartoon']//span[text()='การ์ตูน']")
        driver.execute_script("arguments[0].click();", link_element)
    except TimeoutException:
        print("Timed out waiting for element to be clickable.")
    except Exception as e:
        print(f"An error occurred: {e}")

@pytest.fixture
def get_first_row_book_elements():
    """
    Fixture to get the first 5 book title elements.
    """
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='bg-white book-list']/div[2]//h5[@class='detail-title']"))
    )
    book_title_elements = driver.find_elements(By.XPATH, "//div[@class='bg-white book-list']/div[2]//h5[@class='detail-title']")
    first_row_book_elements = book_title_elements[:5]
    return first_row_book_elements

def test_get_book_title_list(get_first_row_book_elements):
    """
    TC-004: Get book title list.
    """
    assert len(get_first_row_book_elements) == 5

def test_add_book(get_first_row_book_elements):
    """
    TC-005: Add book in cart.
    """
    button_elements = driver.find_elements(By.XPATH, "//form[@id='QuickCartRequestForm']//button[@id='quick-cart-button']")
    buttons_to_click = button_elements[:5]

    assert len(buttons_to_click) == len(get_first_row_book_elements)

    for button in buttons_to_click:
        try:
            time.sleep(3)
            driver.execute_script("arguments[0].click();", button)
            WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.XPATH, "//iframe[@id='k_frame']"))).click()
        except Exception as e:
            print(f"An error occurred: {e}")

def test_click_cart_btn(get_first_row_book_elements):
    """ 
    TC-006: - Click cart button.
            - Verify all of book title in cart using the name from 'get_first_row_book_elements()' function.
    """
    try:
        # Click the cart button.
        cart_element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='nev-noti-icon']//a[@href='https://www.nejavu.com/cart']")))
        cart_element.click()
    except TimeoutException:
        print("Timed out waiting for element to be clickable.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Verify all book title in cart.
    cart_item_elements = driver.find_elements(By.XPATH, "//div[@id='cart']//div[@class='cart-item-table']//div[@class='cart-item-detail']//p[strong]")
    assert len(cart_item_elements) == len(get_first_row_book_elements)

def test_delete_item():
    """
    TC-007: - Delete all books in cart.
            - Verify badge on the cart that there are 0 books.
    """
    # Delete all books in cart.
    delete_item_elements = driver.find_elements(By.XPATH, "//div[@id='cart']//div[@class='cart-item-table']//a[@class='delete-item']")
    for _ in range(len(delete_item_elements)):
        try:
            delete_item_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='cart']//div[@class='cart-item-table']//a[@class='delete-item']")))
            delete_item_element.click()
            # Click pop-up
            confirm_to_delete_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-labelledby='swal2-title' and @aria-describedby='swal2-content']//button[text()='ใช่ ลบรายการ']")))
            confirm_to_delete_element.click()
            # Wait for page refresh
            WebDriverWait(driver, 10).until(staleness_of(driver.find_element(By.XPATH, "//div[@id='cart']")))
        except Exception as e:
            print(f"An error occurred: {e}")

    # Verify badge on the cart.
    item_in_cart_element = driver.find_element(By.ID, "badge-cart")
    total_item_in_cart = int(item_in_cart_element.text)
    assert total_item_in_cart == 0