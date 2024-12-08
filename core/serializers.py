from rest_framework import serializers
from core import models
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    login = LoginSerializer(many=False)

    class Meta:
        model = models.UserProfile
        exclude = ['created_at']


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MuscleGroup
        exclude = ['created_at']


class ExerciseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Exercise
        exclude = ['created_at']
        extra_kwargs = {
            'id': {'read_only': False}
        }


class TrainingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = LoginSerializer(many=False, required=False, read_only=True)

    class Meta:
        model = models.Training
        exclude = ['created_at']
        extra_kwargs = {
            'id': {'read_only': False}
        }


class TrainingExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(many=False, read_only=True)
    training = TrainingSerializer(many=False, read_only=True)

    class Meta:
        model = models.TrainingExercise
        exclude = ['created_at']

    def create(self, validated_data):
        exercise = models.Exercise.objects.get(id=validated_data.pop('exercise').get("id"))
        training = models.Training.objects.get(id=validated_data.pop('training').get("id"))

        return models.TrainingExercise.objects.create(
            exercise=exercise, training=training, **validated_data
        )

    def update(self, instance, validated_data):
        instance.exercise = models.Exercise.objects.get(id=validated_data.pop('exercise').get("id"))
        instance.training = models.Training.objects.get(id=validated_data.pop('training').get("id"))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        exercise_data = data.get('exercise')
        training_data = data.get('training')

        if not exercise_data or 'id' not in exercise_data:
            raise serializers.ValidationError({"exercise": "ID do exercício é obrigatório."})
        if not training_data or 'id' not in training_data:
            raise serializers.ValidationError({"training": "ID do treino é obrigatório."})

        internal_data = super().to_internal_value(data)
        internal_data['exercise'] = exercise_data
        internal_data['training'] = training_data
        return internal_data


class MealSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Meal
        exclude = ['created_at', 'user']


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        exclude = ['created_at']


class MealFoodSerializer(serializers.ModelSerializer):
    meal = MealSerializer(many=False, read_only=True)
    food = FoodSerializer(many=False, read_only=True)

    class Meta:
        model = models.MealFood
        exclude = ['created_at']



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True)  # , validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
