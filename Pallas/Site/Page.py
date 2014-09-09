import uuid

class Page:
    _id = None
    _title = None
    
    def __init__(self):
        self._id = uuid.uuid4()

    def __repr__(self):
        return "<Page ('%s')" % (self._id)
    
