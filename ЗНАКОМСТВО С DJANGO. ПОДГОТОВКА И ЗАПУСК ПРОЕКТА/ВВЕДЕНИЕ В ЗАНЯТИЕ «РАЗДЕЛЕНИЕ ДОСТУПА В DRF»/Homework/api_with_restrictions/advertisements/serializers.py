from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from advertisements.models import Advertisement, AdvertisementStatusChoices

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)

class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at',)

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        # Проверяем только если объявление создается или меняется статус на OPEN
        status = data.get('status') or self.instance.status if self.instance else data.get('status', AdvertisementStatusChoices.OPEN)
        
        if status == AdvertisementStatusChoices.OPEN:
            user = self.context['request'].user
            open_ads_count = Advertisement.objects.filter(
                creator=user, 
                status=AdvertisementStatusChoices.OPEN
            ).count()
            
            # Если это создание нового — лимит 10. Если обновление старого — лимит тоже 10 (но учитываем, что текущее уже может быть OPEN)
            if not self.instance and open_ads_count >= 10:
                raise ValidationError("У вас не может быть более 10 открытых объявлений.")
        
        return data
