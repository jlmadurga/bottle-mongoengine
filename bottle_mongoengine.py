'''
Bottle-mongoengine is a plugin that integrates MongoEngine with your Bottle 
application. It automatically connects to mongo databases at the begining 
of the request, passes the connection handle to the route callback and closes 
the connection afterwards

Usage Example::
    
    import bottle
    from bottle.ext import mongoengine
    
    app = bottle.Bottle()
    plugin = mongoengine.Plugin(db='name',alias='first_db')
    app.install(plugin)
    
    @app.route('/show/:item')
    def show(item, db):
        item = Item.objects(id=item)
        if item:
            return template('showitem', item=item)
        return HTTPError(404, "Page not found")

    
'''



import mongoengine
from mongoengine.connection import disconnect
import inspect
import bottle
from pymongo import errors as pymongo_errors

class MongoEnginePlugin(object):
    '''
    This plugin connects to monogengine database and passes it
    to route callbacks that accept keyword argument. If callback
    does not expect such parameter, no connection is made.
    Several connection may be managed    
    '''
    name = 'mongoengine'    
    api = 2

    def __init__(self,db,alias='default',keyword='db',
                 msg_error="Database Error",**dbargs):
        """
        :param db: name of mongo database
        :param alias: the name that will be used to refer to this connection
            throughout MongoEngine
        :param keyword: keyword used to inject database connection in a route
        :param msg_error: message returned when 500 Internal Server error returned
        :param **dbargs: optional mongoengine connection parameters host,port,user,...
        """

        self.db = db
        self.alias = alias
        self.keyword = keyword
        self.dbargs = dbargs
        self.msg_error = msg_error
                
    def setup(self,app):
        '''
        Make sure other installed plugins don't affect the same keyword
        argument
        '''
        for other in app.plugins:
            if not isinstance(other,MongoEnginePlugin): continue
            if other.keyword == self.keyword:
                raise bottle.PluginError("mongoengine plugin with "\
                                  "conflicting settings (non-unique keyword)")
    
    def apply(self,callback,context):
        #Override global configuration with route-specific values
        conf = context.config.get('mongoengine') or {}
        db = conf.get('db', self.db)
        alias = conf.get('alias',self.alias)
        keyword = conf.get('keyword',self.keyword)
        dbargs = conf.get('dbargs', self.dbargs)
        msg_error = conf.get('msg_error',self.msg_error)
        
        # Test if the original callback accepts a 'mongoengine' keyword
        # Ignore it if it does not need mongoengine connection
        args = inspect.getargspec(context.callback)[0]
        
        if keyword not in args:
            return callback
        
        def wrapper(*args,**kwargs):
            try:
                # Mongoengine connects to mongodb 
                connection = mongoengine.connect(db,alias,**dbargs)            
                #Add the connection handle as a keyword argument
                kwargs[keyword] = connection            
                rv = callback(*args,**kwargs)
                
            except (mongoengine.ConnectionError, pymongo_errors.InvalidURI, pymongo_errors.ConfigurationError), e:
                raise bottle.HTTPError(500, msg_error, e)
            finally:
                disconnect(alias)
            return rv
        #Replace the route callback with the wrapped one
        return wrapper


Plugin = MongoEnginePlugin
                
            