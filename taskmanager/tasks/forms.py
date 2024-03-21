import uuid
from django import forms
from django.core.cache import cache
from .models import Epic, Task, SubscribedEmail, FormSubmission
from .fields import EmailsListField
from django.db import IntegrityError, transaction

class TaskForm(forms.ModelForm):
    uuid = forms.UUIDField(
        required = False,
        widget = forms.HiddenInput(),
    )
    watchers = EmailsListField(required = False)
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "watchers",
            "file_upload",
            "image_upload",
        ]
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # Check if instance is provided and populate watchers field
        if self.instance and self.instance.pk:
            self.fields["watchers"].initial = ", ".join(
                email.email for email in self.instance.watchers.all()
            )
        self.fields["uuid"].initial = uuid.uuid4()
    
    def clean_uuid(self):
        uuid_value = self.cleaned_data.get("uuid")
        with transaction.atomic():
            # Try to record the form submission by UUID
            try:
                FormSubmission.objects.create(uuid = uuid_value)
            except IntegrityError:
                raise forms.ValidationError("THis form is already submitted.")
        return uuid_value

    def save(self, commit = True):
        # First save the task instance
        task = super().save(commit)
        # if commit is true
        if commit:
            # First, remove the old emails associated with this task
            task.watchers.all().delete()
            # Add the new emails to the email model
        for email_str in self.cleaned_data["watchers"]:
            SubscribedEmail.objects.create(
                email = email_str,
                task = task
            )
        return task
    
class ContactForm(forms.Form):
    from_email = forms.EmailField( required = True)
    subject = forms.CharField(required = True)
    message = forms.CharField(
        widget = forms.Textarea,
        required = True
    )

EpicFormSet = forms.modelformset_factory(Task, form=TaskForm,
extra=0)

# use caching in case you dont want to create a new model 
class TaskFormWithRedis(forms.ModelForm):
    uuid = forms.UUIDField(required=False, widget=forms.HiddenInput())
    watchers = EmailsListField(required=False)

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "watchers",
            "file_upload",
            "image_upload",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["watchers"].initial = ", ".join(
                email.email for email in self.instance.watchers.all()
            )
        self.fields["uuid"].initial = uuid.uuid4()
    
    def clean_uuid(self):
        uuid_value = str(self.cleaned_data.get("uuid"))

        was_set = cache.set(uuid_value, "submitted", nx = True)
        if not was_set:
            raise forms.ValidationError("This form has already been submitted.")
        return uuid_value
    
