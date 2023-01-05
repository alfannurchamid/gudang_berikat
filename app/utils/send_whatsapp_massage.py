import numbers
import requests


class WhatsApp(object):

    def __init__(self):
        pass

    def send_message(self, RecipientPhoneNumber: str, kode: int):
        url = 'https://graph.facebook.com/v14.0/113756431518535/messages'
        myobj = {
            "messaging_product": "whatsapp",
            "to": RecipientPhoneNumber,
            # "to": "6285742464907",
            "type": "template",
            "template": {
                "name": "otp",
                "language": {
                    "code": "id"
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": kode
                            }
                        ]
                    }
                ]
            }
        }
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer EAALIAfYZASCQBAGY6MUo8jZAd6qAJbhE1EZCX0Af8x6lwwQUxmX6dGZA2GMrAe2JZBPZC3vzVzZAXFRCgC5Qr5dYOY9VtenpCgpZC3cUW7a8fbqT3KhgMG3c0ZAawfz971LJMpjX7ojZB62FnL7A4hTvF9oGTtcyFqvHu39LUtKbLwAfrhgzdENwgO'}
        x = requests.post(url, json=myobj, headers=header)

        print(x.text)
        return x.json()
