import unittest

from peewee import SqliteDatabase

from app import TimelinePost

MODELS = [TimelinePost]
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind models to test database
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
    
    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()
    
    def test_timeline_post_creation(self):
        """Test creating timeline posts"""
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='This is a test post')
        self.assertEqual(first_post.id, 1)
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='This is another test post')
        self.assertEqual(second_post.id, 2)

    def test_timeline_post_retrieval(self):
        """Test retrieving timeline posts"""
        # Create test posts
        TimelinePost.create(name='John Doe', email='john@example.com', content='This is a test post')
        TimelinePost.create(name='Jane Doe', email='jane@example.com', content='This is another test post')
        
        # Test retrieving posts
        posts = list(TimelinePost.select().order_by(TimelinePost.id))
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].name, 'John Doe')
        self.assertEqual(posts[1].name, 'Jane Doe')
        self.assertEqual(posts[0].content, 'This is a test post')
        self.assertEqual(posts[1].content, 'This is another test post')

    def test_timeline_post_deletion(self):
        """Test deleting timeline posts"""
        # Create test posts
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='This is a test post')
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='This is another test post')
        
        # Test deleting a post
        first_post.delete_instance()
        posts = list(TimelinePost.select())
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].name, 'Jane Doe')
        self.assertEqual(posts[0].content, 'This is another test post')

    def test_timeline_post_fields(self):
        """Test timeline post field validation"""
        post = TimelinePost.create(name='Test User', email='test@example.com', content='Test content')
        self.assertEqual(post.name, 'Test User')
        self.assertEqual(post.email, 'test@example.com')
        self.assertEqual(post.content, 'Test content')
        self.assertIsNotNone(post.created_at)
        
if __name__ == '__main__':
    unittest.main()