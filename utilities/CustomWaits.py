class element_has_css_class(object):
    """An expectation for checking that an element has a particular css class.
  locator - used to find the element
  returns the WebElement once it has the particular css class

  Example of usage:
  # Wait until an element with id='myNewInput' has class 'myCSSClass'
    wait = WebDriverWait(driver, 10)
    element = wait.until(element_has_css_class((By.ID, 'myNewInput'), "myCSSClass"))
  """

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            if self.css_class in element.get_attribute("class"):
                return element
            else:
                return False
        except:
            return False
