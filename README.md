# BlogLite 

[**Live Demo**](https://bloglite-dx6d.onrender.com)


Capstone Project for AppDev I, done under guidance of [@AbhishekPOD](https://github.com/AbhishekPOD) and [@nitinC](https://chandrachoodan.gitlab.io/)

This is a markdown based blogging site. It provides live preview while writing the post. Most interactions in the app are asynchronous. App supports Google based Oauth 2.0 login and API key to authenticate APIs.

## Technologies used

**Flask** <br>
**Bootstrap**: Designing and styling <br>
**Flask MDE**: Interactive editor for Markdown <br>
**Flask Restful**: API <br>
**OpenAPI** 3.0 <br>
**Flask-Markdown** <br>
**Google**: Authentication <br>
**SQLite3**: Database <br>

## API Design
REST based API for Entries, Comments and User. Some extra features have been added as PATCH on some endpoints.
Architecture and Features
The app has a set of controller files which has all the modifier functions. These 
functions have been used by API and routes as per requirements.

## Database

![Schema](https://github.com/monees007/BlogLite/blob/9a977f09fd0a49c9a999298baf463240282d3032/schema.png)

## Features

### Authentication
The app supports Oauth 2.0 Google login, hence needing a google account for the same. Once logged in, users can download the credentials for API, from the ‘Manage’ option on the profile page. The API supports both cookies based authentication as well as api_key  in header. This is done in order to facilitate async functions on the app.

### Entries
Users can create an entry by clicking on the add button at the navigation bar. Text can be entered plain or markdown. Live Preview can be seen aside the textbox. Local as well as external images are supported. No word limit has been set.

### Comments
Markdown support for comments is not provided. They are asynchronous.

### File Upload
File upload is done through API ( async for app ) which returns filename/address that is immediately used by MD editor to add syntax for image. Preview of recently uploaded images is not shown immediately. This is a known issue.

### Export
App supports user data exports and exports posts, profile, comments on post in json format.

### Comments
Markdown support for comments is not provided. They are asynchronous.

<!-- 
## Video
<iframe src="https://drive.google.com/file/d/1WJVVwbNahIhuHh-KhOkC87tNJrJ2CvWg/preview" width="640" height="480" allow="autoplay"></iframe>
https://drive.google.com/file/d/1WJVVwbNahIhuHh-KhOkC87tNJrJ2CvWg/view?usp=sharing
https://drive.google.com/file/d/1Zj9_4Y02Vp6fepXk_wzNWczU4v3pVMCW/view?usp=sharing -->
