from django.test import TestCase
from .models import Post
# Create your tests here.
class PostTestCase(TestCase):
    def setUp(self):
        post_a = Post(title='TestCase', content = 'TestCaseTest')
        post_a.save()
        print(post_a.title)