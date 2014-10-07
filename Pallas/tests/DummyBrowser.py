import random
import uuid
from Main.singleton import singleton

class DummyElement(object):
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.attributes = {}

    def get_attribute(self, attribute):
        if attribute not in self.attributes:
            self.attributes[attribute] = str(uuid.uuid4())
        return self.attributes[attribute]

    def click(self):
        dummy = DummyBrowser()
        dummy.click(self.tag_name)

@singleton
class DummyBrowser(object):
    def __init__(self, seed):
        self.actions = []
        self.entropy = 21

    def get(self, url):
        self.entropy -= 1
        self.actions.append({'action': 'get', 'target': url})
        self.current_url = url
        self.page_source = 'body:get %s' % url

    def click(self, url):
        self.entropy -= 1
        self.actions.append({'action': 'element.click', 'target': url})
        self.current_url = url
        self.page_source = 'body:click %s' % url

    def find_elements_by_tag_name(self, tag):
        returns = random.randint(int(self.entropy/10), int(self.entropy/10) + 3)
        self.actions.append({'action': 'find_elements_by_tag_name', 'target': tag, 'nb': returns})
        elems = []
        try:
            xrange
        except NameError:
            xrange = range
        for i in xrange(returns):
            elems.append(DummyElement(tag))
        return elems

    def find_element_by_xpath(self, xpath):
        self.actions.append({'action': 'find_element_by_xpath', 'target': xpath})
        return DummyElement('new_tag_%s' % xpath)

    def quit(self):
        self.actions.append({'action': 'quit', 'target': None})
