from rest_framework.views import exception_handler


import logging
logger = logging.getLogger(__name__)


def DEFAULT_400_ERROR_EXCEPTION(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        customized_response = {}
        customized_response['errors'] = []

        for key, value in response.data.items():
            error = {'field': key, 'message': value}
            customized_response['errors'].append(error)
            
        response.data['status'] = response.status_code
        # response.data['detail'] = customized_response
        logger.error("{}".format(response.data))
        
        logger.error(" -- SOMETHING WRONG -- ")
    return response
