# Django-Instodramat

This is my second Django project. It took me a while to finish it, because of work and studies. This app should look and work very similar to the Instagram app. This website allows people to create their user account and profile in order to share pictures. If you have an account you can upload any photo and share it with others. Each photo required must be a squre. Instodramat app allows users to crop photos with Pillow package and JavaScript. Also as user you can follow others and see their uploaded files on you main webpage or if you like someone's photo you are able to click "like" button.


## Stack

* Python
* Django
* SQLite3
* HTML
* CSS
* Bootstrap
* JavaScript

## Requirements

*I used this versions to create project*

* Python: 3.9
* Django: 3.2.8

## Running app

It is recommended to create python virtual environment for this project. It could be done by executing command:

`python -m venv <relative path to directory with new venv>`

File *requirements.txt* contain all necessary dependencies (including Django framework). To install them and update pip  execute command:

`pip install -r <relative path to requirements.txt>`

If you successful installed Django, you need to apply database schemas for models. 
Default database type for Django is sqlite3 which is used. It can be changed in *settings.py* file if you need.
To create schemas navigate to Instodramat directory where *manage.py* is located. Then execute command:

`python manage.py makemigrations`

After creating schemas you need to apply them. To do this you have to execute command:

`python manage.py migrate`

Now you can run server with command:

`python manage.py runserver 0.0.0.0:8080`

App is running in DEBUG mode True, because it is easier way to handle static and media file. This means that you don't need any static file server like apache or nginx to check this app out.

## Main webpage ('/') [unauthorized]

Main webpage for not logged in users is very simple. It tells us to log in or to create new account.

<img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/main_unauth.PNG" width="240" height="130">

## Register ('/profile/register/')

Register webpage contains form with 2 section that allows users create new account. First section is responsible for creating User model, so you need pass there username, email and password. Second section contains fields for first and last name, profile description, avatar, etc. You can also choose if your name should be visible or if you want use only username.

<img src="https://github.com/aFku/Django-Instodramat/blob/main/readm_src/register.PNG" width="240" height="130">

## Login ('/profile/login/')

Via Login webpage you can log in :D There is a form for your creds. You also can find there references to password reset and register page.

<img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/login.PNG" width="240" height="130">

## Password reset ('/profile/password_reset/')

<img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/reset_password.PNG" width="240" height="130">

## Main webpage ('/') [authorized] [empty]

If you log in for the first time or you don't follow any user you should see message on your main webpage. It will be there untill you follow someone who uploads photo.

<img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/main_empty.PNG" width="240" height="130">

## Main webpage ('/') [authorized] [with content]

If you follow some users and they have photos you should see them on main webpage. On the top of the list you can see the most recent photo. At the bottom of the website you can find buttons to navigate beetwen paginator pages.

<img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/main.PNG" width="240" height="130"> <img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/main_pagination.PNG" width="240" height="130">

## Add Photo ('/photos/add/')

Webpage contains form with only 2 fields that allow users upload file and add description.

<img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/add_photo.PNG" width="240" height="130">

## Profile ('/profile/<int:pk>/')

Profile webpage shows almost all information about user. You can see there username and display name, list and number of followers and all photos that users uploaded. If you are on someone's profile you can see there also button to follow/unfollow this user.

<img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/profile1.PNG" width="240" height="130"><img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/profile2.PNG" width="240" height="130"><img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/profile3.PNG" width="240" height="130"><img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/profile4.PNG" width="240" height="130"><img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/profile5.PNG" width="240" height="130">

## Profile settings ('/profile/settings/')

In your profile settings you are able to change password, email or other profile data. Also you can delete there your account.

<img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/settings.PNG" width="240" height="130">

## Community ('/community/')

If you want to find new users to follow, or interesting photos you should go to community section. You can find there the newest photos from all users. There is also search bar where you can find any user.

<img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/community.PNG" width="240" height="130"> <img src="https://raw.githubusercontent.com/aFku/Django-Instodramat/master/readme_src/search.gif" width="240" height="130" />
