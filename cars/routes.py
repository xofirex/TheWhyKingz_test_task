from .views import (
    add_car,
    add_car_page,
    get_cars,
    get_car_details,
    delete_car,
    delete_car_page,
    update_car
)


def setup_routes(app):
    app.router.add_get('/', get_cars, name='get_cars')
    app.router.add_get('/cars/create-car', add_car_page, name='add_car_page')
    app.router.add_post('/cars/create-car', add_car, name='add_car')
    app.router.add_get('/cars/{vin_code}', get_car_details, name='get_car_details')
    app.router.add_get('/cars/{vin_code}/delete', delete_car_page, name='get_delete_car_page')
    app.router.add_post('/cars/{vin_code}/delete', delete_car, name='delete_car')
    app.router.add_post('/cars/{vin_code}/update', update_car, name='update_car')
