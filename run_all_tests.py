#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hk_fashion.settings')

# Setup Django
django.setup()

# Now run the tests
if __name__ == '__main__':
    from django.test.utils import get_runner
    from django.conf import settings

    TestRunner = get_runner(settings, 'django.test.runner.DiscoverRunner')
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(['pages', 'products'])
