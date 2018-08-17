# Dublin Busy

Web application for Dublin Bus journey time predictions as developed by T3DB

Available from www.dublinbusy.com


## Prerequisites

The application is built to be used with Python 3. Update `Makefile` to switch to Python 2 if needed.

Some Flask dependencies are compiled during installation, so `gcc` and Python header files need to be present.
For example, on Ubuntu:

    apt install build-essential python3-dev
    pip install virtualenv


## Quick Start

        git clone https://github.com/ernest4/t3db_busy_repo.git
        
Go to t3db_busy_repo. To run the application from the terminal:

    heroku local -p 8765

And open it in the browser at [http://127.0.0.1:8765/](http://127.0.0.1:8765/).


## Built With

* [heroku](https://heroku.com) - Heroku (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.
* [Django](http://flask.pocoo.org/) - The web framework used
* [jQuery](https://jquery.com/) - JavaScript library
* [Bootstrap](https://getbootstrap.com/) - Front-end library
* [Google Maps](https://developers.google.com/maps/) - Real-time information for mapping and navigation
* [Jupyter Notebook](http://jupyter.org/) - Web application used for data analysis
* [Hotjar](http://hotjar.com/) - Web application used for heat mapping user experience


## Data Used

* [RTPI data](https://smartdublin.ie/smartstories/real-time-passenger-information/ ) - Historic planned and actual bus arrival times.
* [OpenWeatherMap](https://openweathermap.org/history-bulk) - History Bulk Weather Data.
* [OpenWeatherMap](https://openweathermap.org/current) - Current Weather Data.

## Authors

* **Julia Boes** - [GitHub](https://github.com/FrauBoes)
* **Daragh O'Farrell** - [GitHub](https://github.com/Basschops)
* **ernestas monkevičius** - [GitHub](https://github.com/ernest4)
* **Jonathan Leon** - [GitHub](https://github.com/jonnyleon1)

