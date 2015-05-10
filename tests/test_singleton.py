"""Tests the singleton class of pyexperiment

Written by Peter Duerr
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import


import unittest
from pyexperiment.utils.Singleton import Singleton, SingletonIndirector


class TestSingleton(unittest.TestCase):
    """Test the Singleton class/mixin
    """
    def test_singleton_subclass(self):
        """Test that subclasses of Singleton always return same instance
        """
        class SingletonTest(Singleton):
            """Singleton test class
            """
            pass

        singleton_a = SingletonTest.get_instance()
        singleton_b = SingletonTest.get_instance()
        self.assertEqual(singleton_a, singleton_b)

    def test_singleton_resets(self):
        """Test that singletons properly reset themselves.
        """
        class SingletonTest(Singleton):
            """Singleton test class
            """
            def __init__(self):
                """Initializer
                """
                self.memory = []

            def add(self, number):
                """Append a number to the memory
                """
                self.memory.append(number)

        singleton_a = SingletonTest.get_instance()
        singleton_a.add(12)
        self.assertEqual(singleton_a.memory, [12])

        SingletonTest.reset_instance()

        singleton_b = SingletonTest.get_instance()
        self.assertNotEqual(singleton_a, singleton_b)

        self.assertEqual(singleton_b.memory, [])

    def test_indirector_calls(self):
        """Test if the indirector calls the singleton correctly
        """

        class SingletonTest(Singleton):
            """Singleton test class
            """
            def __init__(self):
                self.memory = []

            def add(self, number):
                """Add a number to the memory
                """
                self.memory.append(number)

            def reset(self):
                """Reset the memory
                """
                memory = self.memory
                self.memory = []
                return memory

        indirect = SingletonIndirector(SingletonTest)
        indirect.add(12)

        self.assertEqual(indirect.memory, [12])

        memory = indirect.reset()
        self.assertEqual(memory, [12])
        self.assertEqual(indirect.memory, [])

    def test_indirector_get_instance(self):
        """Test if the indirector can use get_instance
        """

        class SingletonTest(Singleton):
            """Singleton test class
            """
            def __init__(self):
                """Initializer
                """
                self.foo_str = "foo"

            def get_foo(self):
                """Returns the foo string
                """
                return self.foo_str

        indirect = SingletonIndirector(SingletonTest)
        direct = indirect.get_instance()

        self.assertEqual(direct.get_foo(), "foo")

    def test_indirector_reset_instance(self):
        """Test if the indirector can use reset_instance
        """

        class SingletonTest(Singleton):
            """Singleton test class
            """
            def __init__(self):
                """Initializer
                """
                self.memory = []

            def add(self, number):
                """Add a number to the memory
                """
                self.memory.append(number)

        indirect = SingletonIndirector(SingletonTest)
        indirect.add(12)

        self.assertEqual(SingletonTest.get_instance().memory, [12])

        indirect.reset_instance()
        self.assertEqual(SingletonTest.get_instance().memory, [])

    def test_singleton_indirector_repr(self):
        """Test calling the repr method on SingletonIndirector
        """
        class FooSingleton(Singleton):
            """Singleton test class
            """
            def __repr__(self):
                """Returns foo
                """
                return "foo"
        singleton = SingletonIndirector(FooSingleton)
        self.assertEqual(singleton.__repr__(), "foo")

    def test_singleton_indirector_dir(self):
        """Test calling the dir method on SingletonIndirector
        """
        class FooSingleton(Singleton):
            """Singleton test class
            """
            @staticmethod
            def bla():
                """Returns foo
                """
                return "foo"

        singleton = SingletonIndirector(FooSingleton)
        self.assertIn('bla', dir(singleton))

    def test_iter_singleton_indirector(self):
        """Test iterating over singleton
        """
        class FooSingleton(Singleton, list):
            """Iterable Singleton
            """
            pass

        singleton = SingletonIndirector(FooSingleton)

        for i in range(10):
            singleton.append(i)

        for item, expected in zip(singleton, range(10)):
            self.assertEqual(item, expected)

    def test_next_singleton_indirector(self):
        """Test using a singleton as an iterator
        """
        class FooSingleton(Singleton):
            """Singleton Iterator
            """
            def __init__(self):
                """Initializer
                """
                self.state = 0

            def __iter__(self):
                """Make FooSingleton an iterator...
                """
                return self

            def __next__(self):
                """Returns the next value
                """
                if self.state < 3:
                    self.state += 1
                    return self.state
                else:
                    raise StopIteration

            def next(self):
                """For python 2.x compatibility"""
                return self.__next__()

        singleton = SingletonIndirector(FooSingleton)

        for item, expected in zip(singleton, range(1, 4)):
            self.assertEqual(item, expected)
