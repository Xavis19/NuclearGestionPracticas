"""
Custom exception handler para la app.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler que proporciona respuestas más detalladas.
    """
    # Llamar al exception handler por defecto de DRF
    response = exception_handler(exc, context)
    
    if response is not None:
        # Personalizar el formato de error
        custom_response_data = {
            'error': True,
            'message': None,
            'details': response.data
        }
        
        # Extraer mensaje principal
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['message'] = response.data['detail']
            elif 'non_field_errors' in response.data:
                custom_response_data['message'] = response.data['non_field_errors'][0]
            else:
                # Tomar el primer error
                first_key = list(response.data.keys())[0]
                if isinstance(response.data[first_key], list):
                    custom_response_data['message'] = response.data[first_key][0]
                else:
                    custom_response_data['message'] = response.data[first_key]
        elif isinstance(response.data, list):
            custom_response_data['message'] = response.data[0]
        else:
            custom_response_data['message'] = str(response.data)
        
        response.data = custom_response_data
    
    return response
