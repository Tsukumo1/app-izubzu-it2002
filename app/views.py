from django.shortcuts import render, redirect
from django.db import connection



def index(request):
    """Shows the main page"""

    ## Show recommendation list
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM house_info ORDER BY expected_price LIMIT(5)")
        houses = cursor.fetchall()

    result_dict = {'records': houses}

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
            cursor.execute("INSERT INTO user_info VALUES (%s,%s,%s,%s,%s)",
            [request.POST['user_name'],request.POST['real_name'],request.POST['password'],
            request.POST['phone_number'],request.POST['email']])

            status='You have registed successfully!'
            cursor.execute("SELECT * FROM user_info WHERE email = %s", [request.POST['email']])
            obj = cursor.fetchone()

    context["status"] = status

    return render(request, "app/register.html", context)


def view(request, title):

    ## Rent the house
    if request.POST:
        if request.POST['action'] == 'rent':
            with connection.cursor() as cursor:
                cursor.execute("UPDATE house_info SET house_status = 'RENTED' WHERE house_title = %s",[request.POST['title']])
                # Update the record in rent_history

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM house_info WHERE house_title = %s", [title])
        house = cursor.fetchone()

        result_dict = {'house': house}
    
    return render(request,'app/view.html',result_dict)
