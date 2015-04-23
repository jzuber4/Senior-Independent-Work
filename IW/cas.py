from django.contrib.auth.models import User
# CAS callback, called on login
def callback(tree):
    # tree[0][0] has the user's netID
    # there doesn't appear to be anything else in the tree
    username = tree[0][0].text
    user, user_created = User.objects.get_or_create(username=username)
