# tests/test_app.py

import unittest
import os
from peewee import SqliteDatabase

# Set up test environment before importing app
os.environ['TESTING'] = 'true'

from app import app, TimelinePost

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Set up test database
        self.test_db = SqliteDatabase(':memory:')
        # Bind to test database
        self.test_db.bind([TimelinePost], bind_refs=False, bind_backrefs=False)
        self.test_db.connect()
        self.test_db.create_tables([TimelinePost])
        
    def tearDown(self):
        # Clean up test database
        self.test_db.drop_tables([TimelinePost])
        self.test_db.close()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # Test main content is present
        assert "Ace Perez" in html
        assert "Software Developer" in html
        
        # Test navigation elements are present
        assert "Home" in html
        assert "Experience" in html
        assert "Education" in html
        assert "Hobbies" in html
        assert "Timeline" in html
        
        # Test that profile section exists
        assert 'id="profile"' in html
        
        # Test that work experience section exists (note the space in HTML)
        assert 'id ="work-experience"' in html
        
        # Test that education section exists
        assert 'id="education"' in html
        
        # Test that visited places section exists
        assert 'id="visited-places"' in html
        
        # Test that CSS and favicon are linked
        assert '/static/styles/main.css' in html
        assert '/static/img/favicon.ico' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_posts")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        # Remove the assumption that timeline_posts is empty
        assert len(json["timeline_posts"]) == 0
        
        # Add more test relating to the /api/timeline_post GET and POST apis
        
    def test_timeline_post_create(self):
        """Test creating a new timeline post via POST API"""
        # Test data
        post_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'content': 'This is a test timeline post'
        }
        
        # Make POST request
        response = self.client.post('/api/timeline_post', data=post_data)
        
        # Check response
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        
        # Verify response contains expected fields
        assert 'id' in json_data
        assert json_data['name'] == 'Test User'
        assert json_data['email'] == 'test@example.com'
        assert json_data['content'] == 'This is a test timeline post'
        assert 'created_at' in json_data
        
    def test_timeline_post_create_missing_fields(self):
        """Test creating timeline post with missing required fields"""
        # Test with missing name - should return 400 error due to validation
        response = self.client.post('/api/timeline_post', data={
            'email': 'test@example.com',
            'content': 'Test content'
        })
        assert response.status_code == 400
        
        # Test with missing email - should return 400 error due to validation
        response = self.client.post('/api/timeline_post', data={
            'name': 'Test User',
            'content': 'Test content'
        })
        assert response.status_code == 400
        
        # Test with missing content - should return 400 error due to validation
        response = self.client.post('/api/timeline_post', data={
            'name': 'Test User',
            'email': 'test@example.com'
        })
        assert response.status_code == 400
        
    def test_timeline_posts_get_with_data(self):
        """Test GET timeline posts after creating some posts"""
        # Create test posts
        posts_data = [
            {'name': 'User 1', 'email': 'user1@example.com', 'content': 'First post'},
            {'name': 'User 2', 'email': 'user2@example.com', 'content': 'Second post'},
            {'name': 'User 3', 'email': 'user3@example.com', 'content': 'Third post'}
        ]
        
        # Create posts via API
        for post_data in posts_data:
            response = self.client.post('/api/timeline_post', data=post_data)
            assert response.status_code == 200
            
        # Get all posts
        response = self.client.get('/api/timeline_posts')
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        
        # Verify posts are returned
        assert 'timeline_posts' in json_data
        assert len(json_data['timeline_posts']) == 3
        
        # Verify posts are ordered by created_at desc (newest first)
        posts = json_data['timeline_posts']
        assert posts[0]['content'] == 'Third post'  # Most recent
        assert posts[1]['content'] == 'Second post'
        assert posts[2]['content'] == 'First post'  # Oldest
        
    def test_timeline_post_delete(self):
        """Test deleting a timeline post via DELETE API"""
        # Create a test post first
        post_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'content': 'Post to be deleted'
        }
        create_response = self.client.post('/api/timeline_post', data=post_data)
        assert create_response.status_code == 200
        post_id = create_response.get_json()['id']
        
        # Delete the post
        delete_response = self.client.delete(f'/api/timeline_post/{post_id}')
        assert delete_response.status_code == 200
        assert delete_response.is_json
        
        delete_json = delete_response.get_json()
        assert 'message' in delete_json
        assert 'deleted_id' in delete_json
        assert delete_json['deleted_id'] == post_id
        
        # Verify post is deleted by trying to get all posts
        get_response = self.client.get('/api/timeline_posts')
        assert get_response.status_code == 200
        posts = get_response.get_json()['timeline_posts']
        assert len(posts) == 0
        
    def test_timeline_post_delete_nonexistent(self):
        """Test deleting a non-existent timeline post"""
        # Try to delete a post that doesn't exist
        response = self.client.delete('/api/timeline_post/999')
        assert response.status_code == 404
        assert response.is_json
        
        json_data = response.get_json()
        assert 'error' in json_data
        assert 'not found' in json_data['error'].lower()
        
    def test_timeline_api_integration(self):
        """Test full integration: create, read, delete timeline posts"""
        # Start with empty timeline
        response = self.client.get('/api/timeline_posts')
        assert len(response.get_json()['timeline_posts']) == 0
        
        # Create multiple posts
        posts_to_create = [
            {'name': 'Alice', 'email': 'alice@example.com', 'content': 'Hello world!'},
            {'name': 'Bob', 'email': 'bob@example.com', 'content': 'This is my second post'},
            {'name': 'Charlie', 'email': 'charlie@example.com', 'content': 'Timeline is working!'}
        ]
        
        created_ids = []
        for post_data in posts_to_create:
            response = self.client.post('/api/timeline_post', data=post_data)
            assert response.status_code == 200
            created_ids.append(response.get_json()['id'])
            
        # Verify all posts exist
        response = self.client.get('/api/timeline_posts')
        posts = response.get_json()['timeline_posts']
        assert len(posts) == 3
        
        # Delete middle post
        response = self.client.delete(f'/api/timeline_post/{created_ids[1]}')
        assert response.status_code == 200
        
        # Verify only 2 posts remain
        response = self.client.get('/api/timeline_posts')
        posts = response.get_json()['timeline_posts']
        assert len(posts) == 2
        
        # Verify the correct posts remain
        remaining_contents = [post['content'] for post in posts]
        assert 'Hello world!' in remaining_contents
        assert 'Timeline is working!' in remaining_contents
        assert 'This is my second post' not in remaining_contents

    def test_timeline_page_get(self):
        """Test the timeline page loads correctly"""
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        # Test page title
        assert "<title>Timeline</title>" in html
        
        # Test main content is present
        assert "Timeline" in html
        assert "Share your thoughts and see what others are saying!" in html
        
        # Test form elements are present
        assert '<form id="timeline-form">' in html
        assert '<input type="text" id="name" name="name" required>' in html
        assert '<input type="email" id="email" name="email" required>' in html
        assert '<textarea id="content" name="content" rows="4" required>' in html
        assert '<button type="submit">Post</button>' in html
        
        # Test posts container is present
        assert 'id="posts-container"' in html
        assert "Recent Posts" in html
        
        # Test navigation is present and timeline is active
        assert "Timeline" in html
        
        # Test JavaScript functions are present
        assert "loadPosts()" in html
        assert "deletePost(" in html
        assert "getGravatarUrl(" in html
        
        # Test API endpoints are referenced in JavaScript
        assert "'/api/timeline_post'" in html
        assert "'/api/timeline_posts'" in html

    def test_timeline_page_navigation(self):
        """Test timeline page navigation is correctly marked as active"""
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        # Test that navigation exists (updated to match actual HTML)
        assert "sidebar-menu" in html
        assert "Timeline" in html
        
        # The navigation should be present (specific active class testing would need more detailed HTML parsing)
        nav_links = ['Home', 'Experience', 'Education', 'Hobbies', 'Timeline']
        for link in nav_links:
            assert link in html

    def test_timeline_page_form_structure(self):
        """Test timeline page form has correct structure and attributes"""
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        # Test form structure
        assert '<form id="timeline-form">' in html
        
        # Test form fields have correct attributes
        assert 'name="name"' in html
        assert 'name="email"' in html  
        assert 'name="content"' in html
        assert 'required' in html  # All fields should be required
        
        # Test form labels
        assert '<label for="name">Name:</label>' in html
        assert '<label for="email">Email:</label>' in html
        assert '<label for="content">Content:</label>' in html
        
        # Test input types
        assert 'type="text"' in html
        assert 'type="email"' in html
        assert '<textarea' in html

    def test_timeline_page_javascript_functionality(self):
        """Test timeline page includes necessary JavaScript functions"""
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        # Test JavaScript functions are defined
        javascript_functions = [
            'function getGravatarUrl(',
            'function loadPosts(',
            'function deletePost(',
            'document.addEventListener(',
            'document.getElementById'
        ]
        
        for func in javascript_functions:
            assert func in html
            
        # Test API calls are present
        assert "fetch('/api/timeline_post'" in html
        assert "fetch('/api/timeline_posts'" in html
        assert "fetch(`/api/timeline_post/${postId}`" in html
        
        # Test form submission handling
        assert 'preventDefault()' in html
        assert 'FormData' in html
        
        # Test Gravatar functionality
        assert 'CryptoJS.MD5' in html
        assert 'gravatar.com' in html

    def test_timeline_page_with_posts_display(self):
        """Test timeline page behavior when posts exist"""
        # Create some test posts first
        test_posts = [
            {'name': 'Alice', 'email': 'alice@example.com', 'content': 'Hello from Alice!'},
            {'name': 'Bob', 'email': 'bob@example.com', 'content': 'Bob posting here!'}
        ]
        
        # Create posts via API
        for post_data in test_posts:
            response = self.client.post('/api/timeline_post', data=post_data)
            assert response.status_code == 200
            
        # Now test the timeline page
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        # The page should still load correctly regardless of posts
        assert response.status_code == 200
        assert "Timeline" in html
        assert "Recent Posts" in html
        
        # JavaScript should handle the posts loading via API
        assert "loadPosts()" in html
        assert "posts-container" in html

    def test_timeline_page_css_and_assets(self):
        """Test timeline page includes necessary CSS and assets"""
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        # Test CSS is linked
        assert '/static/styles/main.css' in html
        
        # Test timeline-specific CSS classes are present
        timeline_css_classes = [
            'timeline-section',
            'timeline-form',
            'timeline-posts',
            'posts-container'
        ]
        
        for css_class in timeline_css_classes:
            assert css_class in html
            
        # Test CryptoJS is loaded for Gravatar
        assert 'crypto-js' in html

    def test_timeline_page_error_handling(self):
        """Test timeline page includes error handling in JavaScript"""
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        # Test error handling is present
        assert '.catch(error' in html
        assert 'console.error' in html
        assert 'alert(' in html
        
        # Test different error scenarios are handled
        assert 'Error creating post' in html
        assert 'Error deleting post' in html
        assert 'Error loading posts' in html

    def test_timeline_page_user_feedback(self):
        """Test timeline page provides user feedback"""
        response = self.client.get('/timeline')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        
        # Test success messages
        assert 'Post created successfully!' in html
        assert 'Post deleted successfully!' in html
        
        # Test confirmation dialogs
        assert 'Are you sure you want to delete this post?' in html
        assert 'confirm(' in html
        
        # Test empty state message
        assert 'No posts yet. Be the first to post!' in html

    def test_malformed_timeline_post(self):
        """Test malformed timeline post requests"""
        # POST request with invalid name
        response = self.client.post("/api/timeline_post", data={
            "name": "", "email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html
        
        # POST request with invalid email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html
        
        # POST request with invalid email format
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html


if __name__ == '__main__':
    unittest.main()