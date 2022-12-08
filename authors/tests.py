from django.test import TestCase
from .models import single_author
# Create your tests here.
class single_author_TestCase(TestCase):
    def setUp(cls):
        print("First test setup")
        single_author.objects.create(username='TestAuthorCase1', password = 'TestAuthorCaseTest1')
        single_author.objects.create(username='TestAuthorCase2', password = 'TestAuthorCaseTest2')
        single_author.objects.create(username='TestAuthorCase3', password = 'TestAuthorCaseTest3', github = 'www.github.com', display_name = 'test3')

    def test_post_exist(self):
        case1 = single_author.objects.get(username = 'TestAuthorCase1')
        case2 = single_author.objects.get(username = 'TestAuthorCase2')
        case3 = single_author.objects.get(username = 'TestAuthorCase3')
        self.assertEqual(case1.password, 'TestAuthorCaseTest1')
        self.assertEqual(case2.password, 'TestAuthorCaseTest2')
        self.assertEqual(case3.password, 'TestAuthorCaseTest3')
        self.assertEqual(case3.github, 'www.github.com')
        self.assertEqual(case3.display_name, 'test3')
        
    def test_description_not_exist(self):
        case1 = single_author.objects.get(username = 'TestAuthorCase1')
        self.assertEqual(case1.github, '')
        self.assertEqual(case1.display_name, '')
        self.assertEqual(case1.url, '')