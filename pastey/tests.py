import datetime

from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from pastey.models import *
from pastey.views import *
from pastey.pretty import DEFAULT_STYLE

thisnow = datetime.datetime.now()

class CodeTestCase(TestCase):
    #establish some database entries for testing
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
        self.assertEqual(self.test_full_paste.get_absolute_url(), "/pastey/" 
            + str(self.test_full_paste.id))
      
    def testDelete(self):
        self.test_full_paste.delete()
        self.test_vague_paste.delete()
        self.test_private.delete()
        
    #test views
    def test_list(self):
        list_response = self.client.get('/pastey/list/')
        self.assertEqual(list_response.status_code, 200)
        #Does this page contain the most important information such as...
        self.assertTrue(list_response.context['pastes']) #list of paste data
        self.assertTrue(list_response.context['page'])   #a paginator object
        self.assertTrue(list_response.context['form'])   #a search form
        #Does the search return what we should expect?
        qlist = [repr(self.test_full_paste)]
        self.assertQuerysetEqual(Code.objects
            .order_by('-pub_date').filter(title__icontains="Testing"),
            qlist)

    def test_details(self):       
        
        detail_response = self.client.post('/pastey/', 
            {'code_paste' : 'test the textarea'}, follow=True)
            
        #Does this submission redirect the user appropriately?
        self.assertRedirects(detail_response, "/pastey/4/", 
            status_code=302, target_status_code=200)
            
        #Are default values assigned when none are given?
        self.assertEqual(detail_response.context['paste'].title, 
            'Untitled Submission')
        self.assertEqual(detail_response.context['paste'].language, 
             None)
        #Is submitted data received?
        self.assertEqual(detail_response.context['paste'].code_paste,
            'test the textarea')
        
        #Delete the file that gets created amidst the actual user data files
        del_response = self.client.post('/pastey/4/', 
            {'delete': None}, follow = True)
            
    def test_copy(self):
        copy_response = self.client.get('/pastey/edit/1/')
        self.assertEqual(copy_response.status_code, 200)
        #Should contain the test message given in setUp()'s test_full_paste()
        self.assertContains(copy_response, "def testing(sys.argv[[1]):")

    def test_plain(self):
        plain_response = self.client.get('/pastey/plain/1/')
        self.assertEqual(plain_response.status_code, 200)
        self.assertContains(plain_response, "<pre>")
        
    def test_html(self):
        html_response = self.client.get('/pastey/html/1/' 
            + DEFAULT_STYLE + "/")
        self.assertEqual(html_response.status_code, 200)
        self.assertContains(html_response, "<pre>")
        
    def test_pdf(self):
        pdf_response = self.client.get('/pastey/pdf/1/' 
            + DEFAULT_STYLE + "/")
        self.assertEqual(pdf_response.status_code, 200)
        
    def test_download(self):
        #Can the file be downloaded?
        obj = Code.objects.get(pk=1)
        fout = obj.txt_file
        dl_response = self.client.get(str(fout))
        self.assertEqual(dl_response.status_code, 200)
       
    def test_index(self):
        #Can the index page be reached from both '' and '/pastey/'?
        index_response = self.client.get('')
        self.assertEqual(index_response.status_code, 200)
        index_response = self.client.get('/pastey/')
        self.assertEqual(index_response.status_code, 200)
        #Does the index page receive a new paste form, and flag variables?
        self.assertTrue(index_response.context['form'])
        self.assertEqual(index_response.context['err_msg'], False)
        self.assertEqual(index_response.context['editing'], None)       
        #contains a CSRF token in the form
        self.assertContains(index_response, "name='csrfmiddlewaretoken'")        
    
#can we reliably save and delete with custom methods in the CodeForm class?
class CodeFormTestCase(TestCase):
    def setUp(self):
        self.test_paste1 = CodeForm()
        
    def testSave(self):
        self.assertTrue(self.test_paste1.save())
        self.assertTrue(self.test_paste1.file_delete())
        

#double check all views with RequestFactory        
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
        #create a paste for factory testing
        detail_response = self.client.post('/pastey/', {'code_paste' : 'text'},
            follow=True)
            
        #Request factory call as usual now that page exists
        request = self.factory.get('/pastey/1/')
        response = detail(request, 1)
        self.assertEqual(response.status_code, 200)
        
        #Delete the file that gets created amidst the actual user data files
        del_response = self.client.post('/pastey/1/', {'delete': None})           
        

