from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm

def home(request):
    expenses = Expense.objects.all()
    return render(request, 'tracker/home.html', {'expenses': expenses})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ExpenseForm()

    return render(request, 'tracker/add_expense.html', {'form': form})

def delete_expense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect('/')