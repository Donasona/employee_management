from django.shortcuts import render,redirect
from django.views.generic import View
from employee_app.forms import EmployeeForm
from employee_app.models import Employee
from django.shortcuts import get_object_or_404

# Create your views here.

class Createemployee(View):
    def get(self,request):
        form=EmployeeForm()
        return render(request,"createemployee.html",{"form":form})

    def post(self,request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.net_salary = (
                employee.base_salary + employee.bonus - employee.tax
            )
            employee.save()
            return redirect('employee_list')
        return render(request, 'createemployee.html', {'form': form})

class EmployeeListView(View):
    def get(self, request):
        employees = Employee.objects.all()
        return render(request, 'employee_list.html', {'employees': employees})
         

class UpdateEmployeeView(View):
    def get(self, request, **kwargs):
        employee = kwargs.get("pk")   
        form = EmployeeForm(instance=employee)
        return render(request, 'edit_employee.html', {'form': form})

    def post(self, request, **kwargs):
        employee = kwargs.get("pk")   
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            employee = form.save(commit=False)

            employee.net_salary = (
                employee.base_salary + employee.bonus - employee.tax
            )

            employee.save()
            return redirect('employee_list')

        return render(request, 'edit_employee.html', {'form': form})

class DeleteEmployeeView(View):
    def get(self, request, **kwargs):
        employee = kwargs.get("pk")  
        employees =get_object_or_404(Employee,employee=employee,user=request.user)
        employees.delete()
        return redirect('employee_list')

