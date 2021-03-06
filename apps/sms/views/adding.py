from malnutrition.forms import Form
from malnutrition.forms import DateField, StringField, GenderField

from malnutrition.sms.views.adding import New
from malnutrition.sms.command import authenticated, FormFailed
from malnutrition.utils.parse import years_months

from apps.shortcuts import parser

#message, last, first, gender, dob, guardian="", contact="", zone=None

class NewPatientForm(Form):
    last_name = StringField(valid="(.+)")
    first_name = StringField(valid="(.+)")
    sex = GenderField()
    dob = DateField(format="%m%d%Y")
    dob.parser = parser
    guardian = StringField(valid="(.+)")
    contact = StringField(valid="(\d+)", required=False)
    
class NewPatient(New):
    @authenticated
    def post_init(self):
        self.form = NewPatientForm

    def pre_process(self):
        # malawi specific request
        years, months = years_months(self.form.clean.dob.data)
        if years > 5:
            raise FormFailed, "You have attempted to register child #%s. However, "\
                "the date of birth entered is %s. The age of this "\
                "child is above 5 years. Please resend SMS with corrected "\
                "age." % (self.form.clean.child.data, self.form.clean.dob.data.strftime("%m.%d.%Y"))

    def post_process(self):
        if self.form.clean.contact.data:
            self.data.case.mobild = self.form.clean.contact

    def error_already_exists(self):
        # malawi specific code
        return "You have attempted to register child #%s in %s GMC. However, this child already exists. If this is an error, please resend SMS with correct information. If this patient is new or a replacement, please use the EXIT command first, then re-register." % (self.form.clean.child.data, self.data.provider.clinic.name)
            
#Old Malawi Form. Useful when you are passing the ID to it.

class NewChildForm(Form):
    child = StringField(valid="(\d+)")
    gmc = StringField(valid="(\d+)")
    sex = GenderField()
    dob = DateField(format="%m%d%Y")
    dob.parser = parser
    contact = StringField(valid="(\d+)", required=False)
    
#Malawi version where you assign the id for the child
class NewChild(New):
    @authenticated
    def post_init(self):
        self.form = NewPatientForm
    
    def pre_process(self):
        # malawi specific request
        years, months = years_months(self.form.clean.dob.data)
        if years > 5:
            raise FormFailed, "You have attempted to register child #%s. However, "\
                "the date of birth entered is %s. The age of this "\
                "child is above 5 years. Please resend SMS with corrected "\
                "age." % (self.form.clean.child.data, self.form.clean.dob.data.strftime("%m.%d.%Y"))
    
    def post_process(self):
        if self.form.clean.contact.data:
            self.data.case.mobild = self.form.clean.contact
    
    def error_already_exists(self):
        # malawi specific code
        return "You have attempted to register child #%s in %s GMC. However, this child already exists. If this is an error, please resend SMS with correct information. If this patient is new or a replacement, please use the EXIT command first, then re-register." % (self.form.clean.child.data, self.data.provider.clinic.name)