from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
	name = forms.CharField(
		label='Your name', 
		error_messages={'required': 'Enter your name'})
	email = forms.EmailField(
		label='Your e-mail address', 
		error_messages={'required': 'Enter your e-mail address'})
	comment = forms.CharField(
		widget=forms.Textarea, 
		label="Your comment", 
		error_messages={'required': 'Enter your comment'})

	class Meta:
		model = Comment
		fields = ('name', 'email', 'comment')

	def __init__(self, *args, **kwargs):
		self.post = kwargs.pop('post')
		super().__init__(*args, **kwargs)

	def save(self):
		comment = super().save(commit=False)
		comment.post = self.post
		comment.save()
		return comment

class ContactForm(forms.Form):
	contact_name = forms.CharField(
		required=True,
		label='Your name',
		max_length='30',
		error_messages={'required': 'Enter your name'}
		)
	contact_email = forms.EmailField(
		required=True,
		label='Your email',
		max_length='50',
		error_messages={'required': 'Enter your e-mail address'}
		)
	content = forms.CharField(
		required=True,
		label='Your message',
		widget=forms.Textarea,
		error_messages={'required': 'Enter your message'}
		)
