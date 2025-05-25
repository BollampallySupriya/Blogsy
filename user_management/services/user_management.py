from Blogsy.user_management.constants import UserStatusConstants
from Blogsy.user_management.models import User
from Blogsy.user_management.serializers import UserSerializer


class UserManagementService:

    def create_user(username, first_name, last_name, email, country_code='', mobile_number='', is_public=True):
        try:
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name, 
                                    email=email, country_code=country_code, mobile_number=mobile_number, 
                                    is_public=is_public) 
            serializer = UserSerializer(user, many=False)
            return True, serializer.data
        except Exception as e:
            return False, {"error", str(e)}

    def update_user(user_id, data, partial=False):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user, data=data, partial=partial) 
            if serializer.is_valid():
                serializer.save()
                return True, {"message": "User updated successfully."}
            else:
                return False, serializer.errors
        except User.DoesNotExist as e:
            return False, {"message": "User not Found."}

    def delete_user(user_id):
        try:
            user = User.objects.get(id=user_id)
            user.status = UserStatusConstants.SUSPENDED
            user.save()
            return True, "User deleted successfully"
        except User.DoesNotExist as e:
            return False, "User not Found"

    def get_user_details(user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user, many=False)
            return True, serializer.data 
        except User.DoesNotExist as e:
            return False, {"error": "User not Found"}

    def list_users():
        users = User.objects.filter(status=UserStatusConstants.ACTIVE)
        serializer = UserSerializer(users, many=True)
        return serializer.data