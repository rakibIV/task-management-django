from django import forms
from tasks.models import Task,TaskDetail


# Djnago Form

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea,label="Task Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget ,label="Due Date")
    assigned_to = forms.MultipleChoiceField(label="Assigned To",widget=forms.CheckboxSelectMultiple,choices=[])
    
    def __init__(self, *args, **kwargs):
        # print(args,kwargs)
        employees = kwargs.pop('employees',[])
        # employees = kwargs
        # print(employees)
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].choices = [(emp.id, emp.name) for emp  in employees ]
        
        

''' Mixin to Style the Form Fields '''


class StyledFormMixin:
    
    
    def apply_styled_widgets(self):
        default_classes = "w-full px-3 py-2 border rounded border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 m-3"
        for field_name, field in self.fields.items():
            for field_name, field in self.fields.items():
                if isinstance(field.widget, forms.TextInput):
                    field.widget.attrs.update({
                        "class": default_classes,
                        "placeholder": f"Enter {field.label.lower()}"
                            
                    })
                elif isinstance(field.widget, forms.Textarea):
                    field.widget.attrs.update({
                        "class": default_classes,
                        "placeholder": f"Enter {field.label.lower()}",
                        "rows": 5
                    })
                    
                elif isinstance(field.widget, forms.SelectDateWidget):
                    print("Inside Date Widget")
                    field.widget.attrs.update({
                        "class": "w-full md:w-1/4 px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white",
                    })
                    
                elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                    print("Inside Checkbox Widget")
                    field.widget.attrs.update({
                        "class": "pt-2 mt-3 active:shadow-blue-300 active:outline-blue-300"
                    })
                    
                # elif isinstance(field.widget, forms.ChoiceField):
                #     print("Inside choice field Widget")
                #     field.widget.attrs.update({
                #         "class": "border border-gray-300 p-3 rounded-lg shadow-md mb-5 focus:shadow-blue-300 focus:outline-blue-300 m-2"
                #     })
                    
                else:
                    field.widget.attrs.update({
                        "class": "md:w-1/3 px-3 py-2 border rounded border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 m-8",
                    })




        
        
# Django Model Form

class TaskModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title","description","due_date", "assigned_to"]
        widgets = {
            "due_date": forms.SelectDateWidget,
            "assigned_to": forms.CheckboxSelectMultiple
        }

        # widgets = {
        #     "title":forms.TextInput(attrs ={
        #         "class": "border border-gray-300 w-full p-2 rounded-lg shadow-md mb-5 focus:shadow-blue-300 focus:outline-blue-300",
        #         "placeholder": "Task Title"
        #     }),
        #     "description": forms.Textarea(attrs={
        #         "class": "border border-gray-300 w-full p-2 rounded-lg shadow-md mb-5 focus:shadow-blue-300 focus:outline-blue-300",
        #         "placeholder": "Task Description"
        #     }),
        #     "due_date": forms.SelectDateWidget(attrs={
        #         "class": "border border-gray-300 p-3 rounded-lg shadow-md mb-5 focus:shadow-blue-300 focus:outline-blue-300 m-2"
        #         }),
        #     "assigned_to": forms.CheckboxSelectMultiple(attrs={
        #         "class": "pt-2 mt-3 active:shadow-blue-300 active:outline-blue-300"
        #         })
        # }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        
        
        
        
class TaskDetailModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority','notes','asset']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()