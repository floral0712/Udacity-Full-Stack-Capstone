import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Order, Dessert
from sqlalchemy import desc

# Create dict with Authorization key and Bearer token as values.
# Later used by test classes as Header

cafe_manager_auth_header = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il94Snd3akdSM1N3ODFWaFFxRmZ4ZCJ9.eyJpc3MiOiJodHRwczovL2Z1bGxzdGFja2xlYXJuaW5nLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjAzMzVhYTcxNDY4YzAwMTNmZmU4N2IiLCJhdWQiOiJkZXNzZXJ0IiwiaWF0IjoxNTk4NDA2MjcwLCJleHAiOjE1OTg0MTM0NzAsImF6cCI6IjVoM0phYkMxUVhCRmtQbEJCWEhBdzJzMzJHMmd4MmI3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6IGRlc3NlcnRzIiwiZ2V0Om9yZGVycyIsInBhdGNoOiBkZXNzZXJ0cyIsInBvc3Q6IGRlc3NlcnRzIiwicG9zdDogb3JkZXJzIl19.gs_b8UIy9_qpxVBTxzYneBfCv5J2oqNPSqFsvhtiO5raEgoc-kWZPhYYWvZn-zf005RWMj8QpvhsdPbwDtt4iJFgGTzdVoHDypyw6ZRw6AyO1tX-LOT_Prjq_uZHpvVrHnU_xlzJU7H6Z9V-qxzbHkKpKZm38hw2gICsLxDOOZnQRG4bSSn05KfJqEqZXXD56HTovDcng6jc-cwKQS8034H9vxe6SuL-Tq2zsCaXPnaUM1TZ2sJAOryH6J-weBaiR2Uqpi287yOGEM9ttFTlSRM1MA6r4tevEhLyTn7-BAK5nUlWT9Ch6cTU8HpYoq-ZHXy0NaUs7MqpLQHjq3yzFQ"
}

customer_auth_header = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il94Snd3akdSM1N3ODFWaFFxRmZ4ZCJ9.eyJpc3MiOiJodHRwczovL2Z1bGxzdGFja2xlYXJuaW5nLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNDc2ODA2Mzk5NjQ0MTAxODUyNiIsImF1ZCI6WyJkZXNzZXJ0IiwiaHR0cHM6Ly9mdWxsc3RhY2tsZWFybmluZy51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk4NDA2NTAwLCJleHAiOjE1OTg0MTM3MDAsImF6cCI6IjVoM0phYkMxUVhCRmtQbEJCWEhBdzJzMzJHMmd4MmI3Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDpvcmRlcnMiLCJwb3N0OiBvcmRlcnMiXX0.W3OsxLHnpXStkzlSkJyYhndb_aB_A6Dk-rZE7dzKS1RJ5jpRLdOxQt3Bs-DDuuySgGx2ZwBvrfj_rhFaPz8k8UkBvnC1dsJr0edWMjPU3ooZxYl_7KUgSTL5UcSOI8U12SkIkMZstFD_DAQlO1RAykPgMNSolKFwbo5cgzA6Lx66DX7PM4uuM0v7LmMIFxIJSyGz5JoLZ0wtKD_Y-Sb3jic7eEa5IzjwCunzRbISPhH_SfmxA-XU4k7GTLBa0GrQ2xUZV04gY4au9-6JHDRoY1FsVnSx4JdJJb2EjtnxaXqSpcJDkp8-mLnVQxIDf2Lewx75UzWTfY8RwfD-Yp6Ecg"
}


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgres://{}/{}".format(
            'yaoxiao@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

# Test driven development (TDD): Create testcases first, then add endpoints to pass tests

#----------------------------------------------------------------------------#
# Tests for /desserts GET and POST
#----------------------------------------------------------------------------#

    def test_get_desserts(self):
        response = self.client().get('/desserts')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_dessert(self):
        """Test POST new dessert."""

        json_create_dessert = {
            'name': 'cookie',
            'price': 2.0
        }

        desserts_before = Dessert.query.all()
        response = self.client().post('/desserts', json=json_create_dessert,
                                      headers=cafe_manager_auth_header)
        data = json.loads(response.data)
        desserts_after = Dessert.query.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(desserts_after) - len(desserts_before) == 1)

    def test_create_wrong_format_dessert(self):
        """ Test POST new dessert with wrong input """
        desserts_before = Dessert.query.all()
        response = self.client().post('/desserts', json={}, headers=cafe_manager_auth_header)
        data = json.loads(response.data)
        desserts_after = Dessert.query.all()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(len(desserts_after) - len(desserts_before) == 0)


#----------------------------------------------------------------------------#
# Tests for /desserts PATCH
#----------------------------------------------------------------------------#

    def test_edit_dessert(self):
        """Test PATCH existing dessert"""
        edit_dessert_with_new_price = {
            'price': 10.0
        }
        res = self.client().patch('/desserts/4', json=edit_dessert_with_new_price,
                                  headers=cafe_manager_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['updated_dessert']) > 0)

    def test_edit_dessert_without_one(self):
        """Test PATCH non-exsting dessert"""
        edit_dessert_with_new_price = {'price': 10.0}

        res = self.client().patch('/desserts/100', json=edit_dessert_with_new_price,
                                  headers=cafe_manager_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_edit_dessert_with_wrong_input(self):
        """Test PATCH dessert with a wrong input"""
        res = self.client().patch('/desserts/4', json={}, headers=cafe_manager_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


#----------------------------------------------------------------------------#
# Tests for /desserts DELETE
#----------------------------------------------------------------------------#


    def test_delete_dessert_without_permission(self):
        """Test DELETE existing dessert with missing permissions"""
        res = self.client().delete('/desserts/11', headers=customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_dessert(self):
        """Test DELETE existing dessert"""
        res = self.client().delete('/desserts/8', headers=cafe_manager_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], )

    def test_delete_non_exsiting_dessert(self):
        """Test DELETE non existing dessert"""
        res = self.client().delete('/deserts/1000', headers=cafe_manager_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


#----------------------------------------------------------------------------#
# Tests for GET /orders
#----------------------------------------------------------------------------#


    def test_get_one_order(self):
        """Test GET one order"""
        res = self.client().get('/orders/1', headers=customer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['order']) > 0)

    def test_get_non_existing_order(self):
        res = self.client().get('/orders/100', headers=customer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


#----------------------------------------------------------------------------#
# Tests for /order POST
#----------------------------------------------------------------------------#

    def test_post_order(self):
        """Test POST an order"""
        new_order = {"customer": "Mary",
                     "items": ["cupcake"]}

        res = self.client().post('/orders', json=new_order, headers=customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['new_order']) > 0)

    def test_post_with_wrong_input(self):
        """Test POST orders with empty json"""
        res = self.client().post('/orders', json={}, headers=customer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


if __name__ == "__main__":
    unittest.main()
