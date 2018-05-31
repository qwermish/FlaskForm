# A Simple Flask WebForm Application
This application allows a user to register with a username, password, and age. After a user successfully registers or logs in, it shows the user a histogram of all ages of registered users. The bar corresponding to the current user's age is highlighted in red. It uses Flask to create the forms, matplotlib to produce the histogram, a PostGreSQL database to store user data, and Heroku for hosting.

The URL for the app is [https://rocky-cliffs-30443.herokuapp.com/](https://rocky-cliffs-30443.herokuapp.com/).

## Contents

The Flask code is contained in app.py and forms.py. Procfile, requirements.txt, and runtime.txt are configuration files for the purposes of making the code run on Heroku.

The templates folder contains the HTML templates for the main page (index2.html) and the page that displays the histogram (images.html).

## Main Resources Used
- [http://blog.sahildiwan.com/posts/flask-and-postgresql-app-deployed-on-heroku/](http://blog.sahildiwan.com/posts/flask-and-postgresql-app-deployed-on-heroku/)
- [https://stackoverflow.com/questions/18290142/multiple-forms-in-a-single-page-using-flask-and-wtforms](https://stackoverflow.com/questions/18290142/multiple-forms-in-a-single-page-using-flask-and-wtforms)
- [https://stackoverflow.com/questions/20107414/passing-a-matplotlib-figure-to-html-flask](https://stackoverflow.com/questions/20107414/passing-a-matplotlib-figure-to-html-flask)
- [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms)