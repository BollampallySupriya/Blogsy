from ..constants import FollowerStatusConstants
from ..models import Followers, User
from ..serializers import FollowerSerializer


class FollowerManagementService:

    def send_follow_request(user_id, follower_id):
        try:
            print(user_id, follower_id)
            user = User.objects.get(id=user_id)
            follower = User.objects.get(id=follower_id)
            if user.is_public:
                status, message = FollowerStatusConstants.ACCEPTED, "Started following"
            else:
                status, message = FollowerStatusConstants.PENDING, "Follow request sent"
            Followers.objects.create(user=user, follower=follower, status=status)
            return True, {"message": message}
        except User.DoesNotExist as e:
            return False, {"message": "user does not exist."}
        except Exception as e:
            return False, {"message": "unable to send follow request. try again later."}

    def approve_follow_request(request_id):
        try:
            follow_request = Followers.objects.get(id=request_id, status=FollowerStatusConstants.PENDING)
            follow_request.status = FollowerStatusConstants.ACCEPTED
            follow_request.save()
            return True, {"message": "Follow request approved"}
        except Followers.DoesNotExist:
            return False, {"message": "No pending request found"} 

    def decline_follow_request(request_id):
        try:
            follow_request = Followers.objects.get(id=request_id, status=FollowerStatusConstants.PENDING)
            follow_request.status = FollowerStatusConstants.REJECTED
            follow_request.save()
            return True, {"message": "Follow request rejected"}
        except Followers.DoesNotExist:
            return False, {"message": "No pending request found"}  

    def list_followers(user_id):
        followers = Followers.objects.filter(user_id=user_id, status=FollowerStatusConstants.ACCEPTED)
        serializer = FollowerSerializer(followers, many=True)
        return serializer.data

    def list_following(user_id):
        following = Followers.objects.filter(follower_id=user_id, status=FollowerStatusConstants.ACCEPTED)
        serializer = FollowerSerializer(following, many=True)
        return serializer.data 

    def remove_follower(follower_id):
        try:
            follower = Followers.objects.get(id=follower_id, status=FollowerStatusConstants.ACCEPTED)
            follower.delete()
            return True, {"message": "Follower removed successfully"}
        except Followers.DoesNotExist:
            return False, {"message": "Follower not found"}

    def unfollow(following_id):
        try:
            follower = Followers.objects.get(id=following_id)
            follower.delete()
            return True, {"message": "Unfollowed successfully"}
        except Followers.DoesNotExist:
            return False, {"message": "Cannot unfollow. Please try again later"}