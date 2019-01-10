import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import AccessToken
from dashboardapp.models import Restaurant, Meal, Order, OrderDetail, Customer
from dashboardapp.serializers import RestaurantSerializer, \
    MealSerializer, \
    OrderSerializer
import stripe
from dashboard.settings import STRIPE_API_KEY
import openpay

openpay.api_key = "sk_39e1b9ee04ba4a40bac4e79380d9e858"
stripe.api_key = STRIPE_API_KEY
openpay.verify_ssl_certs = False
openpay.merchant_id = "m0fyleu0u3azyiz3b16d"


def customer_get_restaurant(request):
     restaurants = RestaurantSerializer(
         Restaurant.objects.all().order_by("-id"),
         many = True,
         context = {"request": request}
     ).data

     return JsonResponse({"restaurants": restaurants})

def customer_get_meals(request, restaurant_id):
    meals = MealSerializer(
        Meal.objects.filter(restaurant_id = restaurant_id).order_by("-id"),
        many = True,
        context = {"request": request}
    ).data
    return JsonResponse({"meals": meals})

@csrf_exempt
def customer_add_order(request):
    """
        params:
        access_token
        restaurant_id
        address
        order_details (json format), example:
            [{"meal_id": 1, "quantity": 2}, {"meal_id": 2, "quantity": 3}]
        conekta_token

        return:
            {"status": "success"}
    """

    if request.method == "POST":
        #Get Token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    #Get Profile
    customer = access_token.user.customer

    #Get stripe token
    #openpay_token = request.POST["openpay_token"]
    stripe_token = request.POST["stripe_token"]

    #Check wheter customer has any order that is not delivered
    if Order.objects.filter(customer = customer).exclude(status = Order.Entregado):
        return JsonResponse({"status": "fail", "error": "Your last order must be completed"})

    #Check Adress
    if not request.POST["address"]:
        return JsonResponse({"status": "failed", "error": "Address is required"})

    #Get Order details
    order_details = json.loads(request.POST["order_details"])

    order_comission = 0
    order_total = 0
    order_subtotal = 0
    order_subtotal1 = 0

    for meal in order_details:
        order_subtotal1 += Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"]* 1.20
        order_subtotal += Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"]
        order_comission += int(round(order_subtotal * 20) / 100)
        order_total += Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"] + order_comission

    if len(order_details) > 0:
        #Step 1 - Create a charge: this will charge customer cars
        charge = stripe.Charge.create(
        amount = int(Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"]) * 100 + int(round(Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"] * 20 ) / 100) , #Amount in cents
        currency = "mxn",
        source = stripe_token,
        description = "FoodClub Orden",
        )

    if charge.status != "failed":
            # Step 2 - Create an order
            order = Order.objects.create(
                customer=customer,
                restaurant_id=request.POST["restaurant_id"],
                total=int(Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"]),
                status=Order.Preparando,
                address=request.POST["address"]
            )

            # Step 3 - Create order details
            for meal in order_details:
                OrderDetail.objects.create(
                    order=order,
                    meal_id=meal["meal_id"],
                    quantity=meal["quantity"],
                    extras = meal["extras"],
                    sub_total=Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]
                )

            return JsonResponse({"status": "success"})

    else:
            return JsonResponse({"status": "failed", "error": "Failed connect to Stripe"})




def customer_get_latest_order(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
       expires__gt = timezone.now())

    customer = access_token.user.customer
    order = OrderSerializer(Order.objects.filter(customer = customer).last()).data

    return JsonResponse({"order": order})

def restaurant_order_notification(request, last_request_time):
    notification = Order.objects.filter(restaurant = request.user.restaurant,
    created_at__gt = last_request_time).count()

    return JsonResponse({"notification": notification})