from collections import namedtuple
from functools import partial

from flask_login import current_user
from flask_principal import identity_loaded, Permission, RoleNeed, UserNeed

BlogPostNeed = namedtuple('blog_post', ['method', 'value'])
EditBlogPostNeed = partial(BlogPostNeed, 'edit')

class EditBlogPostPermission(Permission):
    def __init__(self, post_id):
        need = EditBlogPostNeed(unicode(post_id))
        super(EditBlogPostPermission, self).__init__(need)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

    # Assuming the User model has a list of posts the user
    # has authored, add the needs to the identity
    if hasattr(current_user, 'posts'):
        for post in current_user.posts:
            identity.provides.add(EditBlogPostNeed(unicode(post.id)))