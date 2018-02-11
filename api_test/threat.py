import urllib2
import json
import re
import calendar
import time

# Known bad: 69.43.161.174
# Known good: 8.8.8.8
# Find more examples at https://www.alienvault.com/open-threat-exchange/dashboard


class IPDetails(object):
    def __init__(self, ip, *args, **kw):
        self.is_tracked = False
        self.is_error = False

        # TODO: Check for valid IP
        self.is_valid = self.is_valid_ip(ip)

        # Get IP reputation details from AlienVault API
        raw_response = Reputation.get_details(ip)
        # print "Raw response:{}".format(raw_response)

        if raw_response is not '':
            try:
                # Parse JSON response
                json_response = json.loads(raw_response)
                # print "Keys: {}".format(json_response.keys())
                # print "_id: {}".format(json_response['_id'])
                # print "_id.$id: {}".format(json_response['_id']['$id'])
            except ValueError:
                # TODO: Better error handling - Failed to parse JSON response
                pass
        else:
            json_response = {}

        # Store values from response that we care about
        self._id = json_response.get('_id', {}).get('$id', '')
        self.address = json_response.get('address', ip)
        self.reputation_val = json_response.get('reputation_val', 0)
        self.activities = json_response.get('activities', [])
        self.first_activity = self.get_first_activity_time()
        self.last_activity = self.get_last_activity_time()
        self.activity_types = self.get_activity_types()
        # print "activity[0]: {}".format(self.activities[0])

        return

    # Very simple IPv4 format checker
    # Taken from https://stackoverflow.com/a/25918107
    @staticmethod
    def is_valid_ip(ip):
        m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
        return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

    def get_first_activity_time(self):
        first_activity_time = None

        for activity in self.activities:
            activity_time = activity.get('first_date', {}).get('sec')
            if activity_time is not None and (first_activity_time is None or first_activity_time > activity_time):
                first_activity_time = activity_time

        return first_activity_time

    def get_last_activity_time(self):
        last_activity_time = None

        for activity in self.activities:
            activity_time = activity.get('last_date', {}).get('sec')
            if activity_time is not None and (last_activity_time is None or last_activity_time > activity_time):
                last_activity_time = activity_time

        return last_activity_time

    def get_activity_types(self):
        activity_types = dict()

        for activity in self.activities:
            activity_name = activity.get('name', None)
            if activity_name is not None:
                activity_types[activity_name] = activity_types.get(activity_name, 0) + 1

        return activity_types.keys()

class Reputation(object):
    @staticmethod
    def get_details(ip):
        if ip:
            try:
                # TODO: fetch raw results from the source
                # format: http://reputation.us.alienvault.com/panel/ip_json.php?ip=69.43.161.174
                url = "http://reputation.alienvault.com/panel/ip_json.php?ip={}".format(ip)
                print "threat request url: {}".format(url)
                return urllib2.urlopen(url).read()
            except:
                return "fetch_error"
        else:
            return None