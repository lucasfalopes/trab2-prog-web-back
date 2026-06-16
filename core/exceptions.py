from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {'error': 'Erro interno no servidor.', 'detail': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    error_map = {
        400: 'Requisição inválida.',
        401: 'Autenticação necessária.',
        403: 'Você não tem permissão para realizar esta ação.',
        404: 'Recurso não encontrado.',
        405: 'Método não permitido.',
    }

    default_message = error_map.get(response.status_code, 'Erro na requisição.')

    # DRF already puts detail/field errors in response.data — normalize to our format
    original_data = response.data

    if isinstance(original_data, dict) and 'detail' in original_data:
        # Standard DRF single-message error
        normalized = {
            'error': default_message,
            'detail': str(original_data['detail']),
        }
    elif isinstance(original_data, dict):
        # Field validation errors — keep them under 'fields' for the frontend
        normalized = {
            'error': default_message,
            'detail': 'Verifique os campos enviados.',
            'fields': original_data,
        }
    elif isinstance(original_data, list):
        normalized = {
            'error': default_message,
            'detail': original_data[0] if original_data else default_message,
        }
    else:
        normalized = {
            'error': default_message,
            'detail': str(original_data),
        }

    response.data = normalized
    return response
