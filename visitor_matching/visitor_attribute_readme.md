## Visitor Attribute Matching

Given a new set of visitor attributes, and a list of existing visitor attributes that are potential matches, calculate a match score (take highest score among all candidates). Additionally, return the boolean `ip_timing_red_flag`, which indicates a seemingly impossible combination of distance/times for the IP address data (e.g. traveling across the world in 3 hours).  An optional dictionary of weights can be provided to influence the relative importance of the attributes. 

The match score is between [0, 100] and is a function of all of the different categories of data we have to compare between the visitors:
- Telemetry data (IP addresses, creation time proximity)
- Payment data (similarity in payment details)
- User data (similarity in user attributes like name, email, etc)
- Address data (similarity in address data)

To deploy:
```
zip visitor-match.zip visitor_attribute_lambda_function.py utils.py visitor_attribute_compare.py
aws lambda create-function --function-name visitor_attribute_matching --zip-file fileb://fingerprint-match.zip --handler visitor_attribute_lambda_function.py --runtime python3.8 --role arn:aws:iam::{your_iam_id}:role/lambda-fingerprint-matching
```

Unfinished TODOs:
- Testing (unit tests etc)
- Identify appropriate weights
- better handling of missing/unexpected values

Example input:
```
{
  "previous_visitors": [
    {
      "ips": [
        {
          "ip": "192.168.0.1",
          "updated_at": "2021-03-17 06:04:11.496715",
          "props": {
            "latitude": 37.805239,
            "longitude": -122.253638
          }
        },
        {
          "ip": "192.168.0.1",
          "updated_at": "2021-04-09 06:04:11.496715",
          "props": {
            "latitude": 37.801239,
            "longitude": -122.258301
          }
        }
      ],
      "visitors": {
        "createdAt": "2021-04-13 21:50:46.419555"
      },
      "payment_methods": {
        "brand": "Visa",
        "expMonth": 12,
        "expYear": 2025,
        "last4": 6335,
        "fingerprint": "Xt5EWLLDS7FJjR1c",
        "global_unique_fingerprint": 1
      },
      "visitor_users": {
        "email": "chester.tester@gmail.com",
        "username": "chester",
        "First_name": "Chester",
        "Last_name": "Tester",
        "Phone": "6074206707"
      },
      "visitor_addresses": {
        "Line1": "1280 21st St",
        "Line2": "Apt 500",
        "City": "Washington",
        "Country": "US",
        "Postal_code": "94612",
        "State": "DC"
      }
    }
  ],
  "new_visitor": {
    "ips": [
      {
        "ip": "192.168.0.1",
        "updated_at": "2021-04-20 06:04:11.496715",
        "props": {
          "latitude": 37.911239,
          "longitude": -122.268801
        }
      },
      {
        "ip": "192.168.0.1",
        "updated_at": "2021-05-30 06:04:11.496715",
        "props": {
          "latitude": 37.691239,
          "longitude": -122.358301
        }
      }
    ],
    "visitors": {
      "createdAt": "2021-04-14 13:32:32.413434"
    },
    "payment_methods": {
      "brand": "Visa",
      "expMonth": 12,
      "expYear": 2025,
      "last4": 6335,
      "fingerprint": "Xt5EWLLDS7FJjR1c",
      "global_unique_fingerprint": 1
    },
    "visitor_users": {
      "email": "chester.tester@gmail.com",
      "username": "chesterdude",
      "First_name": "Chester",
      "Last_name": "Tester",
      "Phone": "6074206707"
    },
    "visitor_addresses": {
      "Line1": "1280 21st St",
      "Line2": "Apt 500",
      "City": "Washington",
      "Country": "US",
      "Postal_code": "94612",
      "State": "DC"
    }
  },
  "weights": {
    "telemetry": {
      "ip_match": 15,
      "geographic_proximity": 5,
      "creation_time_proximity": 2.5,
      "visitor_age_proximity": 2.5
    },
    "payment_methods": 50,
    "visitor_addresses": {
      "Line1": 10,
      "Line2": 10,
      "City": 5,
      "Postal_code": 5,
      "State": 10,
      "Country": 10
    },
    "visitor_users": {
      "email": 25,
      "Phone": 15,
      "First_name": 10,
      "Last_name": 10,
      "username": 10
    }
  }
}
```

Example response:
```
{
  "statusCode": 200,
  "body": {
    "match_score": 100,
    "ip_timing_red_flag": false
  }
}
```
