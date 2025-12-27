# Authentication Project

## Overview
This project implements a three-level authentication process using MySQL for storing user data. The application has a basic UI built with Tkinter.

## MySQL DB setup in Docker
1. docker-compose -f mysql-docker-compose.yaml up -d

## Set Up a Virtual Environment
1. python -m venv env
2. env\Scripts\activate

## Setup
1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Set up the database:
    ```sh
    python database/setup.py
    ```

3. Add user data:
    ```sh
    python src/user_management.py
    ```

## Usage
Run the authentication process:
```sh
python main.py

