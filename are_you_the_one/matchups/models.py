from django.db import models


class Participant(models.Model):
    # id = models.IntegerField(primary_key=True)
    # username = models.TextField(max_length=100, unique=True)
    person_one_first_name = models.CharField(max_length=50)
    person_one_last_name = models.CharField(max_length=50)
    person_two_first_name = models.CharField(max_length=50, null=True, blank=True)
    person_two_last_name = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50)
    queries = models.IntegerField(default=0)
    query_limit = models.IntegerField(default=5)
    match_id = models.IntegerField(null=True, blank=True)
    found_match = models.BooleanField(default=False)
    found_match_timestamp = models.DateTimeField(null=True, blank=True)

    # USERNAME_FIELD = 'username'

    def __str__(self):
        if self.person_two_first_name:
            return '{} {} / {} {}'.format(self.person_one_first_name, self.person_one_last_name,
                                          self.person_two_first_name, self.person_two_last_name)
        return '{} {}'.format(self.person_one_first_name, self.person_one_last_name)
