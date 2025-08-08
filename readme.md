# Setup
1. Install Dependencies

``` pip install -r requirements.txt ```
2. run the app 

``` python app.py ```
3. default user :
username : user1 , password : password123
username : user2 , password : password321

# Run test 
1. run test

``` pytest test_app.py ```
2. run coverage test

    ``` pytest --cov=auth --cov=models --cov-report=term-missing test_app.py ```
    ![Test coverage](https://github.com/danangwijaya750/mini-flask-be/blob/master/images/image.png)