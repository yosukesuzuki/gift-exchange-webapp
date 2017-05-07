from google.appengine.ext import ndb


class Events(ndb.Model):
    user = ndb.UserProperty()
    alias = ndb.StringProperty()
    data = ndb.TextProperty()
    public = ndb.BooleanProperty()
    updated_at = ndb.DateTimeProperty(auto_now=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
