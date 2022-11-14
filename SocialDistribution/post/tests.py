from django.test import TestCase
from .models import Post
# Create your tests here.

class PostTestCase(TestCase):
    def setUp(cls):
        print("First test setup")
        Post.objects.create(title='TestCase1', content = 'TestCaseTest1')
        Post.objects.create(title='TestCase2', content = 'TestCaseTest2')
        
    def test_post_exist(self):
        case1 = Post.objects.get(title = 'TestCase1')
        case2 = Post.objects.get(title = 'TestCase2')
        self.assertEqual(case1.content, 'TestCaseTest1')
        self.assertEqual(case2.content, 'TestCaseTest2')

    def test_description_not_exist(self):
        case1 = Post.objects.get(title = 'TestCase1')
        self.assertEqual(case1.description, None)

