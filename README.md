# Foodgram
##### Description
App which destined to cooking lovers, who like diversity of food. You can choose one of many recipes and repeat it on this evening. Also you can start you cooking blog, where you can upload your secret recipe of burger or omelet.
# .env file
```
DB_ENGINE=<specify your DBMS>
DB_NAME=<name of your database>
POSTGRES_USER=<login to connect to the database>
POSTGRES_PASSWORD=<password to connect to the database>
DB_HOST=<name of service>
DB_PORT=<port to connect to the database>
```
# How to launch

1. Clone image foodgram from ```DockerHub``` with command ```docker run <foodgram_image>```
2. Open Docker Desktop
3. In directory ```.../foodgram-project-react/infra``` type command ```docker-compose up``` in bash console
4. Make migrations with command ```docker-compose exec web python manage.py migrate```
5. Make superuser with command ```docker-compose exec web python manage.py createsuperuser```
6. Collect static with command ```docker-compose exec web python manage.py collectstatic --no-input```
7. Load data from fixtures with command ```loaddata <name_db>.json```
8. Enjoy :)
9. If you need close click ```Ctrl + C```

# Examples
```get``` /api/users/ - get all users
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": []
}
```

```post``` /api/recipes/ - add recipe
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "img.png",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

```get``` /api/recipes/{recipes_id}/ - get advanced info about recipe
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

```patch``` /api/recipes/{recipes_id}/ - partial updating of information about the recipe
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

```delete``` /api/recipes/{recipes_id}/ - delete recipe
# Some words from author
It was 