from django.test import TestCase

import json

class CalculatorTests(TestCase):

    # TODO in the future, might move up the case list setups here for more clean code
    def setUp(self) -> None:
        return super().setUp()
    
    def helper_func(self, cases):
        """
        Helper function that makes the requests to the API given a set of cases
        """
        for case in cases:
            response = self.client.post('/calculator/', data=json.dumps(case[0]), content_type='application/json')

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(
                str(response.content, encoding='utf8'),
                {'delivery_fee': case[1]}
            )

    def test_0cost(self):
        """
        Tests for the cases where the cart value is more or equal to 100
        """
        test_cases = [
            (
                {
                    "cart_value": 100,
                    "delivery_distance": 1000,
                    "number_of_items": 4,
                    "time": "2021-10-12T13:00:00Z"
                },
                0
            ),
            (
                {
                    'cart_value': 101,
                    "delivery_distance": 1000,
                    "number_of_items": 4,
                    "time": "2021-10-12T13:00:00Z"
                },
                0
            ),
        ]
        self.helper_func(test_cases)

    def test_15cost(self):
        """
        Tests for the cases where the total cost of transportation excedes 15
        """
        test_cases = [
            (
                {
                    "cart_value": 10,
                    "delivery_distance": 8000,
                    "number_of_items": 10,
                    "time": "2021-10-12T13:00:00Z"
                },
                15
            ),
            (
                {
                    "cart_value": 10,
                    "delivery_distance": 100,
                    "number_of_items": 30,
                    "time": "2021-10-12T13:00:00Z"
                },
                15
            ),
            (
                {
                    "cart_value": 10,
                    "delivery_distance": 100,
                    "number_of_items": 50,
                    "time": "2021-10-12T13:00:00Z"
                },
                15
            )
        ]
        self.helper_func(test_cases)

    def test_normalCost(self):
        """
        Tests for some normal cases
        """
        test_cases = [
            (
                {
                    "cart_value": 10,
                    "delivery_distance": 100,
                    "number_of_items": 29,
                    "time": "2021-10-12T13:00:00Z"
                },
                14.5
            ),
            (
                {
                    "cart_value": 40,
                    "delivery_distance": 1250,
                    "number_of_items": 10,
                    "time": "2021-10-12T13:00:00Z"
                },
                6
            ),
            (
                {
                    "cart_value": 10,
                    "delivery_distance": 1000,
                    "number_of_items": 20,
                    "time": "2021-10-12T13:00:00Z"
                },
                10
            )
        ]
        self.helper_func(test_cases)
    
    def test_rushHour(self):
        """
        Tests for the above cases, but when they are in the rush hour
        """
        test_cases = [
            (
                 {
                    "cart_value": 10,
                    "delivery_distance": 100,
                    "number_of_items": 29,
                    "time": "2022-01-21T15:00:00Z"
                },
                min(15, 14.5 * 1.1)
            ),
            (
                {
                    "cart_value": 40,
                    "delivery_distance": 1250,
                    "number_of_items": 10,
                    "time": "2022-01-21T16:15:35Z"
                },
                6 * 1.1
            )
        ]
        self.helper_func(test_cases)
            