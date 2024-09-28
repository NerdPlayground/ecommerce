from unittest import mock

class CatchSignal():
    def __init__(self,signal):
        self.signal=signal
        self.handler=mock.Mock()
    
    def __enter__(self,*args,**kwargs):
        self.signal.connect(self.handler)
        return self.handler
    
    def __exit__(self,*args,**kwargs):
        self.signal.disconnect(self.handler)