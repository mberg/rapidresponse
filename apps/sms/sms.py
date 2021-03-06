from django.conf.urls.defaults import patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^join (.*)', "apps.sms.views.joining.MalawiJoin"),
    (r'^exit (.*)', "apps.sms.views.exiting.MalawiExit"),
    (r'^new (.*)', "apps.sms.views.adding.NewPatient"),
    (r'^child (.*)', "apps.sms.views.adding.NewChild"),
    (r'^cancel (.*)', "apps.sms.views.cancelling.MalawiCancel"),
    (r'^confirm (.*)', "apps.sms.views.confirming.MalawiConfirm"),
    (r'^report (.*)', "apps.sms.views.malnutrition_reporting.MalnutritionReport")
)