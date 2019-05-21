# Database model

## Users
| Column | Data Type |
| ------ | --------- |
| id  | int NOT NULL AUTO_INCREMENT; PRIMARY KEY  |
| firstname  | varchar(20) DEFAULT NULL  |
| lastname  | varchar(20) DEFAULT NULL  |
| password  | varchar(32) NOT NULL  |
| email  | varchar(50) NOT NULL; UNIQUE  |
| image_path  | varchar(256)  |

## Recipes
| Column | Data Type |
| ------ | --------- |
| id | int NOT NULL AUTO_INCREMENT; PRIMARY KEY |
| user_id | int NOT NULL; FOREIGN KEY; REFERENCES Users |
| title | varchar(32) NOT NULL |
| description | varchar(500) NOT NULL |
| recipe | varchar(500) NOT NULL |
| ingredients | varchar(500) NOT NULL |
| views | int DEFAULT 0 |
| avg_rating | float DEFAULT 0 |
| nr_ratings | int DEFAULT 0 |
| image_path | varchar(256) |
| date_created | TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP |

## Comments
| Column | Data Type |
| ------ | --------- |
| id | int NOT NULL AUTO_INCREMENT; PRIMARY KEY|
| user_id | int NOT NULL; FOREIGN KEY; REFERENCES Users|
| recipe_id | int NOT NULL; FOREIGN KEY; REFERENCES Recipes|
| date | TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP|
| message | varchar(500) NOT NULL|
|  | ON DELETE CASCADE|


## Ratings
| Column | Data Type |
| ------ | --------- |
| id | int NOT NULL AUTO_INCREMENT; PRIMARY KEY|
| user_id | int NOT NULL; FOREIGN KEY; REFERENCES Users|
| recipe_id | int NOT NULL; FOREIGN KEY; REFERENCES Recipes|
| rating | int NOT NULL DEFAULT 0|
|  | ON DELETE CASCADE|

## Labels
| Column | Data Type |
| ------ | --------- |
| id | int NOT NULL AUTO_INCREMENT; PRIMARY KEY|
| name | varchar(20) NOT NULL|


## Label_recipe
| Column | Data Type |
| ------ | --------- |
| id | int NOT NULL AUTO_INCREMENT; PRIMARY KEY|
| recipe_id | int NOT NULL; FOREIGN KEY; REFERENCES Recipes|
| label_id | int NOT NULL; FOREIGN KEY; REFERENCES Labels|
|  | ON DELETE CASCADE |


## Favorites
| Column | Data Type |
| ------ | --------- |
| id | int NOT NULL AUTO_INCREMENT; PRIMARY KEY|
| user_id | int NOT NULL; FOREIGN KEY; REFERENCES Users|
| recipe_id | int NOT NULL; FOREIGN KEY; REFERENCES Recipes|
|  | ON DELETE CASCADE |