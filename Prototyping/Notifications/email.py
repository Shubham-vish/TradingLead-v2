# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join("../../..")))

from Prototyping.setupConfig import setup_config

setup_config()
# Above lines are only for local notebook testing. Not to be used in production.


from SharedCode.Repository.Notifications.Email.email_service import EmailService

email_service = EmailService()

message = {
    "senderAddress": "alerts@tradinglead.in",
    "recipients": {
        "to": [
            {"address": "shubh.v@outlook.com"},
            {"address": "shubhamvishwakarma2001@gmail.com"},
        ],
    },
    "content": {
        "subject": "Alerts Hola Testing Tradinglead.in Alert Notification - Significant Ticker Movements Detected",
        "plainText": (
            "Dear Investor,\n\n"
            "Our system has detected significant movements in the tickers you are tracking. "
            "Please find the details below.\n\n"
            "Ticker: Ticker1\n"
            "Price: 150.00\n"
            "Details: This ticker has moved 5% above the target price.\n\n"
            "Ticker: Ticker2\n"
            "Price: 250.75\n"
            "Details: This ticker has experienced unusual trading volume.\n\n"
            "Ticker: Ticker3\n"
            "Price: 98.50\n"
            "Details: This ticker has reached a new 52-week low.\n\n"
            "Regards,\n"
            "Trading Lead Team"
        ),
        "html": (
            "<html><body>"
            "<p>Dear Investor,</p>"
            "<p>Our system has detected significant movements in the tickers you are tracking. "
            "Please find the details below.</p>"
            "<table border='1'>"
            "<tr><th>Ticker</th><th>Price</th><th>Details</th></tr>"
            "<tr><td>Ticker1</td><td>150.00</td><td>This ticker has moved 5% above the target price.</td></tr>"
            "<tr><td>Ticker2</td><td>250.75</td><td>This ticker has experienced unusual trading volume.</td></tr>"
            "<tr><td>Ticker3</td><td>98.50</td><td>This ticker has reached a new 52-week low.</td></tr>"
            "</table>"
            "<p>Regards,</p>"
            "<p>Trading Lead Team</p>"
            "</body></html>"
        ),
    },
}

email_service.send_email(message)
