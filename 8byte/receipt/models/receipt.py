from django.db import models
from pydantic import BaseModel, validator
from datetime import date
import re

class Receipt(models.Model):
    vendor = models.CharField(max_length=100)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, blank=True)
    file_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['vendor']),
            models.Index(fields=['transaction_date']),
            models.Index(fields=['category']),
        ]

class ReceiptSchema(BaseModel):
    vendor: str
    transaction_date: date
    amount: float
    category: str | None
    file_name: str

    @validator('vendor')
    def validate_vendor(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Vendor name must be at least 2 characters')
        return v.strip()

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v

    @validator('file_name')
    def validate_file_name(cls, v):
        if not re.match(r'.*\.(jpg|png|pdf|txt)$', v, re.IGNORECASE):
            raise ValueError('Invalid file format')
        return v