# LIT REVIEW

This is my fourth Python project for Openclassrooms courses.

In this scenario, I have joined a young startup named LITReview who has just completed his first fundraising.

Our goal is to launch a product which can be use by our community. They can use it to consult or request book reviews on demand.

This application will be a web application,and it will be develop on django web framework.

On the app, you can create your personnal account and use the following system to follow all the users that you want. 

You can request a book review or you can post review on users tickets if they are on your following list.

You can post your ticket with a specific image (a generic image will be posted if you do not have one)

You can not create a review on a ticket if this ticket already received a review.

Also, the system allows you to create a review even if there are no ticket on your book.

## Instalation

This script needs Python installed and some packages detailled in requirements.txt.

Clone the repo with your terminal 
1. Clone the repo with your terminal

```
  git clone https://github.com/bendms/litreview.git
```

## Configuration 

1. Go to litreview directory

```
  cd litreview
```

2. Start virtual environment from the terminal : 
```
    source/env/bin/activate
```

3. Install packages from requirements.txt

```
  pip install -r requirements.txt
```

4. Go to src directory 

```
  cd src
```

5. Launch local server on your machine

```
  python manage.py runserver
```

6. Go to https://127.0.0.1:8000 to access to the website

7. Create your personnal account to access

## How to contribute 

This project is a MVP and specifications requests simple and minimal UI. Feel free to image a design and add style for it. It will be great to have some animation with JavaScript.
