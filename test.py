import os
import unittest
from flaskapi import app
from parameterized import parameterized

class aniani(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        
    def tearDown(self):
        pass


    @parameterized.expand([
    (None, None, None),  # OK
    (None, None, 'primary'), # OK
    (None, None, 'secondary'), # OK
    (None, None, 'tertiary'),

    (1, None, None),  # OK
    (1, None, 'primary'), # OK
    (1, None, 'secondary'), # OK
    (1, None, 'tertiary'),

    (2, None, None),  # OK
    (2, None, 'primary'), # OK
    (2, None, 'secondary'), # OK
    (2, None, 'tertiary'),

    (3, None, None),  # OK
    (3, None, 'primary'), # OK
    (3, None, 'secondary'), # OK
    (3, None, 'tertiary')
    ])

    def test_get_current(self, tel_num, measurement_type, mirror):

        query_string = {'tel_num': tel_num, 'measurement_type': measurement_type, 'mirror': mirror}
        response = self.client.get('/getCurrent', query_string=query_string)

        self.assertEqual(response.status_code, 200)
        
        msg = response.json

        if isinstance(msg, list):
            if len(msg)>0:
                self.assertNotEqual(msg[0].get('status'), 'ERROR')


    '''
    def test_primary_predicts_route(self, tel_num, measurement_type, mirror):

        query_string = {'tel_num': tel_num, 'measurement_type': measurement_type, 'mirror': mirror}
        response = self.client.get('/primaryPredicts', query_string=query_string)

        self.assertEqual(response.status_code, 200)
        
        msg = response.json

        if isinstance(msg, list):
            if len(msg)>0:
                self.assertNotEqual(msg[0].get('status'), 'ERROR')
    '''
        

if __name__ == '__main__':


    unittest.main()