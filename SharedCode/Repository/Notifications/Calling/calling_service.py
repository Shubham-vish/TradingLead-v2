from .calling_factory import CallingFactory


class CallingService:
    def __init__(self):
        self.client = CallingFactory.get_client()
    
   
   
    
    def call_to(self, to_number):
        url="http://demo.twilio.com/docs/voice.xml"
        from_="+12018449779"
        to = to_number
        call = self.client.calls.create(url=url,to=to,from_=from_)
        print(call.sid)

        
    def msg_to(self,to,msg):
        message = self.client.messages.create(
        from_='whatsapp:+14155238886',
        body=msg,
        to=to)
        print(message.sid)
        
    