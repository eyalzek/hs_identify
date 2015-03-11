import time
from selenium import webdriver


class Webpage(object):
    """A headless PhantomJS page holding the arena value comparison"""
    def __init__(self):
        super(Webpage, self).__init__()
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1366, 768)
        self.url = "http://arenavalue.com"
        self.start()

    def start(self):
        self.driver.get(self.url)
        self.screenshot("homepage")
        self.print_title()

    def choose_class(self, heroClass):
        tag = self.driver.find_element_by_css_selector("img[title='%s']" %heroClass)
        tag.click()
        self.screenshot("%s-main" %heroClass)
        self.print_title()

    def enter_picks(self, picks):
        for i in xrange(len(picks)):
            selector = "#card%d" %(i + 1)
            value = self.driver.execute_script('return $(\'%s option:contains("%s")\').val();' %(selector, picks[i].strip()))
            self.driver.execute_script('$(\'%s\').select2(\'val\', \'%s\');' %(selector, value))
            self.driver.execute_script('$(\'%s\').trigger(\'select2-close\');' %selector)
            self.driver.execute_script('$(\'%s\').trigger(\'change\');' %selector)
            time.sleep(0.4)
            self.screenshot("pick%d" %i)

    def get_values(self):
        values = []
        for i in xrange(1, 4):
            selector = "#s%d" %i
            text = self.driver.execute_script('return $(\'%s\').text()' %selector)
            values.append(int("".join([c for c in text if not c.isalpha()])))
        return values

    def make_pick(self, pick):
        el = self.driver.find_element_by_id("img%d" %pick)
        el.click()
        print("Picked: %d" %pick)
        time.sleep(0.3)
        self.screenshot("after_pick")

    def print_title(self):
        print("Page title: %s" %self.driver.title)

    def screenshot(self, filename):
        print("saving %s"%filename)
        self.driver.save_screenshot(filename + ".png")

    def quit(self):
        print("closing page...")
        self.driver.quit()
