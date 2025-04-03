# File: models.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 03/31/2025
# Description: These are for the models for the voter_analytics app.

from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one voter in the newtown town.
    Voter id, First Name, Last Name, Street Address, Precinct, Date of Birth, Date of Registration,
    Party Affiliation, Voter Score, V20 State, V21 Town, V21 Primary, V22 General, V23 Town
    '''

    voter_id = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    street_name = models.TextField()
    precinct = models.TextField()
    apartment_number = models.TextField()

    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    party_affiliation = models.CharField(max_length=3)
    
    street_number = models.IntegerField()
    zip_code = models.IntegerField()
    voter_score = models.IntegerField()

    v20state = models.BooleanField()
    v21town = models.BooleanField() 
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()


    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.street_number}, {self.street_name}, {self.apartment_number},{self.zip_code}), {self.date_of_birth}, {self.party_affiliation}, {self.voter_score}'
    
    def load_data(self):
        ''' Function to load data records from CSV file into Django model instances.'''

        # delete existing records to prevent duplicates:
        Voter.objects.all().delete()
        
        filename = '/Users/Yanni/Desktop/django/voter_analytics/newton_voters.csv'
        f = open(filename)
        f.readline()

        for line in f:
            fields = line.split(',')
        
            try:
                # create a new instance of Result object with this record from CSV
                voter = Voter(
                            voter_id=fields[0].strip(),
                            last_name=fields[1].strip(),
                            first_name=fields[2].strip(),
                            street_number=fields[3] if fields[3].strip() else None,
                            street_name=fields[4].strip(),
                            apartment_number=fields[5].strip() if fields[5].strip() else None,
                            zip_code=fields[6].strip(),
                            date_of_birth=fields[7].strip(),
                            date_of_registration=fields[8].strip(),
                            party_affiliation=fields[9].strip(),
                            precinct=fields[10].strip(),
                            v20state=fields[11].strip().upper() == 'TRUE',
                            v21town=fields[12].strip().upper() == 'TRUE',
                            v21primary=fields[13].strip().upper() == 'TRUE',
                            v22general=fields[14].strip().upper() == 'TRUE',
                            v23town=fields[15].strip().upper() == 'TRUE',
                            voter_score=fields[16].strip(),
                )
            
                voter.save() # commit to database
                print(f'Created voter: {voter}')
                
            except:
                print(f"Skipped: {fields}")
        
        print(f'Done. Created {len(Voter.objects.all())} voters.')