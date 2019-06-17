 # Item-Catalog Web-App
A RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication. It provides a list of items within a variety of categories which comes with CRUD functionality. Authenticated users have the ability to post, edit, and delete their own items.
### Project Overview
This project has one main Python module ```project.py ```which runs the Flask application. A SQL database is created using the ```database_setup.py``` module and you can populate the database with test data using ```datas.py```. The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application. 

### Software Requirements
- [Python](https://www.python.org/)
- [Vagrant](https://www.vagrantup.com/)
- [Virtual Machine](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
- [Git](https://git-scm.com/downloads)

### Tech Stack
- Python
- SQLAlchemy
- Flask
- OAuth2 Authentication
- Developing APIs
- JSON



### Set-Up
**1. Launch the  Vagrant Virtual Machine inside the vagrant sub-directory by       using:**
 ```sh
$ vagrant up
```
**2. Log into your vm by using:**
```sh
$ vagrant ssh
```
**3. Change directory to /vagrant by using:**
```sh
$ cd /vagrant
```
**4. Install the dependencies:**
```sh
$ pip3 install -r requirements.txt
```
**5. Run the server by:**
```sh
$ python project.py
```
**6. Access the application in your browser through:**
```sh
http://localhost:5000/
```

### JSON Endpoints
**1. Displays all the items in the database:**
```sh
/items.json/
```
**2. Displays all the items for a particular category in the database:**
```sh
/items/category/<string:category>.json/
```
**3. Displays data of an item for a given category and item id in the database:**
```sh
/items/category/<string:category>/<int:itemId>.json/
```

