from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
logger.info("Rate limiter initialized")