from unicodedata import name
from django.contrib.gis.db import models #because we are using gid db
import datetime
from django.db.models.deletion import SET, SET_NULL
from django.utils.translation import gettext_lazy as _
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField


class Myplaces(models.Model):

    name = models.CharField(max_length=100) #name of your place
    description = models.TextField()
    District = models.CharField(max_length=100) #name of your place
    province = models.CharField(max_length=100) #name of your place
    Country = models.CharField(max_length=100) #name of your place
    location = models.PointField()

    def __str__(self):

        return self.name

   

class Beneficiary(models.Model):
    """
    Implements the Beneficiary properties and required methods.
    """
    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, null=True, blank=True
    )
    gender = models.CharField(
        max_length=100
    )
    registered_facility = models.ForeignKey(Myplaces, on_delete=models.SET_NULL, null=True, blank=True)
    sex = models.CharField( max_length=100)
    phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )
    email = models.EmailField(max_length=200, null=True, blank=True)
    beneficiary_ids = models.CharField(max_length=100, editable=False)
    art_status = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    last_vl = models.IntegerField(null=True, blank=True)
    hiv_status = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    marital_status = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    name_of_spouse = models.CharField(
        max_length=200, null=True, blank=True
    )
    number_of_children = models.IntegerField(
         null=True, blank=True
    )
    number_of_siblings = models.IntegerField(
        null=True, blank=True
    )

    education_level = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    address = models.TextField(
        null=True,
        blank=True,
    )
    alive = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Beneficiary"
        verbose_name_plural = "Beneficiaries"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_age(self):
        """
        Calculates the Beneficiaries age from birth date.
        """
        days_in_year = 365.2425
        age = int((datetime.date.today() - self.date_of_birth).days / days_in_year)
        return age

# # Created Agent Model
class Agent(models.Model):
#     """
#     Create agent detail table with its attributes or columns.
#     """
  
    first_name = models.CharField(
        _("First Name"), max_length=200, null=True, blank=True
    )
    last_name = models.CharField(_("Last Name"), max_length=200, null=False)
    birthdate = models.DateField(
        _("Birth Date"), auto_now_add=False, null=True, blank=True
    )
    agent_id = models.CharField(max_length=100, editable=False)
    gender = models.CharField(
         max_length=50
    )
    # location = models.PointField(
    #     _("Location"), geography=True, blank=True, null=True, srid=4326
    # )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("beneficiary:agent_detail", kwargs={"pk": self.pk})



# Created Medical Records Model
class MedicalRecord(models.Model):
    """
    Beneficiary's Service.
    """

    beneficiary = models.ForeignKey(
        Beneficiary,
        on_delete=models.CASCADE,
    )
    provider_comments = models.TextField(_("Provider Comments"), null=True, blank=True)
    interaction_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    prescription = models.TextField(_("Prescription Comments"), null=True, blank=True)
    no_of_days = models.IntegerField(_("No of Days"), null=True, blank=True)
    when_to_take = models.TextField(
        _("When to Take"), max_length=500, null=True, blank=True
    )
    lab = models.TextField(_("Lab Comments"), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Medical Record")
        verbose_name_plural = _("Medical Records")
        ordering = ["-created"]

    def __str__(self):
        return f"Medical Record for: {self.beneficiary}"

    def get_absolute_url(self):
        return reverse("beneficiary:details", kwargs={"pk": self.beneficiary.pk})

    def get_files_dict(self):
        return json.loads(self.documents)

