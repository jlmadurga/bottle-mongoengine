
import unittest
import bottle
import mongoengine as mongo
from bottle.ext import mongoengine  # @UnresolvedImport
from webtest import TestApp

TEST_DB_NAME = 'test_bottle_mongoengine'

class Person(mongo.Document):
        name = mongo.StringField()
        age = mongo.IntField()

class MongoEngineTest(unittest.TestCase):

           
    def setUp(self):
        self.app = bottle.Bottle(catchall=False)
        self.test_app = TestApp(self.app)
        self._dbs = []
        
    def test_with_keyword(self):
        self.plugin = self.app.install(mongoengine.Plugin(TEST_DB_NAME))
        @self.app.get('/')
        def test(db):
            self.assertEqual(type(db), type(mongo.connect(TEST_DB_NAME)))
        resp = self.test_app.get('/',expect_errors=True)
        self.assertEqual(resp.status_int, 200)        
        
    def test_without_keyword(self):
        self.plugin = self.app.install(mongoengine.Plugin(TEST_DB_NAME))        
        @self.app.get('/')
        def test():
            pass
        resp = self.test_app.get('/',expect_errors=True)
        self.assertEqual(resp.status_int, 200)

        @self.app.get('/2')
        def test_kw(**kw):
            self.assertFalse('db' in kw)
        resp = self.test_app.get('/2',expect_errors=True)
        self.assertEqual(resp.status_int, 200)
        
    def test_save(self):
        @self.app.get('/')
        def test(db):
            person = Person("Jesus", 33)
            person.save()
            self._db = db
        self.plugin = self.app.install(mongoengine.Plugin(TEST_DB_NAME))
        resp = self.test_app.get('/',expect_errors=True)
        self.assertEqual(resp.status_int, 200)
        self.assertEqual("Jesus",Person.objects()[0].name)
        self.assertEqual(33,Person.objects()[0].age)
        
    def test_multiple_dbs(self):
        @self.app.get('/')
        def test(people,people_2):
            self.assertEqual(type(people), type(mongo.connect(TEST_DB_NAME)))
            self.assertEqual(type(people_2), type(mongo.connect(TEST_DB_NAME)))
            person = Person("Jesus", 33)
            person.save()
            self._dbs.append(people)
        self.plugin = self.app.install(mongoengine.Plugin(TEST_DB_NAME,alias='people',keyword='people'))
        self.plugin_2 = self.app.install(mongoengine.Plugin(TEST_DB_NAME + '2',alias='people_2',keyword='people_2'))    
        
    def test_uri_schema_error(self):
        @self.app.get('/')
        def test(db):
            pass
        self.plugin = self.app.install(mongoengine.Plugin(db=TEST_DB_NAME,alias='failed',host='http://notexists@'))
        resp = self.test_app.get('/',expect_errors=True)
        self.assertEqual(resp.status_int,500)

    def test_uri_ipv6_error(self):
        @self.app.get('/')
        def test(db):
            pass
        self.plugin = self.app.install(mongoengine.Plugin(db=TEST_DB_NAME,alias='refailied',host='mongodb://1080:0:0:0:8:800:200C:417A'))
        resp = self.test_app.get('/',expect_errors=True)
        self.assertEqual(resp.status_int,500)
        
        
    def tearDown(self):
        for connection in self._dbs:
            connection.drop_collection()
        

if __name__ == "__main__":
    unittest.main()