import datetime

from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from pastey.models import *
from pastey.views import *
thisnow = datetime.datetime.now()

class CodeTestCase(TestCase):
    def setUp(self):   
        self.test_full_paste = Code.objects.create(
            title = "Testing",             
            code_paste = "def testing(sys.argv[[1]):",
            author = "Caleb-via-ASUS",
            email = "caleb.smithnc@gmail.com",
            private = False,
            language = "python",
            pub_date = thisnow,
            del_date = thisnow
            )
        self.test_vague_paste = Code.objects.create(
            code_paste = "small code",            
            pub_date = thisnow,
            del_date = thisnow
            )
        self.test_private = Code.objects.create(
            code_paste = "some private code",
            private = True,
            pub_date = thisnow,
            del_date = thisnow
            )
        self.client = Client()
    # test default values and model class methods    
    def testDefaults(self):
        self.assertEqual(self.test_vague_paste.language, "python")
        self.assertEqual(self.test_vague_paste.title, None)
        self.assertEqual(self.test_vague_paste.author, None)
        self.assertEqual(self.test_vague_paste.email, None)
        self.assertEqual(self.test_vague_paste.private, False)
        self.assertEqual(self.test_vague_paste.pub_date, thisnow)
        self.assertEqual(self.test_vague_paste.del_date, thisnow)
        self.assertEqual(self.test_private.private, True)
                
    def testSave(self):
        self.test_full_paste.save()
        self.test_vague_paste.save()
        self.test_private.save()
        
    def testUnicode(self):
        self.assertEqual(self.test_full_paste.__unicode__(), "Testing")
        self.assertEqual(self.test_vague_paste.__unicode__(), None)
        
    def testGet_absolute_url(self):
        self.assertEqual(self.test_full_paste.get_absolute_url(), "/pastey/1")
        self.assertEqual(self.test_vague_paste.get_absolute_url(), "/pastey/" + str(self.test_vague_paste.id))
      
    def testDelete(self):
        self.test_full_paste.delete()
        self.test_vague_paste.delete()
        self.test_private.delete()
        
    #test views
    def test_details(self):       
        
        detail_response = self.client.post('/pastey/', {'code_paste' : 'text'}, follow=True)
        
        self.assertRedirects(detail_response, "/pastey/4/", status_code=302, target_status_code=200)
        self.assertEqual(detail_response.context['paste'].title, "Untitled Submission")
        
        #Delete the file that gets created amidst the actual user data files
        del_response = self.client.post('/pastey/4/', {'delete': None}, follow = True)           
       
    def test_index(self):
        index_response = self.client.get('')
        index_response = self.client.get('/pastey/')
    

class CodeFormTestCase(TestCase):
    def setUp(self):
        self.test_paste1 = CodeForm()
        
    def testSave(self):
        self.assertTrue(self.test_paste1.save())
        self.assertTrue(self.test_paste1.file_delete())
        
        
class FactoryTest(TestCase):
    def setUp(self):
        #provide factory for all tests
        self.factory = RequestFactory()        
        self.client = Client()#needed for detail page creation
        
    def test_index(self):       
        request = self.factory.get('/pastey/')
        response = index(request)
        self.assertEqual(response.status_code, 200)
        
    def test_empty_list(self):
        #database is empty, the list should still display a page stating that
        request = self.factory.get('/pastey/list/')
        response =  list_page(request, 1)
        self.assertEqual(response.status_code, 200)
    
    def test_detail(self):
        #create a paste

        detail_response = self.client.post('/pastey/', {'code_paste' : 'text'}, follow=True)

        request = self.factory.get('/pastey/1/')
        response = detail(request, 1)
        self.assertEqual(response.status_code, 200)
        
        #Delete the file that gets created amidst the actual user data files
        del_response = self.client.post('/pastey/1/', {'delete': None})           
        

