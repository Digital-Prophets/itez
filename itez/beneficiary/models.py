from django.db import models
from django.db.models.deletion import PROTECT 
from django.utils.translation import gettext_lazy as _
from .utils import generate_uuid_and_agent_code
from config.settings.roles import FieldPersonnel


class Province(models.Model):
    """
    Implements province properties and required methods.
    """
    name = models.CharField(
        _("Province"),
        max_length=255 
    )

    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        ordering = ['-created']
    

class District(models.Model):
    """
    Define district properties and corresponding methods.
    """
    
    name = models.CharField(
        _('District'),
        max_length=255
    )

    province = models.ForeignKey(
        Province,
        on_delete=PROTECT,
    )

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
        default = False
    )
    work_address = models.TextField(
        _("Work Address"),
        null=True,
        blank=True
    )

    def __str__(self):
        return self.company


class AgentDetail(models.Model):
    """
    create agent detail table with its instances/columns.
    """
    MALE        =  1
    FEMALE      =  2
    TRANSGENDER =  3
    OTHER       =  4
    GENDER_TYPES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (TRANSGENDER, "Transgender"),
        (OTHER, "Other")
    )
    role = models.ForeignKey(
        FieldPersonnel,
        on_delete=models.CASCADE
    )
    first_name = models.CharField(
        _("First Name"),
        max_length=200,
        null=False
    )
    second_name = models.CharField(
        _("Second Name"),
        max_length=200,
        null=False
    )
    birthdate = models.DateField(
        _("Birth Date"),
        auto_now_add=False,
        null=False
    )
    agend_id = models.TextField(
        _("Agent Id"),
        null=False,
        default=generate_uuid_and_agent_code()[1],
        max_length=100
    )
    gender = models.CharField(
        _("Gender"),
        max_length=200,
        choices=GENDER_TYPES,
        default="Other"
    )
    assigned_location = models.CharField(
        _("Assigned Location"),
        null=False,
        max_length=500
    )

    def __str__(self):
        return "%s %s" %(self.first_name, self.second_name)
