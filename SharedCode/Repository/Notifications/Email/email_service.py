from .email_factory import EmailFactory


class EmailService:
    def __init__(self):
        self.client = EmailFactory.get_client()

    def send_email(self, message):
        return self.client.begin_send(message).result()
    
    
# Following is the sample message that can be sent to the email service:

# message = {
#     "content": {
#         "subject": "str",  # Subject of the email message. Required.
#         "html": "str",  # Optional. Html version of the email message.
#         "plainText": "str"  # Optional. Plain text version of the email
#             message.
#     },
#     "recipients": {
#         "to": [
#             {
#                 "address": "str",  # Email address. Required.
#                 "displayName": "str"  # Optional. Email display name.
#             }
#         ],
#         "bcc": [
#             {
#                 "address": "str",  # Email address. Required.
#                 "displayName": "str"  # Optional. Email display name.
#             }
#         ],
#         "cc": [
#             {
#                 "address": "str",  # Email address. Required.
#                 "displayName": "str"  # Optional. Email display name.
#             }
#         ]
#     },
#     "senderAddress": "str",  # Sender email address from a verified domain. Required.
#     "attachments": [
#         {
#             "contentInBase64": "str",  # Base64 encoded contents of the attachment. Required.
#             "contentType": "str",  # MIME type of the content being attached. Required.
#             "name": "str"  # Name of the attachment. Required.
#         }
#     ],
#     "userEngagementTrackingDisabled": bool,  # Optional. Indicates whether user engagement tracking should be disabled for this request if the resource-level user engagement tracking setting was already enabled in the control plane.
#     "headers": {
#         "str": "str"  # Optional. Custom email headers to be passed.
#     },
#     "replyTo": [
#         {
#             "address": "str",  # Email address. Required.
#             "displayName": "str"  # Optional. Email display name.
#         }
#     ]
# }

# response = {
#     "id": "str",  # The unique id of the operation. Uses a UUID. Required.
#     "status": "str",  # Status of operation. Required. Known values are:
#         "NotStarted", "Running", "Succeeded", and "Failed".
#     "error": {
#         "additionalInfo": [
#             {
#                 "info": {},  # Optional. The additional info.
#                 "type": "str"  # Optional. The additional info type.
#             }
#         ],
#         "code": "str",  # Optional. The error code.
#         "details": [
#             ...
#         ],
#         "message": "str",  # Optional. The error message.
#         "target": "str"  # Optional. The error target.
#     }
# }

# -----------------
# Following is the email message with html example:
# -----------------

# message = {
#     "senderAddress": "DoNotReply@tradinglead.in",
#     "recipients":  {
#         "to": [{"address": "shubh.v@outlook.com" }, {"address": "shubhamvishwakarma2001@gmail.com"}],
#     },
#     "content": {
#         "subject": "Hola Fola Alert Notification - Significant Ticker Movements Detected",
#         "plainText": (
#             "Dear Investor,\n\n"
#             "Our system has detected significant movements in the tickers you are tracking. "
#             "Please find the details below.\n\n"
#             "Ticker: Ticker1\n"
#             "Price: 150.00\n"
#             "Details: This ticker has moved 5% above the target price.\n\n"
#             "Ticker: Ticker2\n"
#             "Price: 250.75\n"
#             "Details: This ticker has experienced unusual trading volume.\n\n"
#             "Ticker: Ticker3\n"
#             "Price: 98.50\n"
#             "Details: This ticker has reached a new 52-week low.\n\n"
#             "Regards,\n"
#             "Trading Lead Team"
#         ),
#         "html": (
#             "<html><body>"
#             "<p>Dear Investor,</p>"
#             "<p>Our system has detected significant movements in the tickers you are tracking. "
#             "Please find the details below.</p>"
#             "<table border='1'>"
#             "<tr><th>Ticker</th><th>Price</th><th>Details</th></tr>"
#             "<tr><td>Ticker1</td><td>150.00</td><td>This ticker has moved 5% above the target price.</td></tr>"
#             "<tr><td>Ticker2</td><td>250.75</td><td>This ticker has experienced unusual trading volume.</td></tr>"
#             "<tr><td>Ticker3</td><td>98.50</td><td>This ticker has reached a new 52-week low.</td></tr>"
#             "</table>"
#             "<p>Regards,</p>"
#             "<p>Trading Lead Team</p>"
#             "</body></html>"
#         )
#     }
# }