# FSND-Capstone-Project

Heroku link: (https://dessertcafe.herokuapp.com/)

## Getting Started
Installing Dependencies
run the following code in the terminal under working directory
`pip install - r requirements.txt`
This will install all required packages



## Running the server
To run the server locally, under working directory , run

```
export FLASK_APP=app.py
flask run --reload
```

## Roles and Permissions
Manager
- post:dessert
- patch:dessert
- delete: dessert
- get: order
- post: order

Customer
- get: order
- post: order

    

## API Reference

### End Points 

Get /
- connect to root endpoint to check if the api is up and running
- requires no authentication
- return 
'Hello, Welcome to Evie's cafe, Enjoy dessert!'

GET /desserts
- display all desserts in Dessert table
- return example
- return no authentication

```
{"desserts":[{"dessert":"brownie","id":1,"price":"5.0"},{"dessert":"cupcake","id":2,"price":"3.0"}],"success":true}
```

POST /desserts
- create a dessert and insert into Dessert table
- sample curl request:
```
curl -X POST -H "Content-Type: application/json" -d '{"name": "cupcake","price":3.0}' http://127.0.0.1:5000/desserts
```

- return example
```
{"created_dessert":{"dessert":"cupcake","id":2,"price":"3.0"},"success":true}
```

PATCH /dessert/<dessert_id>
- update the information for a dessert
- sample curl request:
```
curl http://127.0.0.1:5000/desserts/1 -X PATCH -H "Content-Type: application/json" -d '{"price":2}'
```
- return example
```
{"success":true,"updated_dessert":{"dessert":"brownie","id":1,"price":"2.0"}}
```

DELETE /dessert/<dessert_id>
- delete a dessert from database
- sample curl request:
```
curl http://127.0.0.1:5000/desserts/1 -X DELETE
```
- return example
```
{"deleted":1,"success":true}
```

POST /orders
- create an order
- sample curl request:
```
curl -X POST -H "Content-Type: application/json" -d '{"customer": "Mary","items":["cupcake","carrot cake"]}' http://127.0.0.1:5000/orders
```
- return example:
{"new_order":{"customer":"Mary","dessert":["carrot cake","cupcake"]},"success":true}


GET /order/<order_id>
- get information of an order
- return example
```
{"order":{"customer":"Mary","dessert":["carrot cake","cupcake"]},"success":true}
```

## Testing
To run test, run `python test.py` under working directory. 
