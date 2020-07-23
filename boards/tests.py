from django.test import TestCase
from django.urls import reverse, resolve
from boards.views import home, board_topics
from boards.models import Board


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Write only about django here.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'board_id': self.board.id})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='You can write anything about django in here.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'board_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'board_id': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/board_topics/1')
        self.assertEqual(view.func, board_topics)

    def test_board_topics_view_contain_link_back_to_home_page(self):
        home_page_url = reverse('home')
        board_topics_url = reverse('board_topics', kwargs={'board_id': self.board.id})
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(home_page_url))
