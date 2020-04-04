from django.contrib.auth.models import User 

class EmailBackend(object):
	def authenticate(self,request, username, password):
		try:
			user=User.objects.get(email=username)
			success = user.check_password(password)
			if success:
				return user

		except User.DoesNotExist:
			pass

		return None
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

	def __str__(self):
		return Email 