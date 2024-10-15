import unittest
from preprocess_functions import *

class TestModel(unittest.TestCase):

    def test_prediction(self):
        # Les prédictions à tester
        prediction = process_transform_text(
            ["Wow ! it is so nice !",
             "Je n'aime pas ces films",
             "I hate you !!!!!",
             "I love you !"]
        ) 
        should_be = [1, 0, 0, 1]

        self.assertEqual(prediction, should_be)  # Comparer avec la prédiction attendue

if __name__ == '__main__':
    unittest.main()
