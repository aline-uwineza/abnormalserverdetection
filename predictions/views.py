# predictions/views.py
from django.shortcuts import render, redirect
from .forms import ServerActivityForm
from .models import ServerActivity
from django.utils import timezone
from datetime import timedelta

import random

import plotly.express as px
import pandas as pd
import numpy as np
import joblib

# Load the trained model
model = joblib.load('predictions/abnormal_detection_model.joblib')

def predict_activity(request):
    prediction = None
    if request.method == 'POST':
        form = ServerActivityForm(request.POST)
        if form.is_valid():
            # Save the activity data to the database
            activity = form.save()

            # Prepare data for prediction
            input_data = np.array([
                activity.cpu_usage,
                activity.memory_usage,
                activity.disk_io,
                activity.network_traffic,
                activity.error_count,
            ]).reshape(1, -1)

            # Predict using the model
            prediction = model.predict(input_data)
            activity.target = prediction[0]  # Save the prediction result (0 or 1)
            activity.save()
    else:
        form = ServerActivityForm()

    # Fetch data for visualizations
    activity_data = ServerActivity.objects.all().values(
        'id',  # Ensure 'id' is included for line chart
        'target',
        'cpu_usage',
        'memory_usage',
        'disk_io',
        'network_traffic',
        'error_count'
    )
    
    if not activity_data.exists():  # Check if there is data in the queryset
        return render(request, 'predictions/predict_activity.html', {
            'form': form,
            'prediction': prediction,
            'chart': None,
            'cpu_usage_chart': None,
            'error_message': 'No activity data available for visualization.'
        })

    # Create DataFrame
    df = pd.DataFrame(activity_data)

    # Generate Pie Chart: Abnormal vs Normal Activities
    fig_pie = px.pie(
        df,
        names='target',
        title='Activity Prediction Distribution',
        labels={'target': 'Detection (0=Normal, 1=Abnormal)', 'value': 'Count'}
    )
    pie_chart = fig_pie.to_html(full_html=False)

    # Generate Line Chart: CPU Usage Over Time
    fig_line = px.line(
        df,
        x='id',
        y='cpu_usage',
        title='CPU Usage Over Time',
        labels={'id': 'Activity ID', 'cpu_usage': 'CPU Usage'}
    )
    line_chart = fig_line.to_html(full_html=False)

    # Render the template with data
    return render(request, 'predictions/predict_activity.html', {
        'form': form,
        'prediction': prediction,
        'chart': pie_chart,
        'cpu_usage_chart': line_chart,
    })

def history(request):
    # Fetch all activities
    activity_data = ServerActivity.objects.all()

    # Add a random created_at field (timestamp) for each activity
    for activity in activity_data:
        # Generate a random timedelta (between 0 and 30 days ago)
        random_days = random.randint(0, 0)
        random_time = timezone.now()  + timedelta(days=random_days)
        
        # Add a 'created_at' field to each activity
        activity.created_at = random_time

    return render(request, 'predictions/history.html', {'activity_data': activity_data})
def reset_database(request):
    # Reset the database by deleting all ServerActivity records
    ServerActivity.objects.all().delete()
    return redirect('history')  # Redirect to history view after reset
