from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Post


class BlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='user'
        )
        cls.pub_post = Post.objects.create(
            title='title1',
            text='text1',
            status=Post.STATUS_CHOICES[0][0],
            author_message='message1',
            author=cls.user
        )
        cls.drf_post = Post.objects.create(
            title='title2',
            text='text2',
            status=Post.STATUS_CHOICES[1][0],
            author_message='message2',
            author=cls.user
        )

    #     checking if url names are correct and all pages available
    def test_home_url_name_not_changed(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_url_name_not_changed(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_contact_url_name_not_changed(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_login_url_name_not_changed(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_url_name_ok(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    #   checking if published post exists in home page

    def test_pub_post_is_in_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'title1')
        self.assertContains(response, 'text1')
        self.assertContains(response, self.user)

    #     checking if draft post does not exist in home page

    def test_drf_post_is_not_in_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'title2')
        self.assertNotContains(response, 'text2')

    # checking that detail page exists for published post

    def test_detail_exists_for_pub_post(self):
        response = self.client.get(reverse('detail', args=[self.pub_post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pub_post.title)
        self.assertContains(response, self.pub_post.text)
        self.assertContains(response, self.pub_post.author)
        self.assertContains(response, self.pub_post.author_message)

    #     checking if draft posts doesn't shown in home page

    def test_drf_post_does_not_shown_in_home(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, self.drf_post.title)
        self.assertNotContains(response, self.drf_post.text)

    #         checking that detail page doesn't exist for unknown post

    def test_detail_does_not_exist_for_unknown_post(self):
        response = self.client.get(reverse('detail', args=[2000]))
        self.assertEqual(response.status_code, 404)

    # checking if create post works

    def test_edit_works(self):
        response1 = self.client.post(reverse('new_post'), {
            'title': 'title3',
            'text': 'text3',
            'status': Post.STATUS_CHOICES[0][0],
            'author': self.user.id,
            'author_message': 'message3',
        })
        response2 = self.client.post(reverse('new_post'), {
            'title': 'title4',
            'text': 'text4',
            'status': Post.STATUS_CHOICES[1][0],
            'author': self.user.id,
            'author_message': 'message4',
        })
        response = self.client.get(reverse('home'))

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

    #        checking if edit works

    def test_edit_works(self):
        response = self.client.post(reverse('edit_post', args=[self.pub_post.id]), {
            'title': 'TITLE1',
            'text': 'TEXT1',
            'status': Post.STATUS_CHOICES[0][0],
            'author': self.user.id,
            'author_message': 'MESSAGE1',
        })

        self.assertEqual(response.status_code, 302)


    #         checking if delete works

    def test_delete_works(self):
        response = self.client.post(reverse('delete_post', args=[self.drf_post.id]))
        self.assertEqual(response.status_code, 302)
