from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from twilio.rest import Client

from tasks.forms import TaskForm


def send_sms(to, body):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_='+1234567890',  # Your Twilio number
        to=to
    )

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            # Send SMS
            send_sms(task.customer_mobile, f"Your task '{task.name}' has been created. Status: {task.status}.")
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})
