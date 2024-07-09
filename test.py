import os
import unittest
from flaskapi import app

class aniani(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        
    def tearDown(self):
        pass
    
    def test_internal_route(self):
        semester='abcd'
        obsid='1234'
        query_string = {'semester': semester, 'obsid': obsid}
        response = self.client.get(f'/my/route/', query_string=query_string)
        self.assertEqual(response.status_code, 200)
        msg = response.json
        if isinstance(msg, list):
            if len(msg)>0:
                self.assertNotEqual(msg[0].get('status'), 'ERROR')


if __name__ == '__main__':
    unittest.main()