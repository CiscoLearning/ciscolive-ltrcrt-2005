[Helper files cover page](./README.md) | [Lab guide cover page](../lab_guide/README.md)

![line](../img/banner_line.png)

# REST APIs and how to work with them

When working with network automation, you would use REST APIs with many of the systems that your are communicating with. REST APIs use HTTP(s), and they are stateless APIs. This means that they don't create a session with the server - each API call needs to include all the information to complete the requested task.

## REST API structure

When executing a REST API call, a client (for example your Python script) calls a server (for example Webex). The targeted resource is defined as an HTTP(s) **URL**, and the action that should be done is defined in the **method**.

General REST API URL structure:
| Protocol | Server or host | Resource | optional query parameters |
| - | - | - | - |
| https:// | webexapis.com | /v1/messages |
| https:// | webexapis.com | /v1/webhooks | ?max=100 |

Methods:

| Method | Typical Action |
| - | - |
| POST | Create or replace |
| GET | Read |
|PUT | Update |
| PATCH | Update |
| DELETE | Delete |

If the method allows you to create or update data, you would include a payload to specify the content - for example when creating a new Webex message, a payload with the receiver and message content would be included in the REST API call.

Example payload that could be used to send a Webex message to a person based on their Webex account's email address.
```json
{
    "toPersonEmail":"jusantal@cisco.com",
    "markdown":"This is the message that would be sent!"
}
```

Often the payload is defined in JSON as in the example above. JSON is similar to Python: it has *objects* which is a key-value structure and really similar to Python dictionary, and *arrays* which are really similar to Python lists. Therefor if you can read Python, you can easily read also JSON.

Finally, you also need to be authenticated for the API call to go through successfully. This can be done by multiple ways - in the case of Webex, you use an authentication Bearer token in the header of the API call. Some other systems require first retrieving a token through a login API.

## How do I know what URL / method / payload etc. to use?

When working on APIs, always refer to the documentation of the API in question.
- In case of Webex, that would be the documentation in developer.webex.com.
- In case of RESTCONF, you would refer to YANG Models with the help of YANG Suite.
- In case on Cisco DNA Center, you would refer to the API documentation built in into the Cisco DNA Center server.
- And so on!

A good REST API documentation tells you the URL to be targeted, what methods are supported and what they do, and how to include payload. The documentation would also include details on how the authentication works on that solution's APIs.

## Using `requests` library to make REST API calls.

`requests` library is a popular Python library to be used when calling REST APIs from your scripts. Below are couple of examples on how to use the library, but for proper documentation, refer to `requests`'s [online documentation](https://requests.readthedocs.io/en/latest/).

Examples of using `requests`:

```python
import requests

#GET request
response = requests.get(url, headers=header)

#POST request using dictionary as a payload
response = requests.post(url, headers=header, json=payload)

#printing the status code
#code starting with 2 is good, other
#numbers indicate an error in the call
print(response.status_code)

#printing the response in text format:
print(response.text)

#transforming JSON based response into Python structure:
print(response.json())
```

![line](../img/banner_line.png)
