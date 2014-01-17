===========
Bottle-MongoEngine
===========

This plugin integrates mongoengine with your Bottle application. It connects mongoengine to mongo databases and injects that connection to your route.

Using example::

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


