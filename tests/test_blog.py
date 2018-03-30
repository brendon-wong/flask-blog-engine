# File name should be test_file.py
# Begin function names with test_ so pytest automatically runs them

import os
import tempfile

import pytest

from flask_blog_engine import blog

@pytest.fixture
def client():
    db_fd, blog.app.config['DATABASE'] = tempfile.mkstemp()
    blog.app.config['TESTING'] = True
    client = blog.app.test_client()
    with blog.app.app_context():
        blog.init_db()
    yield client
    os.close(db_fd)
    os.unlink(blog.app.config['DATABASE'])
    
def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data
    
def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)
    
def logout(client):
    return client.get('/logout', follow_redirects=True)
    
def test_login_logout(client):
    """Make sure login and logout works"""
    rv = login(client, blog.app.config['USERNAME'],
               blog.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data
    rv = login(client, blog.app.config['USERNAME'] + 'x',
               blog.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    rv = login(client, blog.app.config['USERNAME'],
               blog.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data
    
def test_messages(client):
    """Test that messages work"""
    login(client, blog.app.config['USERNAME'],
          blog.app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
