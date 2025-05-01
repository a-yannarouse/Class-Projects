# File: views.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 04/18/2025
# Description: These are for the views for the project.

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import *
from .forms import *
import google.generativeai as genai
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.views import View
import re

class HomeView(TemplateView):
    template_name = 'project/home.html'


class ProfileListView(ListView):
    model = Profile
    template_name = 'project/profile_list.html'
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

class CreateProfileView(LoginRequiredMixin, FormView):
    template_name = 'project/create_profile.html'
    form_class = SubmissionForm
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_success_url(self) -> str:
        '''return the URL to redirect to after a successful form submission'''
        return reverse('profile_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.submitted_by = self.request.user.userprofile  # assumes UserProfile
        submission.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class SignupView(FormView):
    template_name = 'project/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('welcome')

    def form_valid(self, form):
        user = form.save()
        UserProfile.objects.create(user=user)
        login(self.request, user)
        return redirect('welcome')


class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'project/welcome.html'
    
class ChatbotSearchView(TemplateView):
    template_name = 'project/chatbot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip().lower()
        context['query'] = query
        context['results'] = []

        if query:
            def singularize(word):
                return word[:-1] if word.endswith('s') else word

            original_words = query.split()
            words = set(original_words + [singularize(w) for w in original_words])

            # Match tags
            tag_q = Q()
            for word in words:
                tag_q |= Q(name__icontains=word)
            tag_matches = Tag.objects.filter(tag_q)

            # Match profiles
            profile_q = Q()
            for word in words:
                profile_q |= Q(tags__name__icontains=word)
                profile_q |= Q(profile_type__icontains=word)
                profile_q |= Q(name__icontains=word)

            # Fallback full query match
            profile_q |= Q(profile_type__icontains=query)
            profile_q |= Q(name__icontains=query)

            results = Profile.objects.filter(profile_q).distinct()
            context['results'] = results

        return context

class GeminiChatbotView(TemplateView):
    template_name = 'project/chatbot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        context['query'] = query
        context['results'] = []
        context['ai_response'] = None

        if query:
            # Step 1: Configure Gemini
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash-002")

            # Pull creator names from the database
            creator_names = ", ".join(Profile.objects.values_list("name", flat=True)[:10]) or "no creators available"

            prompt = f"""
            You are a discovery assistant for a searchable archive of Black game creators and streamers.

            User query: "{query}"

            Here are 10 creators from our archive:
            {creator_names}

            Only recommend creators **from this list**. Do not suggest names that are not on this list. Return only the names of relevant creators and why they might match.

            Your task is to pick 2-3 creators from the list who best match the user's interest.
            Mention their name and explain briefly why they might be a good fit — based on what they do or what type of work they’re known for.
            If the user asked for a certain type of profile, make sure to include only those types.
            If you can't find a match, say "Sorry, I couldn't find any profiles that match your query.

            Format it as a short list, friendly tone, and skip generic advice. Keep it helpful.
            """

            try:
                response = model.generate_content(prompt)
                context['ai_response'] = response.text

                # Extract suggested names from Gemini's response
                suggested_names = re.findall(r'[A-Z][a-z]+(?: [A-Z][a-z]+)*', response.text)
                matched_profiles = Profile.objects.filter(name__in=suggested_names)

                if not matched_profiles.exists():
                    def singularize(word):
                        return word[:-1] if word.endswith('s') else word

                    words = query.lower().split()
                    words += [singularize(w) for w in words]
                    words = list(set(words))  # remove duplicates

                    # Match tags by any of the words
                    tag_q = Q()
                    for word in words:
                        tag_q |= Q(name__icontains=word)
                    tags = Tag.objects.filter(tag_q)

                    # Match profiles using tag, type, or name
                    profile_q = Q()
                    for word in words:
                        profile_q |= Q(tags__name__icontains=word)
                        profile_q |= Q(profile_type__icontains=word)
                        profile_q |= Q(name__icontains=word)

                    profile_q |= Q(profile_type__icontains=query)
                    profile_q |= Q(name__icontains=query)

                    matched_profiles = Profile.objects.filter(profile_q).distinct()

                context['results'] = matched_profiles

            except Exception as e:
                context['ai_response'] = f"Gemini API Error: {e}"

                
            # Filter the real data using tag-based search
            # Smarter tag + profile_type matching
            def singularize(word):
                # very basic plural handling
                return re.sub(r's$', '', word)

            words = [singularize(w) for w in query.lower().split()]
            tags = Tag.objects.filter(name__icontains=words[0])  # Start with first match
            for word in words[1:]:
                tags |= Tag.objects.filter(name__icontains=word)

            profile_qs = Profile.objects.filter(
                Q(tags__in=tags) |
                Q(profile_type__icontains=query) |
                Q(profile_type__icontains=words[0]) |
                Q(name__icontains=query)
            ).distinct()

            context['results'] = profile_qs

            # Update session history
            history = self.request.session.get('chat_history', [])
            history.append({'query': query, 'response': context['ai_response']})
            self.request.session['chat_history'] = history
            context['chat_history'] = history
        else:
            context['chat_history'] = self.request.session.get('chat_history', [])

        return context
    
def clear_chat_history(request):
    request.session['chat_history'] = []
    return HttpResponseRedirect(reverse('chatbot'))

def delete_chat_entry(request, index):
    chat_history = request.session.get('chat_history', [])

    if 0 <= index < len(chat_history):
        del chat_history[index]
        request.session['chat_history'] = chat_history

    return redirect('chatbot')

class ToggleBookmarkView(LoginRequiredMixin, View):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        user_profile = request.user.userprofile

        if profile in user_profile.bookmarked_profiles.all():
            user_profile.bookmarked_profiles.remove(profile)
        else:
            user_profile.bookmarked_profiles.add(profile)

        return HttpResponseRedirect(reverse('profile_detail', args=[pk]))

class BookmarkedProfilesView(LoginRequiredMixin, ListView):
    template_name = 'project/bookmarked_profiles.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return self.request.user.userprofile.bookmarked_profiles.all()
    
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'project/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        context['user_profile'] = user_profile
        context['bookmarks'] = user_profile.bookmarked_profiles.all()
        context['submissions'] = Submission.objects.filter(submitted_by=user_profile)

        return context
    
class EditUserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'project/edit_user_profile.html'

    def get_success_url(self) -> str:
        '''return the URL to redirect to after a successful form submission'''
        return reverse('user_profile')

    def get_object(self):
        return self.request.user.userprofile
    
class EditCreatorProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'project/edit_creator.html'

    def get_success_url(self):
        return reverse('profile_detail', args=[self.object.pk])

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
class SubmitWorkView(LoginRequiredMixin, FormView):
    form_class = WorkSubmissionForm
    template_name = 'project/submit_work.html'
    success_url = reverse_lazy('user_profile')

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.submitted_by = self.request.user.userprofile
        submission.save()
        return super().form_valid(form)