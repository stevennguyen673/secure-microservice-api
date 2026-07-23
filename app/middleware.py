import time
import logging

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("fastapi-service")


# middleware function
async def logging_middleware(request, call_next):
    # get req info
    method = request.method
    path = request.url.path
    start_time = time.time()
    
    try:

        # pass request to FastAPI route
        response = await call_next(request)

        # get response info
        status_code = response.status_code
        end_time = time.time()
        duration = int((end_time - start_time) * 1000) # milliseconds
        
        # determine severity
        if status_code < 400:
            severity = logging.INFO
        elif status_code < 500:
            severity = logging.WARNING
        else:
            severity = logging.ERROR


        # write log
        logger.log(severity, f"method: {method} \npath: {path} \nstatus_code: {status_code} \nduration: {duration}ms")

        return response


    except Exception as error:

        # get exception info
        exception = type(error).__name__
        err_msg = str(error)
        end_time = time.time()
        duration = int((end_time - start_time) * 1000)

        logger.log(logging.ERROR, f"method: {method} \npath: {path} \nexception: {exception} \nmessage: {err_msg} \nduration: {duration}ms")
        
        raise