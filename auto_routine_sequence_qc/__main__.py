#!/usr/bin/env python

import argparse
import datetime
import json
import logging
import os
import time

import auto_routine_sequence_qc.config
import auto_routine_sequence_qc.core as core
from auto_routine_sequence_qc.logging_config import configure_logging

DEFAULT_SCAN_INTERVAL_SECONDS = 3600.0

log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    parser.add_argument('--log-level')
    args = parser.parse_args()

    configure_logging(args.log_level)

    config = {}

    log.debug({"event_type": "debug_logging_enabled"})

    quit_when_safe = False

    while(True):
        try:
            if args.config:
                try:
                    config = auto_routine_sequence_qc.config.load_config(args.config)
                    log.info({"event_type": "config_loaded", "config_file": os.path.abspath(args.config)})
                except json.decoder.JSONDecodeError as e:
                    # If we fail to load the config file, we continue on with the
                    # last valid config that was loaded.
                    log.error({"event_type": "load_config_failed", "config_file": os.path.abspath(args.config)})

            scan_start_timestamp = datetime.datetime.now()
            for run in core.scan(config):
                if quit_when_safe:
                    exit(0)
                if run is not None:
                    try:
                        config = auto_routine_sequence_qc.config.load_config(args.config)
                        log.info({"event_type": "config_loaded", "config_file": os.path.abspath(args.config)})
                    except json.decoder.JSONDecodeError as e:
                        log.error({"event_type": "load_config_failed", "config_file": os.path.abspath(args.config)})
                    core.analyze_run(config, run)
            scan_complete_timestamp = datetime.datetime.now()
            scan_duration_delta = scan_complete_timestamp - scan_start_timestamp
            scan_duration_seconds = scan_duration_delta.total_seconds()
            log.info({"event_type": "scan_complete", "scan_duration_seconds": scan_duration_seconds})

            if quit_when_safe:
                exit(0)

            scan_interval = DEFAULT_SCAN_INTERVAL_SECONDS
            if "scan_interval_seconds" in config:
                try:
                    scan_interval = float(str(config['scan_interval_seconds']))
                except ValueError as e:
                    scan_interval = DEFAULT_SCAN_INTERVAL_SECONDS
            time.sleep(scan_interval)
        except KeyboardInterrupt as e:
            log.info({"event_type": "quit_when_safe_enabled"})
            quit_when_safe = True

if __name__ == '__main__':
    main()
