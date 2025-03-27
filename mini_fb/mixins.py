from django.shortcuts import get_object_or_404 # type: ignore
from django.views.generic.base import ContextMixin # type: ignore
from .models import Profile

class LoggedInUserProfileMixin(ContextMixin):
    """
    A mixin to add the logged-in user's profile to the context.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Get the logged-in user's profile
            context['logged_in_profile'] = get_object_or_404(Profile, user=self.request.user)
        else:
            context['logged_in_profile'] = None
        return context