# File: views.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 03/31/2025
# Description: These are for the views for the voter_analytics app, to show the voters information.

# Create your views here.
from django.db.models.query import QuerySet #type: ignore
from django.shortcuts import render #type: ignore
from django.views.generic import ListView, DetailView #type: ignore
from django.db.models import Count
from . models import Voter
import plotly.io #type: ignore
import plotly.graph_objs as go #type: ignore


class VoterListView(ListView):
    '''View to display marathon results'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        ''' Get the list of voters and filter by party affiliation, date of birth, and voter score'''

        # start with entire queryset
        qs = super().get_queryset()
        request = self.request

        # Get filter params
        party = request.GET.get('party_affiliation')
        min_dob = request.GET.get('min_dob')
        max_dob = request.GET.get('max_dob')
        score = request.GET.get('voter_score')

        # Filter by party affiliation, date of birth, and voter score

        # Party affiliation filter
        if party:
            qs = qs.filter(party_affiliation=party.strip())

        # Date of birth filter
        if min_dob:
            qs = qs.filter(date_of_birth__year__gte=min_dob)

        if max_dob:
            qs = qs.filter(date_of_birth__year__lte=max_dob)

        # Voter score filter
        if score:
            qs = qs.filter(voter_score=score)

        # Election participation filters (checkboxes)
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        for field in election_fields:
            if request.GET.get(field) == 'on':  # Checkbox is checked
                qs = qs.filter(**{field: True})

        return qs
        
    def get_context_data(self, **kwargs):
        '''Add additional data to the context'''

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add any additional context variables
        context['years'] = range(1920, 2005)
        context['scores'] = [0, 1, 2, 3, 4, 5]
        return context

class VoterDetailView(DetailView):
    ''' Display results of a single runner'''

    model = Voter 
    context_object_name = "v" 
    template_name = 'voter_analytics/voters_detail.html'

class VoterGraphsView(ListView):
    ''' View to display graphs of voter data'''

    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'v'

    def get_queryset(self):
        ''' Get the list of voters and filter by party affiliation, date of birth, and voter score'''

        # start with entire queryset
        qs = super().get_queryset()
        request = self.request

        # Get filter params
        party = request.GET.get('party_affiliation')
        min_dob = request.GET.get('min_dob')
        max_dob = request.GET.get('max_dob')
        score = request.GET.get('voter_score')

        # Filter by party affiliation, date of birth, and voter score

        # Party affiliation filter
        if party:
            qs = qs.filter(party_affiliation=party.strip())

        # Date of birth filter
        if min_dob:
            qs = qs.filter(date_of_birth__year__gte=min_dob)

        if max_dob:
            qs = qs.filter(date_of_birth__year__lte=max_dob)

        # Voter score filter
        if score:
            qs = qs.filter(voter_score=score)

        # Election participation filters (checkboxes)
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        for field in election_fields:
            if request.GET.get(field) == 'on':  # Checkbox is checked
                qs = qs.filter(**{field: True})

        return qs

    def get_context_data(self, **kwargs):
        '''Add graph data to the context'''

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Aggregate data for the graphs
        voters = self.get_queryset()

        # For the form section
        context['years'] = range(1920, 2005)
        context['scores'] = [0, 1, 2, 3, 4, 5]

        # Histogram: Distribution of Voters by Year of Birth
        birth_year_counts = voters.values('date_of_birth__year').annotate(count=Count('id')).order_by('date_of_birth__year')
        birth_years = [entry['date_of_birth__year'] for entry in birth_year_counts]
        birth_year_values = [entry['count'] for entry in birth_year_counts]
        birth_year_fig = go.Figure(data=[go.Bar(x=birth_years, y=birth_year_values)])
        birth_year_fig.update_layout(title='Voter Distribution by Year of Birth', xaxis_title='Year of Birth', yaxis_title='Count')
        context['birth_year_graph'] = plotly.io.to_html(birth_year_fig, full_html=False)

        # Pie Chart: Distribution of Voters by Party Affiliation
        party_counts = voters.values('party_affiliation').annotate(count=Count('id'))
        party_labels = [entry['party_affiliation'] for entry in party_counts]
        party_values = [entry['count'] for entry in party_counts]
        party_fig = go.Figure(data=[go.Pie(labels=party_labels, values=party_values)])
        party_fig.update_layout(title='Voter Distribution by Party Affiliation')
        context['party_graph'] = plotly.io.to_html(party_fig, full_html=False)

        # Histogram: Distribution of Voters by Participation in Elections
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = {field: voters.filter(**{field: True}).count() for field in election_fields}
        election_labels = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        election_values = [election_counts[field] for field in election_fields]
        election_fig = go.Figure(data=[go.Bar(x=election_labels, y=election_values)])
        election_fig.update_layout(title='Voter Participation by Election', xaxis_title='Election', yaxis_title='Count')
        context['election_graph'] = plotly.io.to_html(election_fig, full_html=False)

        return context
