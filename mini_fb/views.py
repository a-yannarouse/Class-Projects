# File: views.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/20/2025
# Description: These are for the views for the mini_fb app, to show the profiles.
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from .models import Profile, StatusMessage, Image, StatusImage
from django.urls import reverse

# Create your views here.
class ShowAllProfilesView(ListView):
    ''' Define a view class to show all profiles. '''

    # Defines the model, template, and context object name for the all profiles page
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "Profiles"

class ShowProfilePageView(DetailView):
    ''' Define a view class to show all profiles. '''

    # Defines the model, template, and context object name for the singular profile page
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "Profile"

class CreateProfileView(CreateView):
    ''' A view to handle creation of a new Profile.
        (1) display the HTML form to user (GET)
        (2) process the form submission and store the new profile object (POST)
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    
    def form_valid(self, form):
        ''' Save the form data to the database.'''
        form.save()
        return super().form_valid(form)
    
class CreateStatusMessageView(CreateView):
    ''' A view to handle creation of a new status message on a Profile.'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    
    def get_context_data(self, **kwargs):
        ''' Return the dictionary of context variables for use in the template.'''
        
        # calling the superclass method
        context = super().get_context_data(**kwargs)

        # find/all the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this article into the context dictionary
        context['Profile'] = profile
        return context
    
    def form_valid(self, form):
        ''' This method handles the form and saves the new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment object before saving 
        it to the database. 
        '''

        # instrument our code to display form fields: 
        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
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

        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this article
        return reverse('show_profile', kwargs={'pk': pk})
    
class UpdateProfileView(UpdateView):
    ''' View class to handle update of a profile based on its PK.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

class DeleteStatusMessageView(DeleteView):
    ''' Define a view class to delete status messages. '''

    # Defines the model, template, and context object name for the singular profile page
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "message"

    def get_success_url(self):
        ''' Provide a URL to redirect to after creating a new comment.'''

        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class UpdateStatusMessageView(UpdateView):
    ''' View class to handle update of a status message based on its PK. '''

    model = StatusMessage
    template_name = "mini_fb/update_status_form.html"
    context_object_name = "status_message"
    fields = ['message']

    def get_success_url(self):
        ''' Provide a URL to redirect to after creating a new comment.'''

        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})