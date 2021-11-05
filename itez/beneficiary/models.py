from django.contrib.gis.db import models
from django.db.models.fields.related import create_many_to_many_intermediary_model
from django.utils.translation import gettext_lazy as _

from .utils import generate_uuid_and_agent_code


class Beneficiary(models.Model):
    """
    Implements the Beneficiary properties and required methods.
    """

    GENDER = (
        ("male", _("Male")),
        ("female", _("Female")),
        ("other", _("Other"))
    )

    MARITAL_STATUS = (
        ("single", _("Single")),
        ("married", _("Married")),
        ("seperated", _("Seperated")),
        ("divorced", _("Divorced")),
        ("widowed", _("Widowed")),
    )

    TERTIARY_EDUCATION_QUALIFICATION = (
        ("certificate", _("Certificate")),
        ("diploma", _("Diploma")),
        ("degree", _("Degree")),
        ("masters", _("Masters")),
        ("doctrate", _("Doctrate")),
        ("phd", _("PHD")),
    )

    first_name = models.CharField(
        _("First Name"),
        max_length=200
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=200
    )
    other_name = models.CharField(
        _("Other Name"),
        max_length=200,
        null=True,
        blank=True
    )
    gender = models.CharField(
        _("Gender"),
        max_length=100,
        choices=GENDER,
    )
    profile_photo = models.ImageField(
        upload_to="profile_photo/",
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=200,
        null=True,
        blank=True
    )
    beneficiary_code = models.UUIDField(
        default=generate_uuid_and_agent_code()[0],
        editable=False
    )
    date_of_birth = models.DateField(_("Date of Birth"))
    marital_status = models.CharField(
        _("Marital Status"),
        choices=MARITAL_STATUS,
        max_length=100
    )
    name_of_spouse = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    number_of_children = models.IntegerField(
        null=True,
        blank=True
    )
    number_of_siblings = models.IntegerField(
        null=True,
        blank=True
    )
    parent_details = models.ForeignKey(
        'BeneficiaryParent',
        on_delete=models.PROTECT
    )
    junior_secondary_qualification = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    senior_secondary_qualification = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    tertiary_eduction_qualification = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        choices=TERTIARY_EDUCATION_QUALIFICATION
    )
    created = models.DateTimeField(auto_now_add=True)
    location = models.PointField(
        geography=True,
        blank=True,
        null=True,
        srid=4326
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Beneficiary"
        verbose_name_plural = "Beneficiaries"
        ordering = ["created"]


class BeneficiaryParent(models.Model):
    father_first_name = models.CharField(
        _("Father First Name"),
        max_length=200
    )
    father_last_name = models.CharField(
        _("Father Last Name"),
        max_length=200
    )
    mother_first_name = models.CharField(
        _("Mother First Name"),
        max_length=200
    )
    mother_last_name = models.CharField(
        _("Mother Last Name"),
        max_length=200
    )
    address = models.TextField(
        max_length=300,
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"Beneficiary Parent: {self.father_first_name} {self.father_last_name}"



class Province(models.Model):
    """
    Implements province properties and required methods.
    """

    name = models.CharField(_("Province"), max_length=255)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        ordering = ["-created"]


class District(models.Model):
    """
    Define district properties and corresponding methods.
    """

    name = models.CharField(_("District"), max_length=255)

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    """
    Define service area properties.
    """

    name = models.CharField(_("Service Area"), max_length=200)

    district = models.ForeignKey(District, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkDetail(models.Model):
    """
    Include Work Detail properties.
    """

    gross_pay = models.DecimalField(
        _("Monthly Salary"),
        decimal_places=2,
        max_digits=1000,
        null=False
    )
    company = models.CharField(
        _("Company Name"),
        max_length=200,
        null=False
    )
    insured = models.BooleanField(
        _("Company Insured"),
        default=False
    )
    work_address = models.TextField(
        _("Work Address"),
        null=True,
        blank=True
    )

    def __str__(self):
        return self.company
