import random
from uuid import uuid4
from datetime import timedelta
from django.utils.timezone import now
from core.models import  Facilities
from users.models import Invite

def test():
    facilities = list(Facilities.objects.all())

    if not facilities:
        print("❗️ Сначала нужно создать хотя бы один объект (Facility)")
    else:
        for i in range(100):
            Invite.objects.create(
                email=f'test{i}@example.com',
                token=uuid4().hex,
                role='admin',
                facility=random.choice(facilities),
                used_at=now()
            )
        print("✅ 100 тестовых приглашений создано")
