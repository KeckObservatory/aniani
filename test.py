import os
import unittest
from flaskapi import app
from itertools import product
import db_conn
from aniani_functions import create_db_connection

class aniani(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

        self.connection = create_db_connection()
        
    def tearDown(self):
        pass
        #self.connection.query("DELETE FROM MirrorSamples WHERE notes = 'testing'")

    def test_get_all_samples(self):

        telescope_num_values = [1, 2]
        measurment_type_values = ['T', 'S', 'D', 't', 'd', 's']
        mirror_values = ['primary', 'secondary', 'tertiary', 'PRIMARY', 'SECONDARY']

        tests = list(product(telescope_num_values, measurment_type_values, mirror_values))

        for test in tests:
            #print('GET ALL SAMPLES: ****** TESTING: ******', test)

            query_string = {'telescope_num': test[0], 'measurement_type': test[1], 'mirror': test[2]}

            response = self.client.get('/getAllSamples', query_string=query_string)

            self.assertEqual(response.status_code, 200)
        
            msg = response.json

            if isinstance(msg, list):
                if len(msg)>0:
                    self.assertNotEqual(msg[0].get('status'), 'ERROR')


    
    def test_add_Reflectivity_Measurement(self):

        telescope_num = [1, 2]
        measurement_type = ['T', 'S', 'D']
        mirror = ['primary', 'secondary', 'tertiary', 'PRIMARY']
        segment_id = [1, 2, 3, 4, 10, 36]
        mirror_type = ["1", "2", "A", "B", "C"]
        measured_date = ['20240717']
        install_date = ['20240717']
        sample_status = ["clean", "dirty"]
        segment_position = [1, 2, 3, 7, 10, 36 ]
        spectrum = ["400-540", "480-600", "590-720", "900-1100"]
        reflectivity = [0.923842, 0.838546, 0]
        notes = ['testing']

        tests = list(product(telescope_num, measurement_type, mirror, segment_id, mirror_type, measured_date, install_date, sample_status, segment_position, spectrum, reflectivity, notes))

        for test in tests:
            print('ADD REFLECTIVITY: ****** TESTING: ******', test)

            query_string = {

                "telescope_num": test[0],
                "measurement_type": test[1],
                "mirror": test[2],
                "segment_id": test[3],
                "mirror_type": test[4],
                "measured_date": test[5],
                "install_date": test[6],
                "sample_status": test[7],
                "segment_position": test[8],
                "spectrum": test[9],
                "reflectivity": test[10],
                "notes": test[11]
            }

            response = self.client.get('/addReflectivityMeasurement', query_string=query_string)

            self.assertEqual(response.status_code, 200)
        
            msg = response.json

            if isinstance(msg, list):
                if len(msg)>0:
                    self.assertNotEqual(msg[0].get('status'), 'ERROR')

            # Verify the data was inserted
            rows_added = self.connection.query( "SELECT * FROM MirrorSamples WHERE notes = 'testing")
        
        assertEqual(rows_added == len(tests))

        self.connection.query("DELETE FROM MirrorSamples WHERE notes = 'testing'")
    

    def test_get_current_reflectivity(self):

        telescope_num_values = [1, 2]
        measurment_type_values = ['T', 'S', 'D', 't', 'd', 's']
        mirror_values = ['primary', 'secondary', 'tertiary', 'PRIMARY', 'SECONDARY']

        tests = list(product(telescope_num_values, measurment_type_values, mirror_values))

        for telescope_num, measurement_type, mirror in tests:
            #print('GET CURRENT REFLECT: ****** TESTING: ******', telescope_num, measurement_type, mirror)


            query_string = {'telescope_num': telescope_num, 'measurement_type': measurement_type, 'mirror': mirror}
            response = self.client.get('/getCurrentReflectivity', query_string=query_string)

            self.assertEqual(response.status_code, 200)
        
            msg = response.json

            if isinstance(msg, list):
                if len(msg)>0:
                    self.assertNotEqual(msg[0].get('status'), 'ERROR')

    '''
    def test_get_current_reflectivity_extraneous(self):

        telescope_num_values = [4, 't']
        measurment_type_values = ['t', 1]
        mirror_values = [1, 'p', 's', 'prime', 'three']

        tests = list(product(telescope_num_values, measurment_type_values, mirror_values))

        for telescope_num, measurement_type, mirror in tests:
        

            query_string = {'telescope_num': telescope_num, 'measurement_type': measurement_type, 'mirror': mirror}
            response = self.client.get('/getCurrentReflectivity', query_string=query_string)

            self.assertEqual(response.status_code, 500)
        
            msg = response.json

            if isinstance(msg, list):
                if len(msg)>0:
                    self.assertNotEqual(msg[0].get('status'), 'ERROR')
    '''
    
    def test_get_predict_reflectivity(self):

        telescope_num_values = [1, 2]
        measurment_type_values = ['T', 'S', 'D', 't', 'd', 's']
        mirror_values = ['primary', 'secondary', 'tertiary', 'PRIMARY']

        tests = list(product(telescope_num_values, measurment_type_values, mirror_values))

        for telescope_num, measurement_type, mirror in tests:
            print('GET PREDICT REFLECT: ****** TESTING: ******', telescope_num, measurement_type, mirror)

            query_string = {'telescope_num': telescope_num, 'measurement_type': measurement_type, 'mirror': mirror}
            response = self.client.get('/getPredictReflectivity', query_string=query_string)

            self.assertEqual(response.status_code, 200)
            
            msg = response.json

            if isinstance(msg, list):
                if len(msg)>0:
                    self.assertNotEqual(msg[0].get('status'), 'ERROR')
    
        

if __name__ == '__main__':


    unittest.main()