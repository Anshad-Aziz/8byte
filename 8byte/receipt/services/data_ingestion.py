import os
import logging
from typing import List
from .data_parsing import parse_file
from receipt.models.receipt import Receipt, ReceiptSchema
from django.core.files.storage import default_storage
from pydantic import ValidationError

# Set up logging
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'.jpg', '.png', '.pdf', '.txt'}

def ingest_file(file) -> Receipt:
    try:
        # Validate file extension
        file_ext = os.path.splitext(file.name)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            logger.error(f"Unsupported file type: {file_ext}")
            raise ValueError(f"Unsupported file type: {file_ext}")

        # Ensure uploads directory exists
        uploads_dir = os.path.join('media', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)

        # Save file
        relative_file_path = default_storage.save(f'uploads/{file.name}', file)
        full_file_path = os.path.join('media', relative_file_path)
        logger.info(f"File saved to: {full_file_path}")

        # Verify file exists
        if not os.path.exists(full_file_path):
            logger.error(f"File not found at: {full_file_path}")
            raise FileNotFoundError(f"File not found at: {full_file_path}")

        # Parse file content
        parsed_data = parse_file(full_file_path)
        logger.info(f"Parsed data: {parsed_data}")
        
        # Validate with Pydantic
        schema = ReceiptSchema(**parsed_data)
        
        # Save to database
        receipt = Receipt.objects.create(
            vendor=schema.vendor,
            transaction_date=schema.transaction_date,
            amount=schema.amount,
            category=schema.category or 'Uncategorized',
            file_name=full_file_path
        )
        logger.info(f"Receipt saved to database: {receipt.id}")
        return receipt

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise ValueError(f"Validation error: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing file {file.name}: {str(e)}", exc_info=True)
        raise Exception(f"Error processing file: {str(e)}")