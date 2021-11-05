from django.contrib.gis import models
from django.db.models.deletion import PROTECT
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
        null=True
    )
    gender = models.CharField(
        _("Gender"),
        max_length=100,
        choices=GENDER
    )
    profile_photo = models.ImageField(
        upload_to="profile_photo/"
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
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Beneficiary"
        verbose_name_plural = "Beneficiaries"
        ordering = ["created"]


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
        on_delete=PROTECT,
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    """
    Define service area properties.
    """

    name = models.CharField(_("Service Area"), max_length=200)

    district = models.ForeignKey(District, on_delete=PROTECT)

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
