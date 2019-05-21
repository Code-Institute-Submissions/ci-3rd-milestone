# Tasting Experience - Recipes
This project is build upon [The Tasting Experience](https://github.com/Seboeb/ci-1st-milestone) and [The Tasting Experience Finder](https://github.com/Seboeb/ci-2nd-milestone) project. At The Tasting Experience website you can book a cultural tasting for your friends or beloved ones and at the Tasting Finder website you can find a fancy place to grab some nice drinks. This page allows the fans of The Tasting Experience to find, create and share recipes of some delicous drinks created by the fans!

At [this](https://seboeb.github.io/ci-2nd-milestone/) separate page of The Tasting Experience website you can join The Tasting Experience community!

## UX
The focus of this website is to provide a community platform for the users to share their tasting experiences. You can find recipes for nice drinks or cocktails, but you could also create your own recipes and share them with the rest of the userbase. The website allows to search for specific ingredients, alcoholic percentages, ratings or most viewed drinks.

### User stories
- As a user I want to see a clear overview of the recipes at my dashboard screen.
- As a user I want to be able to signup and subsequently login.
- As a user I am able to upload a profile picture.
- As a user I can select favorite recipes and have a list of them.
- As a user I can delete favorite recipes from my list.
- As a user I can write comments below recipes to share my experience or opinion.
- As a user I can search for specific recipes.
- As a user I can filter recipes by their label or rating.
- As a user I can create and share my own recipe and put labels on them.
- As a user I am able to delete a recipe that was created by myself.
- As a user I am able to edit a recipe that was created by myself.
- As a user I am able to give a rating for recipes I (dis)like. 

## Features
Here you can see the features that are already implemented and which are left to implement in this project.

### Existing Features
The user can:
- Signup for the Tasting Experience community
- Login as a registered user
- Upload a profile picture and edit your personal details
- See a list of all available recipes
- Search for certain recipes based on their label or rating
- Create comments when logged in
- Delete his own comments
- Create new recipes
- Edit his recipes
- Delete his recipes
- Add recipes to his favorite list
- Provide ratings for recipes

### Features Left to Implement
At this moment none.


## Technologies used
This project uses several existing third party technologies to improve code quality and to speed up the development time. The following tools are used:
- **[Python](https://www.python.org/)
    - Python is a programming language that lets you work quickly and integrate systems more effectively
- **[Flask](http://flask.pocoo.org/)**
    - Flask is a microframework for Python based on Werkzeug and Jinja 2. It is used as a webserver for serving the Tasting Experience website.
- **[JQuery](https://jquery.com/)**
    - JQuery makes things like HTML document traversal and manipulation, event handling, animation, and Ajax much simpler with an easy-to-use API that works across a multitude of browsers.
- **[Croppie](https://foliotek.github.io/Croppie/)**
    - Croppie is a fast, easy to use image cropping plugin with tons of configuration options. It provides a way to upload and resize images on screen.
- **[NodeJs](https://nodejs.org/en/)**
    - Node is designed to build scalable network applications. It will be used to run the webpack builder for client JavaScript.
- **[npm](https://www.npmjs.com/)**
    - npm is the package manager for JavaScript and the world’s largest software registry. It will be used to manage all the javaScript dependencies used in this project.
- **[webpack](https://webpack.js.org/)**
    - Webpack is a build tool that puts all of your assets, including JavaScript, images, fonts, and CSS, in a dependency graph.
- **[Handlebars](https://handlebarsjs.com/)**
    - Handlebars provides the power necessary to let you build semantic templates effectively. It is used to improve UX experience during AJAX calls.
- **[MySQL](https://www.mysql.com/)**
    - MySQL is a freely available open source Relational Database Management System (RDBMS) that uses Structured Query Language (SQL). SQL is the most popular language for adding, accessing and managing content in a database.

Additionally, the following webpack modules are used:
- **babel-loader, babel/core, babel/preset-env**
    - These modules are used to convert modern ES6 JavaScript files into robust ES5 JavaScript files which is supported on any browser.
- **handlebars-loader**


## Installing
This project uses NodeJs for managing the Javascript libraries, webpack and a testing webserver. Visite their [website](https://nodejs.org/en/) to install NodeJs for your operation system. NodeJs ships with npm, which will be automatically installed.

In order to install the JavaScript dependecies in this project, please clone the repository to a folder on your computer. Open a terminal (or command prompt) and cd into your cloned folder. Type in the following command:
```
npm install
```
This command will install all the module dependencies that are listed in the package.json file. 

Since the webserver runs on Flask, which is a microframework for Python, it is necessary to install Python from their [website](https://www.python.org/). When installing Python, PIP is automatically installed as well. The latter is a package manager for Python. Open a terminal (or command prompt) and cd into your cloned folder. Type in the following command:
```
pip install -r requirements.txt
```
This command will install all the module dependencies that are listed in the requirements.txt. Please note that the actual install command for PIP may vary based on your OS and Python version. 

This project uses a MySQL database as the backend storage technology. You can run a MySQL server by yourself by using, for instance, the following [docker image](https://hub.docker.com/_/mysql) or by using an online free MySQL service such as [db4free](https://www.db4free.net/). When you have created a MySQL server, please make sure that you update the ```config.json``` file located in the root folder of this repository. This file in necessary in order to connect to you database.

When the MySQL database server is properly installed, the required tables must be created in order for this project to run. You can create the MySQL tables by running the following python script:
```
python setup-db.py
```

Once the tables are created, you are able to run the project by executing the ```app.py``` python script :)!

## Testing
**Database test**
This project uses the build-in assertions from Python in order to test the database connection and its functions. The tests are written in the ```test.py``` Python script and to run the test, simply run the python script.
```
python test.py
```
When the test are successful, you should receive the ```Database tests executed successfully!``` message in your terminal.

**JavaScript test**
When you run the project and navigate with you browser to the website, you can start testing the javascript functions. All the JavaScript functions are written in such a way that possible errors are logged in the console of the browser. When using the Google Chrome browers, you can open the development console and check for network operations and logs in the console while using the The Tasting Experience website.

## Deployment

## Credits

### Media
- Images used in this project are grabbed from [pixabay](https://pixabay.com).
https://best-cocktails-recipes.com/recipe-categories/
https://www.liquor.com/hub/cocktail-recipes/#gs.aa4tem
### Acknowledgements

