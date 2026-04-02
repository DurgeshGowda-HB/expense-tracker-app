from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

def dashboard(request):
    total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
    return render(request, 'tracker/dashboard.html', {'total': total})

def home(request):
    expenses = Expense.objects.all()

    category = request.GET.get('category')
    search = request.GET.get('search')

    if category:
        expenses = expenses.filter(category=category)

    if search:
        expenses = expenses.filter(title__icontains=search)

    return render(request, 'tracker/home.html', {'expenses': expenses})

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