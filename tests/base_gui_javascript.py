import random
import string
from htmlPy import settings


def html_with_string(s):
    return "<html><head></head><body>{}</body></html>".format(s)


class BaseGUIJavascript(object):
    """
    Testing text selection is difficult as text selection is difficult to
    simulate. Persistence of javascript setting will be checked for
    htmlPy.AppGUI
    """

    right_click_simulator = """
        var element = document.getElementsByTagName('div')[0];
        var event = element.ownerDocument.createEvent('MouseEvents');
        event.initMouseEvent('contextmenu', true, true,
            element.ownerDocument.defaultView, 1, 0, 0, 0, 0, false,
            false, false, false,2, null);
        document.write(element.dispatchEvent(event));
        """

    def test_javascript_execution(self):
        random_string = "".join(random.sample(string.ascii_letters, 32))
        javascript = "document.body.innerHTML += '{}'".format(random_string)
        self.app.evaluate_javascript(javascript)
        assert random_string in self.app.html

    def test_right_click_default(self):
        self.app.evaluate_javascript(self.right_click_simulator)
        print self.app.html
        assert self.app.html == html_with_string("true")

    def test_right_click_enabled(self):
        self.app.right_click_setting(settings.ENABLE)
        self.test_right_click_default()

    def test_right_click_disabled(self):
        self.app.right_click_setting(settings.DISABLE)
        self.app.evaluate_javascript(self.right_click_simulator)
        assert self.app.html == html_with_string("false")

    def test_right_click_input_only_non_input(self):
        self.app.right_click_setting(settings.INPUTS_ONLY)
        self.app.evaluate_javascript(self.right_click_simulator)
        assert self.app.html == html_with_string("false")

    def test_right_click_input_only_input(self):
        self.app.right_click_setting(settings.INPUTS_ONLY)
        self.app.evaluate_javascript("document.body.appendChild(" +
                                     "document.createElement('input'));")
        self.app.evaluate_javascript(self.right_click_simulator.replace(
            "div", "input"))
        assert self.app.html == html_with_string("true")