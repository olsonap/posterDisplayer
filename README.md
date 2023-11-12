# posterDisplayer
A PyGame window which displays a movie poster.

In conjunction with the attempt2hometheater repo, this app is used to display images through a Raspberry Pi and TV screen.
The RPi will host a uWSGI server delivering a Django web app.
The web app allows the user to sign in, search for movies, and preview the movie poster.
Upon selection of a movie, the web app also displays info about the movie, including a movie trailer.
Meanwhile, the PyGame app is continually checking to see if the currently selected movie poster has changed.
Upon a change, the PyGame app will reload the image being displayed.
