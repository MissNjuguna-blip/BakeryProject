from django.db import IntegrityError,transaction
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from Center.models import Admin, Customer,Deliverer,User
from rest_framework_simplejwt.exceptions import TokenError

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def SignUp(request):
    # print ("register function")
    username=request.data.get("username")
    email=request.data.get("email")
    password=request.data.get("password")
    role=request.data.get("role")
    
    
    # print(username,email,password,role,phone)

    if not username or not email or not password:
        return Response({"error":"Email,Username and password are required"}, status=400)
    
    # check if user exsists
    if User.objects.filter(username=username).exists():
        return Response({"error":"Username already exist"}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({"error":"Email already exist"}, status=400)
    
    try:
        # user account creation
        user=User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            
        )
        if role == 'admin':
            Admin.objects.create(
                user=user,
                address=request.data.get("address")

            )
        elif role == 'customer':
            Customer.objects.create(
                user=user,
                address=request.data.get("address")
                
            )
        # elif role == 'deliverer':
        #     Deliverer.objects.create(
        #         user=user,
        #         first_name=request.data.get("first_name"),
        #         last_name=request.data.get("last_name"),
        #         assigned_order=request.data.get("assigned_order")
    
        #     )

        return Response({
            "user_id":user.id,
            "username":user.username,
            "role":user.role,
            "message":f"{role.capitalize()} Registered successfully"
        })
    except IntegrityError as e:
        return Response({"error":"Integrity Error" + str(e)})
    except Exception as e:
        return Response({"error":str(e)})


# Login
@api_view(["POST"])
@permission_classes([AllowAny])
def Login(Request):
    username=Request.data.get("username")
    password=Request.data.get("password")
    # print(username,password)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error":"Invalid Credentials"})
    refresh=RefreshToken.for_user(user)
    return Response ({
        "username":user.username,
        'role':user.role,
        'refresh':str(refresh),
        'access_token':str(refresh.access_token)
    })

# Get User Profile

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MyProfile(request):
    user=request.user
    print(user)

    profile_data={}
    if user.role=='customer' and hasattr(user, 'customer_profile'):
        p=user.customer_profile
        profile_data = {
            'phone':v.phone,
            'address':v.address

        }

    elif user.role=='deliverer' and hasattr(user,'deliverer_profile'):
        v=user.deliverer_profile
        profile_data = {
            'name':v.name,
            'phone':v.phone,
            'order':v.order,
        }
    return Response({
        'id': user.id,
        'username':user.username,
        'role':user.role,
        'profile_data':profile_data
    })

# LogOut
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Logout(request):
    try:
        refresh_token=request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message":"Logout successful"})
    except TokenError:
        return Response({"error":"Invalid or expired Token"})
    except Exception as e:
        return Response({"error":str(e)})
