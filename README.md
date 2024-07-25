# Travel Tales

## Description

The Travel Tales is a web application that allows users to explore various travel destinations, upload their travel experiences, and interact with content shared by other users. Users can browse destinations added by different contributors. This app provides an interactive platform for users to select their desired destination, view details about the place, and contact administrators for reservation inquiries.

## Technologies Used

The Travel App is built using the following technologies:

- Front-end: HTML, CSS, JS, Jinja template
- Back-end: Python Flask
- Database: SQLite Database with SQLALCHEMY

## Installation and Usage

To use the Travel App locally, follow these steps:

1. Clone the GitHub repository for the app onto your local machine.
2. Optionally, create a python virtual environment.
3. Install all the modules using `yarn pip:install`.
4. Initialize the database by running `yarn db:init`.
5. Then migrate the initial database schema with `yarn db:migrate`.
6. Finally apply the migrations using `yarn db:upgrade`.
7. Start the web app by running `yarn dev` to run in debug mode.
8. Access the app through your web browser at the specified local address `(localhost:5000)`.

After upgrading the database schema, you can add a default admin user by running `yarn db:add`.

Additionally you can run:

- `yarn format` to format all the `.py` files.
- `yarn host` to host the application globally on your local machine in ubuntu or WSL for 60 minutes.

## Contributions

Contributions to the Travel App for GitHub are welcome! If you would like to contribute, please fork the repository, make your changes, and submit a pull request with a detailed description of the enhancements or bug fixes made.

We hope you enjoy exploring new travel destinations conveniently through our Travel App! Happy travels!
