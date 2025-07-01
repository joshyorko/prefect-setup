#!/usr/bin/env python3

# /// script
# dependencies = [
#   "pandas"
# ]
# ///

from typing import Union, Dict, Any, Optional
import requests
from prefect import task, flow
from prefect.logging import get_run_logger
import time



@task(retries=0, log_prints=True)
def run_producer():
    return 

@task(retries=0, log_prints=True)
def run_consumer():
    """Insert consumer logic here"""
    return 

@flow(name="RPA Services Flow", log_prints=True)
def rpa_services_flow():
    """
    Flow that handles both RPA billing report and transcript generation
    """
    logger = get_run_logger()
    
    # Get RPA billing report
    run_producer()
    
    run_consumer()


if __name__ == "__main__":
    rpa_services_flow()
