# -*- coding: utf-8 -*-

__author__ = 'Tyler Lubeck'
__email__ = 'tyler@tylerlubeck.com'
__version__ = '0.1.0'

# Lifted from here:
# http://docs.python-guide.org/en/latest/writing/logging/#logging-in-a-library
# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
