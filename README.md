# Tasting Experience - Recipes
This project is build upon [The Tasting Experience](https://github.com/Seboeb/ci-1st-milestone) and [The Tasting Experience Finder](https://github.com/Seboeb/ci-2nd-milestone) project. At The Tasting Experience website you can book a cultural tasting for your friends or beloved ones and at the Tasting Finder website you can find a fancy place to grab some nice drinks. This page allows the fans of The Tasting Experience to find, create and share recipes of some delicous drinks created by the fans!

At [this](http://the-tasting-experience.herokuapp.com/) separate page of The Tasting Experience website you can join The Tasting Experience community!

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
- **[Python](https://www.python.org/)**
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

## Database model
This project uses a SQL type database and MySQL to be specific. [Here](https://www.mysql.com/) you can find more about MySQL. This project uses the following database tables:
- **Users**
    - In this table the information about the user is stored, e.g. name, email, password.
- **Recipes**
    - In this table the information of a recipe is stored, e.g. title, description, labels.
- **Comments**
    - This table holds all the comments of users.
- **Ratings**
    - User can provide ratings to certain recipes. These ratings are stored in this table.
- **Labels**
    - This project uses several labels that can be assigned to recipes. Labels are stored in this table.
- **Label_recipe**
    - This is an intermediate table that connects the many-to-many relationship of the labels en recipes together.
- **Favorites**
    - This table stores the favorite recipes assigned by users.

A detailed overview of the table structure and data types can be seen in the [database_schema](https://github.com/Seboeb/ci-3rd-milestone/tree/master/database_schema) folder.

## Installing
This project uses NodeJs for managing the Javascript libraries, webpack and a testing webserver. Visite their [website](https://nodejs.org/en/) to install NodeJs for your operation system. NodeJs ships with npm, which will be automatically installed.

In order to install the JavaScript dependecies in this project, please clone the repository to a folder on your computer. Open a terminal (or command prompt) and cd into your cloned folder. Type in the following command:
```
npm install
```
This command will install all the module dependencies that are listed in the package.json file. 

Since the webserver runs on Flask, which is a microframework for Python, it is necessary to install Python from their [website](https://www.python.org/). When installing Python, pip is automatically installed as well. The latter is a package manager for Python. Open a terminal (or command prompt) and cd into your cloned folder. Type in the following command:
```
pip install -r requirements.txt
```
This command will install all the module dependencies that are listed in the requirements.txt. Please note that the actual install command for pip may vary based on your OS and Python version. 

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
When you run the project and navigate with your browser to the website, you can start testing the javascript functions. All the JavaScript functions are written in such a way that possible errors are logged in the console of the browser. When using the Google Chrome browers, you can open the development console and check for network operations and logs in the console while using the The Tasting Experience website.

## Deployment
This project is deployed using Heroku and can be seen over [here](http://the-tasting-experience.herokuapp.com/). Heroku is a cloud platform as a service supporting several programming languages. 

Follow the following steps to deploy this project to Heroku by yourself:

1. Create a Heroku account over [here](https://signup.heroku.com).
2. Create a new app and give it a name.
3. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
4. Open a terminal and login to heroku by using the ```heroku login``` command.
5. When successfully logged in, we have to add the remote heroku git repository. In the terminal, navigate to the root folder of your project. When git is not initialize, initialize it with ```git init```. In order to add the remote heroku repository you first have to navigate to the settings of your Heroku application. Under 'Info' you will find your Heroku Git URL (see image below). Copy this git url and execute the following command to add this remote repository to your local git.
```
git remote add heroku https://git.heroku.com/the-tasting-experience.git
```
6. Make sure that you have included a ```requirements.txt``` and a ```Procfile``` in your projects root folder. An example ```Procfile``` can be found in the source files of this project. 
7. If you do not have an up-to-date ```requirements.txt``` file, create it using the following command:
```
pip freeze > requirements.txt
```
8. Now it is time to push your local git repository to your remote Heroku git repository by using the command below. Please note that ```master``` represents the git branche you want to push.
```
git push -u heroku master
```
9. The application is almost ready to be used on Heroku. Go to the settings tab and make sure you set the Config Vars. These variables are the environment parameters required for the application in order to run. Restart of the dyno may be necessary. See the image below which variables are required.

![heroku settings](https://github.com/Seboeb/ci-3rd-milestone/blob/master/static/images/heroku-settings.png)

## Developing
If you want to continue developing this project, you can do so by cloning this git repository. Make sure you install the project (see Installing) with the help of npm and pip. Make sure you configure the ```config.json``` file. The webpack config file is already good to go and does not need additional tweaks (but you can if you want). 

The main application file is ```app.py```. All the Flask routes can be found in the ```routes``` folder. The database files and some extra python librabries are located in the ```lib``` folder. The JavaScript, css and images are located in the ```static``` folder, as this folder is statically served by Flask. The html files have their own ```templates``` folder.

In order to build the JavaScript files using webpack, run the following command:
```
npm run build
```
and for production run:
```
npm run build-prod
```

If you want to write your own testing cases, please add them to the ```test.py``` file located in the root folder.

## Credits
Find below the sources used for this project. 
### Media
- Images used in this project are grabbed from [pixabay](https://pixabay.com).
- Recipes are used from [Best Cocktails Recipes](https://best-cocktails-recipes.com/) and [Liqour.com](https://www.liquor.com/)

### Acknowledgements
- A good introduction tutorial that I followed for webpack was provided by the Academind [videos](https://www.youtube.com/watch?v=GU-2T7k9NfI&list=PL55RiY5tL51rcCnrOrZixuOsZhAHHy6os).
