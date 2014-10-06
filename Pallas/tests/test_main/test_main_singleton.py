import os.path
import sys


def setup_module(module):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class Test_Main_singleton(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_singleton(self):
        import random
        from Main.singleton import singleton
        @singleton
        class Test:
            value = None
            def __init__(self):
                self.value = random.random()
        t1 = Test()
        t2 = Test()
        assert t1.value == t2.value

    def test_singleton_with_value(self):
        import random
        from Main.singleton import singleton
        @singleton
        class Test:
            value = None
            def __init__(self, init):
                self.value = random.random()
        t1 = Test(3)
        t2 = Test(3)
        assert t1.value == t2.value
        t3 = Test(7)
        assert t1.value != t3.value
        t4 = Test(7)
        assert t3.value == t4.value
        #re-initializing a singleton with a value already used still create a new instance
        t5 = Test(3)
        assert t1.value != t5.value
