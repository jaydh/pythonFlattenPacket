import unittest
from main import flatten_packet, flatten_packet_recursive
import io
import sys

packet = {"a": 1, "b": 2, "c": {"d": 3, "e": {"f": 4}, "g": 5}}

jumbled_small_packet = {
    "c": {
        "e": {"f": 4},
        "g": 5,
        "d": 3,
    },
    "a": 1,
    "b": 2,
}

float_packet = {"a": 1.0, "b": 2.0, "c": {"d": 3.0, "e": {"f": 4.0}, "g": 5.0}}


deep_nested_packet = input_json = {
    "name": "John Doe",
    "age": 30,
    "top_property1": "value1",
    "top_property2": "value2",
    "nested1": {
        "nested2": {
            "nested3": {
                "nested4": {
                    "nested5": {
                        "nested6": {
                            "nested7": {
                                "nested8": {
                                    "nested9": {"nested10": "final_value"}
                                }
                            }
                        }
                    }
                }
            }
        }
    },
}


class FlattenTest(unittest.TestCase):
    def test_small_packet(self):
        self.assertEqual(
            flatten_packet(packet),
            {"a": 1, "b": 2, "c.d": 3, "c.e.f": 4, "c.g": 5},
        )

    def test_small_packet_recursive(self):
        self.assertEqual(
            flatten_packet_recursive(packet),
            {"a": 1, "b": 2, "c.d": 3, "c.e.f": 4, "c.g": 5},
        )

    def test_jumbled_small_packet(self):
        self.assertEqual(
            flatten_packet(packet),
            {"a": 1, "b": 2, "c.d": 3, "c.e.f": 4, "c.g": 5},
        )

    def test_jumbled_small_packet_recursive(self):
        self.assertEqual(
            flatten_packet_recursive(packet),
            {"a": 1, "b": 2, "c.d": 3, "c.e.f": 4, "c.g": 5},
        )

    def test_float_packet(self):
        self.assertEqual(
            flatten_packet(float_packet),
            {"a": 1.0, "b": 2.0, "c.d": 3.0, "c.e.f": 4.0, "c.g": 5.0},
        )

    def test_float_packet_recursive(self):
        self.assertEqual(
            flatten_packet_recursive(float_packet),
            {"a": 1.0, "b": 2.0, "c.d": 3.0, "c.e.f": 4.0, "c.g": 5.0},
        )

    def test_nested_packet(self):
        self.assertEqual(
            flatten_packet(deep_nested_packet),
            {
                "age": 30,
                "name": "John Doe",
                "nested1.nested2.nested3.nested4.nested5.nested6.nested7.nested8.nested9.nested10": "final_value",
                "top_property1": "value1",
                "top_property2": "value2",
            },
        )


class PrintTest(unittest.TestCase):
    def test_small_packet(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # and redirect stdout.

        flattened = flatten_packet(packet)
        print(flattened, end="")

        sys.stdout = sys.__stdout__  # Reset redirect.

        self.assertEqual(
            captured_output.getvalue(),
            "{'a': 1, 'b': 2, 'c.d': 3, 'c.e.f': 4, 'c.g': 5}",
        )

    def test_small_packet_recursive(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # and redirect stdout.

        flattened = flatten_packet_recursive(packet)
        print(flattened, end="")

        sys.stdout = sys.__stdout__  # Reset redirect.

        self.assertEqual(
            captured_output.getvalue(),
            "{'a': 1, 'b': 2, 'c.d': 3, 'c.e.f': 4, 'c.g': 5}",
        )


unittest.main()
