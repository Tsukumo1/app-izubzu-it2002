from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def index(request):
    """Shows the main page"""

    ## Show recommendation list
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM house_info WHERE  house_status='FOR RENT' LIMIT(1)")
        total = cursor.fetchone()

        cursor.execute("SELECT * FROM house_info ORDER BY expected_price LIMIT(5)")
        houses = cursor.fetchall()

        # Try advanced queries
        cursor.execute("SELECT COUNT(*) AS sell_count, user_name, email FROM house_info h LEFT JOIN user_info u ON u.email = h.owner_email WHERE house_status='FOR RENT' GROUP BY u.email ORDER BY sell_count LIMIT (1)")
        best_seller = cursor.fetchone()



    result_dict = {'records': houses,
                   'total': total,
                   'best_seller': best_seller}

    return render(request,'app/index.html',result_dict)



def rent(request):

    ## Rent the house
    if request.POST:
        if request.POST['action'] == 'rent':
            with connection.cursor() as cursor:
                cursor.execute("UPDATE house_info SET house_status = 'RENTED' WHERE house_title = %s",[request.POST['id']])
                # Update the record in rent_history
            
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM house_info ORDER BY expected_price")
        houses = cursor.fetchall()
    result_dict = {'records': houses}

    return render(request,'app/rent.html',result_dict)




def register(request):
    context={}
    status=''

    ## Add the user
    if request.POST:
        with connection.cursor() as cursor:
            user_name = request.POST['user_name']
            real_name = request.POST['real_name']
            password = request.POST['password']
            phone_no = request.POST['phone_number']
            email = request.POST['email']

            cursor.execute("INSERT INTO user_info VALUES (%s,%s,%s,%s,%s)",
            [user_name,real_name,password,phone_no,email])

            user = User.objects.create_user(user_name, email, password)
            user.save()

            status='You have registed successfully!'

    context["status"] = status

    return render(request, "app/register.html", context)


def view(request, title):

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM house_info WHERE house_title = %s", [title])
        house = cursor.fetchone()

        result_dict = {'house': house}
        
    ## Rent the house
    if request.POST:
        if request.POST['action'] == 'rent':
            with connection.cursor() as cursor:
                cursor.execute("UPDATE house_info SET house_status = 'RENTED' WHERE house_title = %s",[request.POST['title']])
                # Update the record in rent_history

    return render(request,'app/view.html',result_dict)

def login(request):
    context={}
    status = ''

    if request.POST:
        user_name = request.POST['user_name']
        pw = request.POST['password']
        user = authenticate(request, username=user_name, password=pw)

        if user is not None:
            status='You have log in successfully!'
            context["status"] = status
        
        else:
            status='Emmm... Seems username/password is wrong! Please check again!'
            context["status"] = status
    
    return render(request, "app/login.html", context)


def post(request):
    context={}
    status=''

    ## Add the house
    if request.POST:
        with connection.cursor() as cursor:
            house_title = request.POST['house_title']
            area_info = request.POST['area_info']
            room_size = request.POST['room_size']
            house_location = request.POST['house_location']
            postal_code = request.POST['postal_code']
            number_of_bedrooms = request.POST['number_of_bedrooms']
            number_of_washrooms = request.POST['number_of_washrooms']
            max_tenant = request.POST['max_tenant']
            available_date = request.POST['available_date']
            expected_price = request.POST['expected_price']
            price_per_feet = request.POST['price_per_feet']
            negotiable = request.POST['negotiable']
            owner_email = request.POST['owner_email']
            owner_phone_number = request.POST['owner_phone_number']
            house_status = 'YES'

            cursor.execute("INSERT INTO house_info VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [house_title, area_info, room_size, house_location, postal_code, number_of_bedrooms, 
            number_of_washrooms, max_tenant, available_date, expected_price, 
            price_per_feet, negotiable, owner_email, owner_phone_number, house_status])

            status='Congratulation! You have post a house successfully!'

    context["status"] = status
    
    return render(request, "app/post.html", context)
