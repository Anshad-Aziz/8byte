from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from receipt.models.receipt import Receipt
from receipt.services.data_ingestion import ingest_file
from receipt.services.algorithms import search_receipts, sort_receipts, get_aggregates
import csv
from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)

def upload_receipt(request):
    if request.method == 'POST':
        try:
            if 'file' not in request.FILES:
                logger.error("No file provided in request")
                return render(request, 'receipt_list.html', {'error': 'No file selected'})
            
            file = request.FILES['file']
            logger.info(f"Processing file: {file.name}")
            receipt = ingest_file(file)
            logger.info(f"Successfully saved receipt: {receipt.id}")
            return redirect('receipt_list')
        except Exception as e:
            logger.error(f"Error in upload_receipt: {str(e)}", exc_info=True)
            return render(request, 'receipt_list.html', {'error': f"Error processing file: {str(e)}"})
    return render(request, 'receipt_list.html')

def receipt_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'date')
    receipts = search_receipts(query)
    receipts = sort_receipts(receipts, sort_by)
    aggregates = get_aggregates(receipts)
    
    return render(request, 'receipt_list.html', {
        'receipts': receipts,
        'aggregates': aggregates
    })

def edit_receipt(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    if request.method == 'POST':
        try:
            receipt.vendor = request.POST.get('vendor', receipt.vendor)
            receipt.amount = request.POST.get('amount', receipt.amount)
            receipt.transaction_date = datetime.strptime(
                request.POST.get('transaction_date'), '%Y-%m-%d'
            ).date()
            receipt.category = request.POST.get('category', receipt.category)
            receipt.save()
            logger.info(f"Updated receipt: {receipt.id}")
            return redirect('receipt_list')
        except Exception as e:
            logger.error(f"Error updating receipt {pk}: {str(e)}")
            return render(request, 'receipt_edit.html', {'receipt': receipt, 'error': str(e)})
    return render(request, 'receipt_edit.html', {'receipt': receipt})

def export_csv(request):
    receipts = Receipt.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="receipts.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Vendor', 'Date', 'Amount', 'Category'])
    for receipt in receipts:
        writer.writerow([
            receipt.vendor,
            receipt.transaction_date,
            receipt.amount,
            receipt.category
        ])
    return response