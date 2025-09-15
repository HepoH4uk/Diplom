from django.contrib import admin

from tests.models import Test, Question, TestAttempt, Answer

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(TestAttempt)
admin.site.register(Answer)
