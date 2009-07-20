from django.conf import settings
from apps.shortcuts import has_roles

def processor(self):
    user = self.user
    tabs = []
    if has_roles(user, ["partner", "national", "district"]):
        tabs.append({ "link": "/", "title": "National" })
        tabs.append({ "link": "/district/", "title": "District"})
    if has_roles(user, ["partner", "national", "district", "clinic"]):
        tabs.append({ "link": "/clinic/", "title": "Clinic"})
        tabs.append({ "link": "/child/", "title": "Child"})
        tabs.append({ "link": "/hsa/", "title": "HSA"})
    if has_roles(user, ["partner", "national", "district"]):
        tabs.append({ "link": "/setup/", "title": "Setup"})
    context = {
        "site": { "title": "RapidResponse",
                  "tabs": tabs },
        "settings": settings,
    }
    return context