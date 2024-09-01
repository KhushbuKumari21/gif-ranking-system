import unittest
from app import app, init_db, track_interaction, fetch_gifs  # Adjust import based on your project structure

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()  # Initialize the database

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search for GIFs', response.data)

    def test_index_post(self):
        response = self.app.post('/', data={'query': 'funny'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GIFs', response.data)

    def test_search_gifs(self):
        response = self.app.get('/search?q=funny')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('gifs', json_data)
        self.assertTrue(len(json_data['gifs']) > 0)

    def test_click(self):
        # You might want to insert a mock GIF into the database before testing
        # and then test if the click functionality works
        response = self.app.get('/click/some-gif-id')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GIF clicked!', response.data)

if __name__ == '__main__':
    unittest.main()
