"""

Note: these tests depend on Pinax/projects.

>>> from classifieds.models import *
>>> from django.contrib.auth.models import User

>>> bob = User(username='bob')
>>> bob.save()
>>> alice = User(username='alice')
>>> alice.save()

>>> offer1 = Listing(
...     owner=bob,
...     title='test offer',
...     description='something good',
...     want='something better')
>>> offer1.save()
>>> offer2 = Listing(
...     owner=alice,
...     title='another test offer',
...     description='something better',
...     want='whatever')
>>> offer2.save()

"""
