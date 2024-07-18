import os
import unittest
from flaskapi import app
from itertools import product

class aniani(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        
    def tearDown(self):
        pass

    '''
    def test_addReflectivityMeasurement(self):

        telescope_num = [1, 2]
        measurment_type = ['T', 'S', 'D', 't', 'd', 's']
        mirror = ['primary', 'secondary', 'tertiary', 'PRIMARY', 'SECONDARY']
        segment_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 36, None]
        mirror_type = ["1", "2", "3", "4", "5", "6", "A", "B", "C"]
        measured_date = ['20240717']
        install_date = ['20240717']
        sample_status = ["clean", "dirty"]
        segment_position = [1, 2, 3, 4, 5, 6, 7, 36, None]
        spectrum = ["400-540", "480-600", "590-720", "900-1100"]
        measurement_type = ["T", "S", "D"]
        reflectivity = [0.923842, 0.838546, None, 0]
        notes = [None, 'testing']

        tests = list(product(telescope_num, measurment_type, mirror, segment_id, mirror_type, measured_date, install_date, sample_status, segment_position,))
    '''
    
    def test_get_current(self):

        tel_num_values = [1, 2]
        measurment_type_values = ['T', 'S', 'D', 't', 'd', 's']
        mirror_values = ['primary', 'secondary', 'tertiary', 'PRIMARY', 'SECONDARY']

        tests = list(product(tel_num_values, measurment_type_values, mirror_values))

        for tel_num, measurement_type, mirror in tests:

            query_string = {'tel_num': tel_num, 'measurement_type': measurement_type, 'mirror': mirror}
            response = self.client.get('/getCurrent', query_string=query_string)

            self.assertEqual(response.status_code, 200)
        
            msg = response.json

            if isinstance(msg, list):
                if len(msg)>0:
                    self.assertNotEqual(msg[0].get('status'), 'ERROR')


    def test_get_current_extraneous(self):

        tel_num_values = [4, 't']
        measurment_type_values = ['t', 'd', 's', 1]
        mirror_values = [1, 'p', 's', 'prime', 'three']

        tests = list(product(tel_num_values, measurment_type_values, mirror_values))

        for tel_num, measurement_type, mirror in tests:
            # print('GET CURRENT EXT: ****** TESTING: ******', tel_num, measurement_type, mirror)

            query_string = {'tel_num': tel_num, 'measurement_type': measurement_type, 'mirror': mirror}
            response = self.client.get('/getCurrent', query_string=query_string)

            self.assertEqual(response.status_code, 500)
        
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
            response = self.client.get('/getPredicts', query_string=query_string)

            self.assertEqual(response.status_code, 200)
            
            msg = response.json

            if isinstance(msg, list):
                if len(msg)>0:
                    self.assertNotEqual(msg[0].get('status'), 'ERROR')
    
        

if __name__ == '__main__':


    unittest.main()