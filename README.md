# KaiVegan
#### Video Demo: ~~<URL HERE>~~
#### Description: 
KaiVegan is a customer to customer e-commerce. What is KaiVegan's purpose? to buy and sell a products. Who is KaiVegan's target audience? Vegan community.

> [!NOTE]
> Considered as prototype or experimental. <br>
> Real-Time communication is not efficient unlike WebSockets or Server-Sent events.

## Features
- Database Interaction:
  - Object-relational mapping
- Data Interchange:
  - Front-to-End ***x-www-form-urlencoded***, ***multipart/form-data***; Vice versa ***json***
- Security:
  - hash user's plaintext, method=sha?
- Real-Time communication
  - Web Worker API

## Installation
> [!IMPORTANT]
> This project is developed on a Linux environment, Ubuntu distro.

First ensure that you're up to date.
```
sudo apt update && sudo apt upgrade
```
after that, install python3 and python3's package manager.
```
sudo apt install python3 && sudo apt install python3-pip
```
***(Optional)*** project's database.
```
sudo apt install sqlite3
```
### Project's environment
```
pip3 install flask flask_session flask-sqlalchemy
```
and then 
```
git clone 
```

## Execution
```
python3 app.py -h  
```

## Technologies Used
- Front-end:
  - html
  - css & bootstrap
  - javascript
- Back-end:
  - Python flask
  - sqlite3 database ***(Optional you can choose your own)***

## Topics that i research
- database Object-relational mapping with python sqlalchemy.
- more about python flask, html, css, javascript documentation.
