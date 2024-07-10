import os
import unittest
from flaskapi import app
from itertools import product

class aniani(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        
    def tearDown(self):
        pass


    def test_get_current(self):

        tel_num_values = [1, 2, 3, 4, 't']
        measurment_type_values = ['T', 'S', 'D', 't', 'd', 's', 1]
        mirror_values = ['primary', 'secondary', 'tertiary', 'three', 'PRIMARY', 'SECONDARY', 1]

        tests = list(product(tel_num_values, measurment_type_values, mirror_values))

        for tel_num, measurement_type, mirror in tests:
            # print('****** TESTING: ******', tel_num, measurement_type, mirror)

            query_string = {'tel_num': tel_num, 'measurement_type': measurement_type, 'mirror': mirror}
            response = self.client.get('/getCurrent', query_string=query_string)

            self.assertEqual(response.status_code, 200)
        
            msg = response.json

            if isinstance(msg, list):
                if len(msg)>0:
                    self.assertNotEqual(msg[0].get('status'), 'ERROR')


    
    def test_primary_predicts_route(self):

        tel_num_values = [1, 2, 3, 4, 't']
        measurment_type_values = ['T', 'S', 'D', 't', 'd', 's', 1]
        mirror_values = ['primary', 'secondary', 'tertiary', 'three', 'PRIMARY', 'SECONDARY', 1]

        tests = list(product(tel_num_values, measurment_type_values, mirror_values))

        for tel_num, measurement_type, mirror in tests:

            query_string = {'tel_num': tel_num, 'measurement_type': measurement_type, 'mirror': mirror}
            response = self.client.get('/primaryPredicts', query_string=query_string)

            self.assertEqual(response.status_code, 200)
            
            msg = response.json

            if isinstance(msg, list):
                if len(msg)>0:
                    self.assertNotEqual(msg[0].get('status'), 'ERROR')
    
        

if __name__ == '__main__':


    unittest.main()