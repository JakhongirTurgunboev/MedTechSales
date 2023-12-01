# MedTech

[![Build Status](https://travis-ci.org/JakhongirTurgunboev/MedTechSales.svg?branch=master)](https://github.com/JakhongirTurgunboev/MedTechSales)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)

## Description

This is a Django Rest Framework project that .

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started with the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/JakhongirTurgunboev/MedTechSales.git
   cd project_name
   
2. Run the following command to build docker images:
   ```bash
   docker-compose build
   
3. Run the migrations:
   ```bash
   docker-compose run migrate

4. Run the application:
   ```bash
   docker-compose up

   
## Usage

1. After running the application, open http://localhost:8000/
2. You can visit http://localhost:8000/swagger/ for API documentation.
3. Add products, clients, employees, and orders with API.
4. When adding order, list of product ids should be inserted in products list in payload. Example:
      ```bash
      {
        "client": 1,
        "employee": 1,
        "products": [
          1, 2, 1
        ],
        "date": "2023-12-01"
      }
      ``` 
      Note that, you can use ids several times inside the list, quantity and price will be 
   automatically calculated. Product ids used in list must be available in Product table.
5. You can get the statistics in the following:
   - http://localhost:8000/employee/statistics/ - for all employees' statistics, parameters 
     like month and year can be added optionally.
   - http://localhost:8000/statistics/client/{id}/ - for client's statistics, parameters 
     like month and year can be added optionally, id parameter is required.
   - http://localhost:8000/statistics/employee/{id}}/ - for single employee's statistics, parameters 
     like month and year can be added optionally, id parameter is required.
6. Note that since the project is designed for the usage on local machine, database configurations
   are not securely defined and debug mode is on. Different type of queries like annotation and gathering
   data, then manipulating with python is used for demonstration purposes.


## API Documentation
For detailed API documentation, visit http://localhost:8000/swagger/ after running the application.

## Configuration
To customize the project, refer to the Configuration section in the README.

## Contributing
If you'd like to contribute to the project, follow these guidelines:

1. Fork the repository.
2. Create a new branch: git checkout -b feature/your-feature.
3. Commit your changes: git commit -m 'Add some feature'.
4. Push to the branch: git push origin feature/your-feature.
5. Submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
