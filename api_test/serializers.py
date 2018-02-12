from rest_framework import serializers
from threat import IPDetails


class ActivitySerializer(serializers.Serializer):
    activity_type = serializers.CharField(source='name')
    first_date = serializers.IntegerField(source='first_date.sec', default=None)
    last_date = serializers.IntegerField(source='last_date.sec', default=None)


class DetailsSerializer(serializers.Serializer):
    is_valid = serializers.BooleanField()
    # TODO: serialize the rest of your values in IPDetails here
    # use of the simple serializers.Field() is acceptable
    address = serializers.CharField()
    id = serializers.CharField(source='_id')
    reputation_val = serializers.CharField()
    activities = ActivitySerializer(many=True)

    # The value of the earliest first_date.sec in activities[]
    first_activity = serializers.IntegerField()

    # The value of the latest last_date.sec in activities[]
    last_activity = serializers.IntegerField()

    # Enumeration of every unique value of activity.name in activities[]
    activity_types = serializers.ListField(child=serializers.CharField())


class VisitsSerializers(serializers.Serializer):
    address = serializers.CharField()
    timestamp = serializers.DateTimeField(format='%s')
    endpoint = serializers.CharField()


class TrafficSerializer(serializers.Serializer):
    alienvaultid = serializers.CharField(source='alien_vault_id')
    visits = VisitsSerializers(many=True)
