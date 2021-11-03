from django.db import models
from django.db.models.deletion import PROTECT
from django.utils.translation import gettext_lazy as _

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
        on_delete=PROTECT
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkDetail(models.Model):
    """
    Include Work Detail properties.
    """
    POSITIVE_CHOICE = "Yes"
    NEGATIVE_CHOICE = "No"
    CHOICE_LIST = [
        (POSITIVE_CHOICE, "Yes"),
        (NEGATIVE_CHOICE, "No")
    ]

    salary = models.IntegerField(
        "Monthly Salary",
        null=False
    )

    company = models.CharField(
        "Company Name", 
        max_length=200, 
        null=False
    )

    insured = models.CharField( 
        "Is your company insured?.", 
        choices = CHOICE_LIST,
        max_length=100, 
        default = POSITIVE_CHOICE
    )

    work_address = models.CharField(
        "Work Address",
        null=False,
        max_length=500
    )

    def __str__(self):
        return self.company
