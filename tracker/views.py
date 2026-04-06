from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.db.models.functions import ExtractMonth
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'tracker/profile.html')


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    monthly = expenses.annotate(month=TruncMonth('date')) \
                      .values('month') \
                      .annotate(total=Sum('amount')) \
                      .order_by('month')

    # Convert month to string
    for item in monthly:
        item['month'] = item['month'].strftime('%b %Y')

    return render(request, 'tracker/dashboard.html', {
        'total': total,
        'monthly': list(monthly)
    })


@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user)

    category = request.GET.get('category')
    search = request.GET.get('search')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category:
        expenses = expenses.filter(category=category)

    if search:
        expenses = expenses.filter(title__icontains=search)

    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])

    return render(request, 'tracker/home.html', {'expenses': expenses})

import csv
from django.http import HttpResponse

@login_required
def export_csv(request):
    expenses = Expense.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Date', 'Category'])

    for expense in expenses:
        writer.writerow([expense.title, expense.amount, expense.date, expense.category])

    return response


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('/')
    else:
        form = ExpenseForm()

    return render(request, 'tracker/add_expense.html', {'form': form})

def delete_expense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect('/')

def edit_expense(request, id):
    expense = Expense.objects.get(id=id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'tracker/edit_expense.html', {'form': form})

def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

    return render(request, 'tracker/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'tracker/login.html')

def user_logout(request):
    logout(request)
    return redirect('/login/')