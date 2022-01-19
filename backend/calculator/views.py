from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import json

def convertdate(date):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')

# This is a proof of concept like thing, so for now I will ignore csrf verification
# for simplicities sake. Also this view does not access to the database any any shape or form.
@csrf_exempt
def index(request, *args, **kwargs):
    # Get json from request
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    # Extract data
    cart_value = float(body['cart_value'])
    delivery_distance = float(body['delivery_distance'])
    number_of_items = float(body['number_of_items'])
    time = convertdate(body['time'])

    # Check for any possible errors that might not work with our calculations
    # TODO more clear error handling, this is very basic
    if not cart_value or not delivery_distance or not number_of_items or not time:
        return JsonResponse({'delivery_fee': 'Wrong set of parameters'})
    if cart_value <= 0:
        return JsonResponse({'delivery_fee': 'cart_value cannot be less then or equal o 0'})
    if delivery_distance <= 0:
        return JsonResponse({'delivery_fee': 'delivery_distance cannot be less then or equal 0'})
    if number_of_items <= 0:
        return JsonResponse({'delivery_fee': "number_of_items cannot be less then or equal to 0"})

    # TODO extract the following part into its seperate function on a seperate file for more readability

    # If the cart_value is more then 100, no delivery cost
    if cart_value >= 100:
        return JsonResponse({'delivery_fee': 0})

    # Calculate surcharge
    surcharge = 0
    if cart_value < 10:
        surcharge = 10 - cart_value
    
    # Calcualte distance cost
    distance_cost = 2
    delivery_distance -= 1000
    while delivery_distance > 0:
        distance_cost += 1
        delivery_distance -= 500
    
    # Calcualte item count cost
    item_cost = 0.5 * max(0, number_of_items - 4)

    fee = min(15, surcharge + distance_cost + item_cost)

    # Check for rush hour
    start = datetime(time.year, time.month, time.day, 15, 0, 0, 0)
    end = datetime(time.year, time.month, time.day, 17, 0, 0, 0)
    if time.weekday() == 4 and start <= time and time <= end:
        fee = min(15, fee * 1.1)
    
    return JsonResponse({'delivery_fee': fee})