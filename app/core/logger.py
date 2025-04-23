import logging
from logging import Logger


logging.basicConfig(
    level=logging.INFO,  # Can be DEBUG/INFO/WARNING/ERROR/CRITICAL
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("app") 

# logger.info("App started!")
# logger.warning("Disk space running low.")
# logger.error("Something failed", exc_info=True)