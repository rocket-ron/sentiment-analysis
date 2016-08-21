from flask import Flask
from flask_restful import Resource, Api
import unittest
import json
from pymongo import MongoClient


"""
    RESTful API for Sentiment Analysis

    Provide a REST API to query the average sentiment at a location provided
        latitude
        longitude
        radius (meters)

    GET http://localhost:5000/sentiment?lat=40.7128?lon=74.0059?radius=5000

    The response is a JSON object with the following structure

        {
            "tweets": 100,              // number of tweets
            "average_polarity": 0.4,    // TextBlob provides a polarity value for sentiment analysis
            "most_positive": {          // tweet at this location with highest polarity
                "text": "what a great day!",
                "coordinates": [-75.14310264, 40.05701649]
            },
            "most_negative": {          // tweet at this location with lowest polarity
                "text": "worst lunch ever!",
                "coordinates": [-75.14311344, 40.05701716]
            }
        }

"""


# Implement the sentiment REST GET query
class Sentiment(Resource):
    def get(self):
        return {'tweets': 100,
                'average_polarity': 0.4,
                'most_positive': {
                    'text': 'what a great day!',
                    'coordinates': [-75.14310264, 40.05701649]
                },
                'most_negative': {
                    'text': 'worst lunch ever!',
                    'coordinates': [-75.14311344, 40.05701716]
                }}

app = Flask(__name__)
api = Api(app)

api.add_resource(Sentiment, '/')

# run the app server
if __name__ == '__main__':
    app.run(debug=True)


"""

    Unit Tests

"""


class Sentiment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a Flask test client
        self.app = app.test_client()
        # propogate exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_response_structure(self):
        result = self.app.get('/')
        response = json.loads(result.data)
        self.assertIn('tweets', response, "Missing 'tweets' in response")
        self.assertIn('average_polarity', response, "Missing 'average_polarity' in response")
        self.assertIn('most_positive', response, "Missing 'most_positive' in response")
        self.assertIn('most_negative', response, "Missing 'most_negative' in response")

    def test_response_values(self):
        result = self.app.get('/')
        response = json.loads(result.data)
        self.assertEqual(response['tweets'], 100,
                         "Tweet count should be 100 but I saw {0}".format(response['tweets']))
        self.assertEqual(response['average_polarity'], 0.4,
                         "Average polarity should be 0.4 but I saw {0}".format(response['average_polarity']))

    def test_bad_path(self):
        result = self.app.get('/foo')
        self.assertEqual(result.status_code, 404)


# Run the unit tests
#if __name__ == '__main__':
#    unittest.main()
