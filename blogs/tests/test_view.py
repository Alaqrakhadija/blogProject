from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blogs.models import Blogger, Blog


class BlogListViewTest(TestCase):
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='1234')
        test_user.save()
        test_blogger = Blogger.objects.create(user=test_user, bio="hello")
        for blog_num in range(13):
            Blog.objects.create(title='blog_tes %s' % blog_num, blogger=test_blogger, description='hell %s' % blog_num)

    def test_view_url_at_desired_location(self):
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get('/blog/blogs/')
        self.assertTemplateUsed(response, 'blogs/blog_list.html')

    def test_view_pagination_is_five(self):
        response = self.client.get('/blog/blogs/')
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['blog_list']), 5)
