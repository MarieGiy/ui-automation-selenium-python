# pre-requisites 
# pip install selenium
# requires external installation of chromedriver if < selenium 4.6 

from selenium import webdriver
# sends keyboard commands | fills out input 
from selenium.webdriver.common.keys import Keys
# convinient finders/ locators
from selenium.webdriver.common.by import By
# for explicit waits with condition
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.wizardingworld.com/"

# very high-level control (expected) data 
PAGE_TITLE = 'Wizarding World: The Official Home of Harry Potter' 
SNAPE_NAME = 'Severus Snape'

# selectors | tags | xpath
SEARCH_BUTTON_CSS = 'button.SearchInput_navSearch__3fovm'
SEARCH_BAR_HTML = 'input'
CURATED_TAB_XPATH = '/html/body/div[1]/div[2]/div/div[5]/div/div[3]/div[1]/ul/ul/li[6]'
CURATED_PAGE_CSS = '.SearchResult_resultWrapper__BHJ-2'
SNAPE_NAME_CSS = '.CollectionHero_header__3rDGu'


def test_main():
  # new versions of selenium doen't require chromederiver path
  driver = webdriver.Chrome()
  driver.get(URL)
  
  # for page title validation
  page_title = driver.title

  # find and click on search icon
  # using CSS finder
  search_button = driver.find_element(By.CSS_SELECTOR, SEARCH_BUTTON_CSS)
  search_button.click()  
    
  # init explicit waits with 5 sec timecap  
  wait = WebDriverWait(driver, 5)
  
  # wait for search bar to 
  # fill in search query | SNAPE_NAME
  # used HTML tag finder
  
  # notice: html generates dynamicly
  # TODO: found with document.querySelector
  input = wait.until(EC.element_to_be_clickable((By.TAG_NAME, SEARCH_BAR_HTML)))
  input.send_keys(SNAPE_NAME)
  input.send_keys(Keys.RETURN)

  # Choose Curated tab
  # using XPATH finder
  curated_side_tab = wait.until(
    EC.element_to_be_clickable((By.XPATH, CURATED_TAB_XPATH))
    )  
  curated_side_tab.click()

  # implicit wait example 
  # notice: only waits specific time, no element presence check
  driver.implicitly_wait(2)

  # Click on entry Snape's entry
  curated_page = driver.find_element(By.CSS_SELECTOR, CURATED_PAGE_CSS)
  
  # notice: opens in new window, thus save open windows at this moment
  open_windows = driver.window_handles
  curated_page.click()

  # waits for new windpw 
  wait.until(EC.new_window_is_opened(open_windows))
  
  # notice: open windows length changed, therefor check open windows again
  open_windows = driver.window_handles
  # new window id appends to windows list
  # TODO: more precise solution - check new list's entries
  new_tab_id = open_windows[1]
  
  # move to new window
  driver.switch_to.window(new_tab_id)
  
  # main text with snape's name 
  snape_header = driver.find_element(By.CSS_SELECTOR, SNAPE_NAME_CSS)
  snape_text = snape_header.text 

  # close browser
  driver.quit()

  # assertions
  assert page_title == PAGE_TITLE
  assert snape_text == SNAPE_NAME

test_main()