from rest_framework import serializers

class TagInputField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, str):
            return value.split(":::") if value else []
        return value

    def to_internal_value(self, data):
        if isinstance(data, list):
            return ":::" .join(data)
        raise serializers.ValidationError("Expected a list of strings.")
