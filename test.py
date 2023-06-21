import unittest
from main import flatten_packet, flatten_packet_recursive, validate_packet
import io
import sys

small_packet = {
    'a': 1,
    'b': 2,
    'c': {
        'd': 3,
        'e': {
            'f': 4
        },
        'g': 5
    }
}

small_packet_expected_output = {"a": 1, "b": 2, "c.d": 3, "c.e.f": 4, "c.g": 5}

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
            flatten_packet(small_packet),
            small_packet_expected_output,
        )

    def test_small_packet_recursive(self):
        self.assertEqual(
            flatten_packet_recursive(small_packet),
            small_packet_expected_output,
        )

    def test_jumbled_small_packet(self):
        self.assertEqual(
            flatten_packet(small_packet),
            small_packet_expected_output,
        )

    def test_jumbled_small_packet_recursive(self):
        self.assertEqual(
            flatten_packet_recursive(small_packet),
            small_packet_expected_output,

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
        captured_output = io.StringIO()
        sys.stdout = captured_output
        flattened = flatten_packet(small_packet)
        print(flattened, end="")

        sys.stdout = sys.__stdout__

        self.assertEqual(
            captured_output.getvalue(),
            "{'a': 1, 'b': 2, 'c.d': 3, 'c.e.f': 4, 'c.g': 5}",
        )

    def test_small_packet_recursive(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output

        flattened = flatten_packet_recursive(small_packet)
        print(flattened, end="")

        sys.stdout = sys.__stdout__  # Reset redirect.

        self.assertEqual(
            captured_output.getvalue(),
            "{'a': 1, 'b': 2, 'c.d': 3, 'c.e.f': 4, 'c.g': 5}",
        )


class ValidateTest(unittest.TestCase):
    def test_not_dict(self):
        self.assertRaises(TypeError, validate_packet, [])

    def test_dict_with_list(self):
        self.assertRaises(TypeError, validate_packet, {"a": 1, "b": []})

    def test_small_packet(self):
        validate_packet(small_packet)

    def test_dict_with_bad_key(self):
        self.assertRaises(TypeError, validate_packet, {2: 1})


unittest.main()
