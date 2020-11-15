import aiohttp_jinja2
from aiohttp import web

from .db import car, get_car_by_vin_code, delete_car_by_vin_code
from .utils import check_input_form


@aiohttp_jinja2.template('add_car.html')
async def add_car(request):
    form = await request.post()

    errors = check_input_form(car, form)
    if errors:
        return {'errors': errors, 'form': form}

    vin_code = form['vin_code']
    car_exists = await get_car_by_vin_code(request.app['mongo'].car, vin_code)
    if car_exists:
        return {'errors': {'vin_code': 'Car with this code already exists.'}, 'form': form}

    await request.app['mongo'].car.insert_one(
        {
            'vin_code': vin_code,
            'manufacturer': form['manufacturer'],
            'model': form['model'],
            'year_created': form['year_created'],
            'colour': form['colour']
        }
    )
    return web.HTTPFound(location='/')


@aiohttp_jinja2.template('add_car.html')
async def add_car_page(request):
    return {"errors": {}, "form": None}


@aiohttp_jinja2.template('cars.html')
async def get_cars(request):
    cars = await request.app['mongo'].car.find(request.rel_url.query).to_list(length=100)
    return {"cars": cars}


@aiohttp_jinja2.template('car_details.html')
async def get_car_details(request):
    car_detail = await get_car_by_vin_code(request.app['mongo'].car, request.match_info['vin_code'])
    if not car_detail:
        return web.HTTPNotFound()
    return {"car": car_detail}


@aiohttp_jinja2.template('car_delete.html')
async def delete_car_page(request):
    car_detail = await get_car_by_vin_code(request.app['mongo'].car, request.match_info['vin_code'])
    if not car_detail:
        return web.HTTPNotFound()
    return {}


@aiohttp_jinja2.template('car_delete.html')
async def delete_car(request):
    await delete_car_by_vin_code(request.app['mongo'].car, request.match_info['vin_code'])
    return web.HTTPFound(location='/')


@aiohttp_jinja2.template('car_details.html')
async def update_car(request):
    form = await request.post()

    car_detail = await get_car_by_vin_code(request.app['mongo'].car, request.match_info['vin_code'])
    if not car_detail:
        return web.HTTPNotFound()

    errors = check_input_form(car, form)
    if errors:
        return {'errors': errors, 'car': form}

    vin_code = form['vin_code']
    car_exists = car_detail['vin_code'] != vin_code and await get_car_by_vin_code(request.app['mongo'].car, vin_code)
    if car_exists:
        return {'errors': {'vin_code': 'Car with this code already exists.'}, 'car': form}

    await request.app['mongo'].car.replace_one({'_id': car_detail['_id']}, form)

    return web.HTTPFound(location='/')
