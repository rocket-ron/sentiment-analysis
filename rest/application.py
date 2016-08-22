from flask import Flask
from flask_restful import Resource, Api, reqparse
import unittest
import json
import os
from pymongo import MongoClient


mongo_client = MongoClient(host='ec2-54-193-5-118.us-west-1.compute.amazonaws.com')
mongodb = mongo_client['tweets']

parser = reqparse.RequestParser()
parser.add_argument('lat', type=float, required=True)
parser.add_argument('lon', type=float, required=True)
parser.add_argument('dist', type=float, required=True)

"""
    RESTful API for Sentiment Analysis

    Provide a REST API to query the average sentiment at a location provided
        latitude
        longitude
        radius (meters)

    GET http://localhost:5000/sentiment?lat=40.7128?lon=74.0059?dist=5000

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

    db.sentiment.find({ coordinates: {$geoWithin: {$centerSphere: [ [ -74, 40.74 ], 10/6371] } } } )

    radius of earth in kilometers = 6371

"""


# Implement the sentiment REST GET query
class Sentiment(Resource):
    def get(self):
        args = parser.parse_args()
        if 'lat' in args and 'lon' in args and args['lat'] and args['lon']:
            if args['lat']:
                latitude = float(args['lat'])
            if args['lon']:
                longitude = float(args['lon'])
            if 'dist' in args:
                # distance should be in kilometers
                distance = float(args['dist'])/6371
            else:
                distance = 0.0
            cursor = mongodb['sentiment'].aggregate(
                [{"$match": {"coordinates": {"$geoWithin": {"$centerSphere": [[longitude, latitude], distance]}}}},
                {"$group": {
                  "_id": "null",
                  "tweets": {"$sum": 1},
                  "average_polarity": {"$avg": "$polarity"},
                  "most_positive": {"$max": "$polarity"},
                  "most_negative": {"$min": "$polarity"},
                  "docs": {"$push": {
                    "polarity": "$polarity",
                    "text": "$text",
                    "coordinates": "$coordinates.coordinates"
                  }}
                }},
                {"$project": {
                    "tweets": 1,
                    "average_polarity": 1,
                    "most_positive": {
                        "$setDifference": [
                          {"$map": {
                            "input": "$docs",
                            "as": "doc",
                            "in": {
                              "$cond": [
                                {"$eq": ["$most_positive", "$$doc.polarity"]},
                                  "$$doc",
                                  "false"
                                ]}
                          }},
                          ["false"]
                        ]
                    },
                    "most_negative": {
                        "$setDifference": [
                          {"$map": {
                            "input": "$docs",
                            "as": "doc",
                            "in": {
                              "$cond": [
                                {"$eq": ["$most_negative", "$$doc.polarity"]},
                                 "$$doc",
                                 "false"
                            ]
                        }
                      }},
                      ["false"]
                    ]}
                    }}
                ])
            for result in cursor:
                return result
        else:
            return "Latitude: {0} Longitude: {1} distance: {2}".format(args['lat'], args['lon'], args['dist'])


application = Flask(__name__)
api = Api(application)

api.add_resource(Sentiment, '/sentiment')


# run the app server
if __name__ == '__main__':
    application.run()


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
        self.app = application.test_client()
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
