# -*- coding: utf-8 -*-
"""Allow running Test with AI via ``python -m test_with_ai``."""
from .cli.main import cli

if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
