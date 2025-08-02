# CogniQ
G7_CPE106L-4_E03 CogniQ
by De Jesus, Rei Bryan Jericho; Duque, Joseph Emmanuel; Jasmin, Jazmin Taye

CogniQ is a Python-built application that enhances mental wellness through its features 
of mood tracking, journaling, and local support resources to support the community for 
their well-being. It provides a personal approach to the user to track their mood patterns 
and advises insights from external resources to support their mental well-being for their 
stability.

# Features
1. User / Admin Sign-in and Log-in – allows users and administrators to create 
their accounts based on their roles and email domain (@admin.ph or 
@gmail.com).
2. User Input on Mood Levels and Journal - Users can put their mood and 
journal based on their experience today.
3. Admin Accessibility to User Inputs - Admins can observe the user's mood and 
journal inputs for data gathering
4. Graph Visualization (Admins only) - Admins can view the user's data through 
Matplotlib to track their well-being on a particular day.
5. Provides Resources and Insights - The program provide resources and insights 
based on the user's journal and mood inputs  to aid them in their journey.

# Prerequisites
CogniQ requires/used packages such as flet, sqlite3, matplotlib, datetime, random, os
It is highly recommended to download python (latest version 3.13.5; link: https://www.python.org/downloads/), or visual studio code(link: https://code.visualstudio.com/) to see the full codes of the project, if you are going to access or run CogniQ

***Other downloads***
Git (link: https://git-scm.com/downloads) - to clone the repository and store the files, without the necessity to download the files one by one

# MVC Layout
***Model***
database.py – administers the interactions with cogniq_database.db for storing and retrieving
information such as user, mood, admin, etc.
recommendation.py – provide mental health recommendations according to the mood tracker
graph.py – visual representations and stores as images

***Views***
auth.py - Authentication FletUI, which shows first in the program for login and signup
user_panel.py – UI for users in applying the features of mood, journal, and view inputs.
admin_panel.py – UI for admin in applying features such as view journals, mood, and graphs of the
user

***Controller***
main.py – central controller of the program which determines the user status (admin or login) based on the email domains (only run this file if you have downloaded and inserted all the needed files and assests and insert them inside a folder)

# Tutorials to Access
For tutorials kindly check the COGNIQ_TUTORIALS.pdf if you want to access and try CogniQ

Once again thank you for accessing CogniQ as your mental health tracker
