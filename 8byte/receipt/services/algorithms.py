from typing import List, Dict
from ..models.receipt import Receipt
from django.db.models import Sum, Count
from statistics import mean, median, mode
from collections import defaultdict
import re

def search_receipts(query: str, field: str = 'all', date_range: tuple = None) -> List[Receipt]:
    receipts = Receipt.objects.all()
    
    if field == 'vendor' or field == 'all':
        receipts = receipts.filter(vendor__icontains=query)
    elif field == 'category':
        receipts = receipts.filter(category__icontains=query)
    
    if date_range:
        start_date, end_date = date_range
        receipts = receipts.filter(transaction_date__range=[start_date, end_date])
    
    return list(receipts)

def sort_receipts(receipts: List[Receipt], key: str, reverse: bool = False) -> List[Receipt]:
    def get_key(receipt):
        if key == 'amount':
            return receipt.amount
        elif key == 'date':
            return receipt.transaction_date
        elif key == 'vendor':
            return receipt.vendor.lower()
        return receipt.created_at
    
    return sorted(receipts, key=get_key, reverse=reverse)

def get_aggregates(receipts: List[Receipt]) -> Dict:
    amounts = [float(r.amount) for r in receipts]
    
    vendor_freq = defaultdict(int)
    monthly_spend = defaultdict(float)
    
    for receipt in receipts:
        vendor_freq[receipt.vendor] += 1
        month = receipt.transaction_date.strftime('%Y-%m')
        monthly_spend[month] += float(receipt.amount)
    
    return {
        'total': sum(amounts) if amounts else 0,
        'mean': mean(amounts) if amounts else 0,
        'median': median(amounts) if amounts else 0,
        'mode': mode(amounts) if amounts else 0,
        'vendor_distribution': dict(vendor_freq),
        'monthly_trend': dict(sorted(monthly_spend.items()))
    }
