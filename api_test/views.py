from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from models import Users, Visits
from threat import IPDetails
from serializers import *


# Visit tracking cookie
COOKIE_NAME = 'AlienVaultId'
COOKIE_MAX_AGE = 60*60*24*365


class APIRoot(APIView):
    def get(self, request):
        return Response({
            'IP Details': reverse('threat_details', request=request),
        })


class IPDetailsView(APIView):
    def get(self, request, ip, *args, **kw):
        print "Requested IP: {}".format(ip)
        details_request = IPDetails(ip, *args, **kw)

        # Track API usage
        alien_vault_id = request.COOKIES.get(COOKIE_NAME, None)
        if alien_vault_id is None:
            user = Users()
        else:
            try:
                user = Users.objects.get(alien_vault_id=alien_vault_id)
            except:
                user = Users()
        user.save()

        visit = Visits(
            user=user,
            address=request.META.get('REMOTE_ADDR'),  # TODO: Handle X-Forwarded-For
            endpoint='api/threat/ip/{}'.format(ip)
        )
        visit.save()

        result = DetailsSerializer(details_request)
        response = Response(result.data, status=status.HTTP_200_OK)

        response.set_cookie(
            COOKIE_NAME,
            user.alien_vault_id,
            max_age=COOKIE_MAX_AGE
        )

        return response

# TODO: View for /api/traffic
class TrafficView(APIView):
    def get(self, request):
        users = Users.objects.order_by('alien_vault_id').all()
        serialize = TrafficSerializer(users, many=True)
        response = Response(serialize.data, status=status.HTTP_200_OK)
        return response