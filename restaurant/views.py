# File: views.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/11/2025
# Description: This is the confirmation page after the user submits the order form.
from django.shortcuts import render
import random

# List of special dishes with their names and prices
specials = [ {"name": "Errol's Thai Fried Rice w/ Jerk Pork", "price": 14.95}, {"name": "Jerk Chicken Flatbread", "price": 17.00}, 
            {"name": "Ackee and Saltfish Flatbread", "price": 19.00}, {"name": "Honey Garlic Tenders Flatbread", "price": 22.50}, 
            {"name": "Curry Shrimp Flatbread", "price": 22.00}, {"name": "Oxtail Flatbread", "price": 22.50}, {"name": "Cajun Chicken Burger & Fries", "price": 18.00}, 
            {"name": "Cajun Salmon Burger & Fries", "price": 20.00}, {"name": "Jerk Chicken Breast Salad", "price": 14.00}, {"name": "Caribbean Salad", "price": 13.00}, 
            {"name": "Rasta Pasta w/ Seafood Pasta", "price": 33.00}, {"name": "Palo's Jerk Pork (By itself - one pound)", "price": 12.00}, {"name": "Steak Rib Eye", "price": 28.50}, 
            {"name": "Steak & Shrimp", "price": 31.95}, {"name": "Codfish Cakes (4)", "price": 5.50}, {"name": "Andrew's Jerk Pork Wrap", "price": 11.95}, 
            {"name": "Kingfish", "price": 20.75}, {"name": "Roy's Honey Garlic Wings", "price": 10.00}, {"name": "Reggae Pasta", "price": 14.00}, 
            {"name": "Rasta Pasta w/ Sliced Snapper (steak)", "price": 24.00}]

# Create your views here.
def main_page(request):
    """ Render the main page of the application. """
    return render(request, "restaurant/main.html")

def order_page(request):
    """ Render the order page where users can place an order. """

    # Randomly choose a special dish from the list of specials
    selected_special = random.choice(specials)
    # Build context with the selected special's name and price
    context = {"special": selected_special["name"], "special_price": selected_special["price"]}
    return render(request, "restaurant/order.html", context)

def confirmation_page(request):
    """ Render the confirmation page without additional context. """
    return render(request, "restaurant/confirmation.html")

def submit(request):
    """
    Process the order form submission and render the confirmation page.
    
    Extracts customer information and order details from the POST data.
    Checks for selected menu items and calculates the total price.
    Constructs a context dictionary with order details to be displayed
    in the confirmation page.
    """

    # Check if the request method is POST 
    if request.method == "POST":
        # Extract customer info:
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        special_instructions = request.POST.get('special_instructions', '')
        
        # Define menu items with their prices.
        menu_items = {
            "jerk_chicken": {"name": "Jerk Chicken", "price": 14.75},
            "oxtail_fried_rice": {"name": "Oxtail Fried Rice", "price": 26.00},
            "curry_goat_roti": {"name": "Curry Goat Roti", "price": 14.00},
            "shrimp_rasta_pasta": {"name": "Shrimp Rasta Pasta", "price": 22.00},
            "oxtail_extra_plantains": {"name": "Extra Plantains", "price": 2.00},
            "oxtail_extra_gravy": {"name": "Extra Gravy", "price": 1.50},
            # For the special dish, we try to get its name and price from the form; if not, use default text and the price is $0.
            "today_special": {"name": request.POST.get('today_special', "Today's Special"), "price": float(request.POST.get('today_special_price', 0))},
        }
        
        ordered_items = [] # List to hold ordered menu items
        total_price = 0.0  # Total order price in dollars
        
        # Check which items were selected.
        for key, item in menu_items.items():
            # Check if the key exists in the POST data 
            if key in request.POST:
                ordered_items.append(item)      # Append the item to the ordered_items list
                total_price += item["price"]    # Add the price of the item to the total_price
        
        # Build context dictionary to pass order details to the confirmation template
        context = {
            "name": name,
            "phone": phone,
            "email": email,
            "special_instructions": special_instructions,
            "ordered_items": ordered_items,
            "total_price": total_price,
        }

    # Render the confirmation template with the context data
    return render(request, "restaurant/confirmation.html", context)
