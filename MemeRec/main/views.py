from django.shortcuts import render, redirect
from .forms import NewUserForm, CheckboxForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import boto3
from django.http import JsonResponse
from django.template.loader import render_to_string
from main.feed_utilities_upd import put_updated_feed
import os
import re

dynamodb = boto3.resource('dynamodb')  
table = dynamodb.Table('Users')  


# def homepage(request):
#     return render(request=request, template_name='main/home.html')

def get_files_with_prefix(prefix, dirlist):
    regex = re.compile(f'^{prefix}.*jpg')
    return list(filter(regex.match, dirlist))

def homepage(request, user_id):
    # Connect to DynamoDB
    
    # Get feeds for user ID
    print(user_id)
    user_item = table.get_item(Key={'user_id': user_id})['Item']
    feeds = user_item['feed']
    print(feeds)
    # print(feeds)
    # Connect to EC2 and get image URLs
    image_urls = []
    dirlist = os.listdir('/Users/ramsankar/Documents/ISR/OnlyMemes/final_media/')
    feeds = [get_files_with_prefix(feed, dirlist) for feed in feeds]

    # media_len = [len(feed) for feed in feeds]
    
    # feeds = [['2022-09-22_15-02-12_UTC_1.jpg','2022-09-22_15-02-12_UTC_2.jpg','2022-09-22_15-02-12_UTC_3.jpg'],['2022-01-29_11-30-50_UTC_1.jpg','2022-01-29_11-30-50_UTC_2.jpg','2022-01-29_11-30-50_UTC_3.jpg','2022-01-29_11-30-50_UTC_4.jpg','2022-01-29_11-30-50_UTC_5.jpg']]
 
    for feed in feeds:
        image_urls.append(feed)
    # print('feeds for called user_id are', image_urls)    
    # Render template with image URLs
    context = {'image_urls': image_urls, 'user_id': user_id}
    
    # rendered_template = render_to_string('main/home.html', context)
    # print(rendered_template)

    return render(request, 'main/home2.html', context)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage", user_id= username)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            data = form.cleaned_data  # pranav
            username = data['username']  # pranav
            password = data['password1']  # pranav
            # print(data)  # pranav
            login(request, user)
            messages.success(request, "Registration successful.")
            item = {
                'user_id': username,
                'password': password,
                'chosen_tags': [],
                'liked_memes': [],
                'feed': []
            }
            table.put_item(Item=item)
            if len(item['chosen_tags']) == 0:
                return redirect('main:firstuser', user_id=username)
            else:
                return redirect('main:homepage', user_id=username)
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})

def firstuser_request(request, user_id):
    # form = CheckboxForm()
    user_data = table.get_item(Key={'user_id': user_id}).get('Item')
    if user_data and user_data['chosen_tags']:
        return redirect('main:homepage')
        # url = reverse('main:homepage') + f'?user_id={user_id}'
        # return redirect(url)
    if request.method == 'POST':
        form = CheckboxForm(request.POST)
        if form.is_valid():
            # data = form.cleaned_data
            interests = form.cleaned_data
            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET chosen_tags = :interests',
                ExpressionAttributeValues={':interests': interests}
            )
            
            return redirect('main:init_feed', user_id = user_id)
            return redirect('main:homepage' , user_id=user_id)
            # url = reverse('main:homepage') + f'?user_id={user_id}'
            # return redirect(url)
            # print(data)  # or do something else with the data
    else:
        form = CheckboxForm()

    # print(form)
    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_class = 'form-inline'
    helper.layout = Layout(
        
        Row(
            Column('cat', css_class='form-check'),
            Column('dog', css_class='form-check'),
            Column('voyaged', css_class='form-check'),           
            css_class='form-group'
        ),
         Row(
            # Column('barked', css_class='form-check'),
            Column('adulting', css_class='form-check'),
            Column('relationship', css_class='form-check'),
            Column('travel', css_class='form-check'),           
            css_class='form-group'
        ),
          Row(
            Column('couple', css_class='form-check'),
            Column('couplegoals', css_class='form-check'),
            Column('work', css_class='form-check'),           
            css_class='form-group'
        ),
           Row(
            # Column('goldenretriever', css_class='form-check'),
            Column('anime', css_class='form-check'),
            Column('doodles', css_class='form-check'),
            Column('cute', css_class='form-check'),           
            css_class='form-group'
        ),
            Row(
            Column('sleep', css_class='form-check'),
            Column('comics', css_class='form-check'),
            Column('funny', css_class='form-check'),           
            css_class='form-group'
        ),
         Row(
            Column('girlfriend', css_class='form-check'),
            Column('gaming', css_class='form-check'),
            Column('boyfriend', css_class='form-check'),           
            css_class='form-group'
        ),
          Row(
            Column('friends', css_class='form-check'),
            Column('food', css_class='form-check'),
            Column('music', css_class='form-check'),           
            css_class='form-group'
        ),
          Row(
            Column('childhood', css_class='form-check'), 
            Column('life', css_class='form-check'),
            Column('school', css_class='form-check'),           
            css_class='form-group'
        ),
        #    Row(
        #     Column('doggo', css_class='form-check'),
        #     Column('love', css_class='form-check'),
        #     Column('corgi', css_class='form-check'),           
        #     css_class='form-group'
        # ),
        #     Row(
        #     Column('animation', css_class='form-check'),
        #     Column('GoldenRetriever', css_class='form-check'),
        #     Column('adulthood', css_class='form-check'),           
        #     css_class='form-group'
        # ),
        #  Row(
            # Column('adulting', css_class='form-check'),
            # Column('anime', css_class='form-check'),
            # Column('childhood', css_class='form-check'),           
        #     css_class='form-group'
        # ),
        #   Row(
        #     Column('doge', css_class='form-check'),
        #     Column('quarantine', css_class='form-check'),
        #     Column('art', css_class='form-check'),           
        #     css_class='form-group'
        # ),
        #    Row(
        #     Column('job', css_class='form-check'),
        #     Column('satisfying', css_class='form-check'),
        #     Column('fluffy', css_class='form-check'),           
        #     css_class='form-group'
        # ),
        #     Row(
        #     Column('texting', css_class='form-check'),
        #     Column('halloween', css_class='form-check'),
        #     Column('cats', css_class='form-check'),           
        #     css_class='form-group'
        # ),
        #  Row(
        #     Column('relatable', css_class='form-check'),
        #     Column('hamster', css_class='form-check'),
            # Column('life', css_class='form-check'),           
        #     css_class='form-group'
        # ),
        #   Row(
            # Column('school', css_class='form-check'),
        #     Column('relationshipgoals', css_class='form-check'),
        #     Column('kitten', css_class='form-check'),           
        #     css_class='form-group'
        # ),
        #    Row(
        #     Column('phone', css_class='form-check'),
        #     Column('christmas', css_class='form-check'),
        #     Column('bunny', css_class='form-check'),           
        #     css_class='form-group'
        # ),
        #     Row(
        #     Column('parents', css_class='form-check'),
            
                      
        #     css_class='form-group'
        # ),
        
        Row(
            Submit('submit', 'Submit', css_class='btn btn-primary'),
        )

    )
    # added user_id pranav
    return render(request, 'main/firstuser.html', {'form': form, 'helper': helper, 'user_id': user_id})

@csrf_exempt
def like_image(request):
    if request.method == 'POST':
        button_name = request.POST.get('button_name')
        user_id = request.POST.get('user_id')
        button_name = button_name.split('_UTC')[0] + '_UTC'
        print('Button name:', button_name)
        if user_id:
            user_data = table.get_item(Key={'user_id': user_id}).get('Item')
            if user_data:
                liked_images = user_data.get('liked_images', [])
                if button_name not in liked_images:
                    liked_images.append(button_name)
                    table.update_item(
                        Key={'user_id': user_id},
                        UpdateExpression='SET liked_images = :liked_images',
                        ExpressionAttributeValues={
                            ':liked_images': liked_images}
                    )
        return JsonResponse({'message': 'Button name received'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def run_recommendations(request):
    user_id = request.POST.get('user_id')
    # print(user_id)
    # print("here")
    put_updated_feed(user_id)
    return JsonResponse({'message': 'success'})


def init_feed(request, user_id):
    return render(request, 'main/loading_animation.html', {'user_id': user_id})
    pass
