from django.utils import unittest

class CodeTestCase(unittest.TestCase):
    def setUp(self):
        self.test_full_paste = Code.objects.create(
            title = "Testing", 
            code_paste = "def testing(sys.argv[[1]):",
            author = "Caleb-via-ASUS",
            email = "caleb.smithnc@gmail.com",
            private = False,
            language = "python",
            )
        self.test_vague_paste = Code.objects.create(
            code_paste = "small code",            
            )
        self.test_private = Code.objects.create(
            code_paste = "some private code",
            private = True,
            author = "Caleb in private"
            )

#    def testUnicode(self):
#    def testGet_absolute_url(self):


#Django Doc example
"""
class AnimalTestCase(unittest.TestCase):
    def setUp(self):
        self.lion = Animal.objects.create(name="lion", sound="roar")
        self.cat = Animal.objects.create(name="cat", sound="meow")

    def testSpeaking(self):
        self.assertEqual(self.lion.speak(), 'The lion says "roar"')
        self.assertEqual(self.cat.speak(), 'The cat says "meow"')
"""        
        
        
#Code model methods
"""
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/pastey/detail/%i' % self.id
"""
