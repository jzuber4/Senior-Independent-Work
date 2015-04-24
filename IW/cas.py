from django.contrib.auth.models import User
from quiz_service.models import UserInfo
from quiz_service.service import is_admin
# CAS callback, called on login
def callback(tree):
    # tree[0][0] has the user's netID
    # there doesn't appear to be anything else in the tree
    username = tree[0][0].text
    user, user_created = User.objects.get_or_create(username=username)
    is_teacher = is_admin(user.username)

    # get user permission on login
    if user_created:
        new_userinfo = UserInfo(user=user, is_teacher=is_teacher)
        new_userinfo.save()
    else:
        user.userinfo.is_teacher = is_teacher
        user.userinfo.save()
