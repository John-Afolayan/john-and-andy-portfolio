import unittest
import os

os.environ['TESTING'] = 'true'
from app import app 


class AppTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()

  def test_home(self):
    response = self.client.get("/")
    self.assertEqual(response.status_code, 200)
    html = response.get_data(as_text=True)
    self.assertIn("John Afolayan", html)
    self.assertIn('<link rel="stylesheet" href="../static/styles/menubar.css">', html)
  
  def test_timeline(self):
    response = self.client.get('/api/timeline_post')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.is_json)

    json = response.get_json()

    self.assertIn('timeline_posts', json)
    self.assertEqual(len(json['timeline_posts']), 0)

    form = {"name": "Jane", "email": "you.already.know.doe@gmail.com", "content": "Who it is!"}
    response = self.client.post('/api/timeline_post', data = form)
    
    self.assertEqual(response.status_code, 200) 
    self.assertTrue(response.is_json) #this test assumes that every time you post to the api, you get the newly created record in return. 
    self.assertEqual('Jane', response.json['name']) #this test assumes that every time you post to the api, you get the newly created record in return. 
    
    timelinePage = self.client.get('/timeline/')
    self.assertEqual(timelinePage.status_code, 200)
    self.assertIn('<td>Jane</td>', timelinePage.get_data(as_text=True))

    #print(timelinePage.get_data(as_text=True))
  
  def test_malformed_timeline_post(self):
    """ 
      For this TDD I solved the issues on the backend by putting constraints on the endpoint. 
      The requests are not allowed to reach the database if data is missing, i.e name, content, etc. 
      However, a better approach is to add these contraints to the database model it self. 
      Even if this aproach is kept, its always a good idea to add contraints to the database to kelp keep data integrity. 
    """
    form_no_name = { "email": "john@example.com", "content": "Hello world, I'm John!" }
    response = self.client.post("/api/timeline_post", data=form_no_name)

    self.assertEqual(response.status_code, 400)

    html = response.get_data(as_text=True)
    self.assertIn("Invalid name", html)

    form_no_content = {"name": "John Doe", "email": "john@example.com", "content": ""}
    response = self.client.post("/api/timeline_post", data=form_no_content)
    self.assertEqual(response.status_code, 400)
    html = response.get_data(as_text=True)
    self.assertIn('Invalid content', html)

    form_no_email = {"name" : "John Doe",  "email": "not-an-email", "content": "Hello world, I'm John!"}
    response = self.client.post("/api/timeline_post", data=form_no_email)
    self.assertEqual(response.status_code, 400)
    html = response.get_data(as_text=True)
    self.assertIn('Invalid email', html)