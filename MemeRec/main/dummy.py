from main.models import DummyModel

d1 = DummyModel(image_name='2021-09-22_22-00-19_UTC.jpg', user_id=1)
d2 = DummyModel(image_name='2021-10-20_19-00-13_UTC.jpg', user_id=1)
d3 = DummyModel(image_name='2021-11-04_10-01-04_UTC.jpg', user_id=1)
d4 = DummyModel(image_name='2021-12-09_22-00-13_UTC.jpg', user_id=1)


d1.save()
d2.save()
d3.save()
d4.save()
