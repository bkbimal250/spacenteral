"""
File upload validators for document security
"""
import os
from django.core.exceptions import ValidationError


# Allowed file extensions
ALLOWED_EXTENSIONS = [
    # Documents
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    # Images
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg',
    # Text
    '.txt', '.csv',
]

# Allowed MIME types
ALLOWED_MIME_TYPES = [
    # Documents
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    # Images
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'image/svg+xml',
    # Text
    'text/plain',
    'text/csv',
]

# Maximum file size: 30MB
MAX_FILE_SIZE = 30 * 1024 * 1024  # 30MB in bytes


def validate_file_extension(value):
    """
    Validate that the uploaded file has an allowed extension
    """
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f'Unsupported file extension: {ext}. '
            f'Allowed extensions are: {", ".join(ALLOWED_EXTENSIONS)}'
        )


def validate_file_size(value):
    """
    Validate that the uploaded file size is within limits
    """
    if value.size > MAX_FILE_SIZE:
        size_mb = value.size / (1024 * 1024)
        max_size_mb = MAX_FILE_SIZE / (1024 * 1024)
        raise ValidationError(
            f'File size ({size_mb:.1f}MB) exceeds maximum allowed size of {max_size_mb:.0f}MB.'
        )


def validate_file_content(value):
    """
    Validate file MIME type for additional security
    """
    # Get the file's content type
    if hasattr(value, 'content_type') and value.content_type:
        if value.content_type not in ALLOWED_MIME_TYPES:
            raise ValidationError(
                f'Unsupported file type: {value.content_type}. '
                f'Please upload a valid document or image file.'
            )


def validate_document_file(value):
    """
    Combined validator for document files
    """
    validate_file_extension(value)
    validate_file_size(value)
    validate_file_content(value)

