# File: views.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/20/2025
# Description: These are for the views for the mini_fb app, to show the profiles.
from django.shortcuts import get_object_or_404, redirect # type: ignore
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View # type: ignore
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from .models import Profile, StatusMessage, Image, StatusImage
from django.urls import reverse # type: ignore
from django.shortcuts import redirect # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin # for authorization # type: ignore
from django.contrib.auth.forms import UserCreationForm # the Django user model # type: ignore
from django.contrib.auth.models import User # the Django user model # type: ignore
from django.contrib.auth import login # type: ignore
from django.views.generic.base import ContextMixin # type: ignore

# Create your views here.

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
    
# Public Views (no login required)
class ShowAllProfilesView(LoggedInUserProfileMixin, ListView):
    ''' Define a view class to show all profiles. '''

    # Defines the model, template, and context object name for the all profiles page
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "Profiles"

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllProfilesView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllProfilesView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)

class ShowProfilePageView(LoggedInUserProfileMixin, DetailView):
    ''' Define a view class to show all profiles. '''

    # Defines the model, template, and context object name for the singular profile page
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "Profile"

    def get_object(self):
        ''' Fetch the Profile object dynamically. '''
        pk = self.kwargs.get('pk')  # Get `pk` from the URL if it exists
        if pk:
            return get_object_or_404(Profile, pk=pk)
        return get_object_or_404(Profile, user=self.request.user)

class CreateProfileView(LoggedInUserProfileMixin, CreateView):
    ''' A view to handle creation of a new Profile.
        (1) display the HTML form to user (GET)
        (2) process the form submission and store the new profile object (POST)
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    
    def get_context_data(self, **kwargs):
        ''' Provide context data to the template, including the UserCreationForm. '''
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        ''' Save the form data to the database with the proper user.'''
        # Reconstruct the UserCreationForm from POST data
        user_creation_form = UserCreationForm(self.request.POST)
        if user_creation_form.is_valid():
            # Save the new User object
            user = user_creation_form.save()
            # Log the user in
            login(self.request, user)
            # Attach the User to the Profile instance
            form.instance.user = user
            # Delegate the rest to the superclass
            return super().form_valid(form)
        else:
            # If the UserCreationForm is invalid, re-render the page with errors
            return self.render_to_response(self.get_context_data(form=form, user_creation_form=user_creation_form))
    
# Protected Views (login required)
class CreateStatusMessageView(LoginRequiredMixin, LoggedInUserProfileMixin, CreateView):
    ''' A view to handle creation of a new status message on a Profile.'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        ''' Return the dictionary of context variables for use in the template.'''
        
        # calling the superclass method
        context = super().get_context_data(**kwargs)

        # find the profile for the logged-in user
        profile = get_object_or_404(Profile, user=self.request.user)

        # add this article into the context dictionary
        context['Profile'] = profile
        return context
    
    def form_valid(self, form):
        ''' This method handles the form and saves the new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment object before saving 
        it to the database. 
        '''

        # find the profile for the logged-in user
        profile = get_object_or_404(Profile, user=self.request.user)

        # attach the article to the comment
        form.instance.profile = profile # set the FK

        # save the status message to database
        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')
        for file in files:
            # create an Image object and save it
            image = Image(image_file=file, profile=profile)
            image.save()

            # create and save a StatusImage object
            status_image = StatusImage(status_message=sm, image_file=image)
            status_image.save()

        # delegate the work to the superclass methom form_valid:
        return super().form_valid(form)
    
    def get_success_url(self):
        ''' Provide a URL to redirect to after creating a new comment.'''

        # call reverse to generate the URL for this article
        return reverse('show_profile')
    
class UpdateProfileView(LoginRequiredMixin, LoggedInUserProfileMixin, UpdateView):
    ''' View class to handle update of a profile based on its PK.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        ''' Fetch the Profile object for the logged-in user. '''
        return get_object_or_404(Profile, user=self.request.user)
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

class DeleteStatusMessageView(LoginRequiredMixin, LoggedInUserProfileMixin, DeleteView):
    ''' Define a view class to delete status messages. '''

    # Defines the model, template, and context object name for the singular profile page
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "message"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        ''' Ensure the logged-in user is the owner of the profile associated with the status message. '''
        status_message = self.get_object()
        if request.user != status_message.profile.user:
            return redirect(f"{reverse('show_profile')}?pk={status_message.profile.pk}")

        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        ''' Provide a URL to redirect to after creating a new comment.'''
        return reverse('show_profile')
    
class UpdateStatusMessageView(LoginRequiredMixin, LoggedInUserProfileMixin, UpdateView):
    ''' View class to handle update of a status message based on its PK. '''

    model = StatusMessage
    template_name = "mini_fb/update_status_form.html"
    context_object_name = "status_message"
    fields = ['message']

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        ''' Ensure the logged-in user is the owner of the profile associated with the status message. '''
        status_message = self.get_object()
        if request.user != status_message.profile.user:
            return redirect('show_profile', pk=status_message.profile.pk)

        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        ''' Provide a URL to redirect to after creating a new comment.'''

        return reverse('show_profile')

class AddFriendView(LoginRequiredMixin, LoggedInUserProfileMixin, View):
    ''' View class to handle adding a friend to a profile. '''

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        ''' Handle the request to add a friend. '''

        # retrieve the PKs from the URL pattern
        friend_pk = self.kwargs['other_pk']

        # find the logged-in user's profile and the friend's profile
        profile = get_object_or_404(Profile, user=self.request.user)
        friend = get_object_or_404(Profile, pk=friend_pk)

        # add the friend to the profile
        profile.add_friend(friend)

        # redirect to the profile page
        return redirect(f"{reverse('show_profile')}?pk={friend_pk}")
    
class ShowFriendSuggestionsView(LoginRequiredMixin, LoggedInUserProfileMixin, DetailView):
    ''' Defines a view class to show friend suggestions. '''

    # Defines the model, template, and context object name for the singular profile page
    login_url = '/mini_fb/login/'
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "Profile"

    def get_object(self):
        ''' Fetch the Profile object for the logged-in user. '''
        return get_object_or_404(Profile, user=self.request.user)

class ShowNewsFeedView(LoginRequiredMixin, LoggedInUserProfileMixin, DetailView):
    ''' Defines a view class to show news feeds. '''

    # Defines the model, template, and context object name for the singular profile page
    login_url = '/mini_fb/login/'
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "Profile"

    def get_object(self):
        ''' Fetch the Profile object for the logged-in user. '''
        return get_object_or_404(Profile, user=self.request.user)