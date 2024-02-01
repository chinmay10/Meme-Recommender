from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import csv

# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class CheckboxForm(forms.Form):
    with open('Recommender/tags.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        # Assuming the CSV file has columns named 'column1', 'column2', and 'column3'
        tags_values = []
        for row in reader:
            tags_values.append(row['tag_name'])
            
    tags_values = tags_values[:50]
    # print(tags_values)
    cat = forms.BooleanField(label='cat', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    dog = forms.BooleanField(label='dog', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    voyaged = forms.BooleanField(label='voyaged', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # barked = forms.BooleanField(label='barked', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    relationship = forms.BooleanField(label='relationship', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    travel = forms.BooleanField(label='travel', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    couple = forms.BooleanField(label='couple', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    couplegoals = forms.BooleanField(label='couplegoals', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    work = forms.BooleanField(label='work', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # goldenretriever = forms.BooleanField(label='goldenretriever', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    doodles = forms.BooleanField(label='doodles', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    cute = forms.BooleanField(label='cute', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    sleep = forms.BooleanField(label='sleep', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    comics = forms.BooleanField(label='comics', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    funny = forms.BooleanField(label='funny', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    girlfriend = forms.BooleanField(label='girlfriend', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    gaming = forms.BooleanField(label='gaming', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    boyfriend = forms.BooleanField(label='boyfriend', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    friends = forms.BooleanField(label='friends', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    food = forms.BooleanField(label='food', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    music = forms.BooleanField(label='music', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # doggo = forms.BooleanField(label='doggo', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # love = forms.BooleanField(label='love', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # corgi = forms.BooleanField(label='corgi', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # animation = forms.BooleanField(label='animation', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # GoldenRetriever = forms.BooleanField(label='GoldenRetriever', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # adulthood = forms.BooleanField(label='adulthood', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    adulting = forms.BooleanField(label='adulting', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    anime = forms.BooleanField(label='anime', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    childhood = forms.BooleanField(label='childhood', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # doge = forms.BooleanField(label='doge', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # quarantine = forms.BooleanField(label='quarantine', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # art = forms.BooleanField(label='art', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # job= forms.BooleanField(label='job', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # satisfying= forms.BooleanField(label='satisfying', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # fluffy= forms.BooleanField(label='fluffy', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # texting= forms.BooleanField(label='texting', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # halloween = forms.BooleanField(label='halloween', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # cats = forms.BooleanField(label='cats', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # relatable = forms.BooleanField(label='relatable', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    life = forms.BooleanField(label='life', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    school = forms.BooleanField(label='school', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # relationshipgoals = forms.BooleanField(label='relationshipgoals', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # kitten = forms.BooleanField(label='kitten', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # phone = forms.BooleanField(label='phone', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # christmas = forms.BooleanField(label='christmas', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # bunny = forms.BooleanField(label='bunny', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # parents = forms.BooleanField(label='parents', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
    # hamster = forms.BooleanField(label='hamster', required=False, widget=forms.CheckboxInput(attrs={'class': 'my-class'}))
        