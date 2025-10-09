import os

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

# создаем root-пользователя
user, created = User.objects.get_or_create(
	username="root",
	defaults={"is_superuser": True, "is_staff": True}
)

if created or not user.has_usable_password():
	user.set_password("admin")
	user.save()
	print("✅ Root user created with password `admin`")

# создаем токен
token, _ = Token.objects.get_or_create(user=user)
print(f"✅ Root token: {token.key}")

# сохраняем токен в общий том
path = "/app/storage/root_token.txt"
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w") as f:
	f.write(token.key)

print(f"💾 Token saved to {path}")
