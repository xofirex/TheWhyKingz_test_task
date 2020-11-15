Install deps - run::

    $ pip install -r requirements.txt

Download and install mongo db::

   https://docs.mongodb.com/manual/installation

Create db with name::

    cars(car is collection)

Run web server::

    $ python -m cars

Endpoints::

    GET '/' = main page
    GET '/cars/{vin_code}' = get car details
    POST '/cars/{vin_code}/update' = update car details
    POST '/cars/{vin_code}/delete' = delete car
    POST '/cars/create-car' = create car
