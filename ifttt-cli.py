#!/usr/bin/env python
import sys
import os
import json
import argparse
import urllib2
import logging as log

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='show verbose messages')
    parser.add_argument('-d', '--debug', action='store_true', help='show debug messages')
    parser.add_argument('-k', '--key', required='IFTTT_KEY' not in os.environ, default=os.environ.get('IFTTT_KEY', None), help='Your IFTTT Maker channel key. Can be set as environment variable IFTTT_KEY')
    parser.add_argument('-e', '--event', default='ifttt-cli', help='IFTTT event name (default: ifttt-cli)')
    parser.add_argument('value1', nargs='?')
    parser.add_argument('value2', nargs='?')
    parser.add_argument('value3', nargs='?')
    args = parser.parse_args()

    if args.debug:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output")
    elif args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
        log.info("Verbose output")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    url = 'https://maker.ifttt.com/trigger/%s/with/key/%s' % (args.event, args.key)
    data = {'value'+str(i): vars(args)['value'+str(i)] for i in range(1,4) if vars(args)['value'+str(i)] is not None}
    headers = {'Content-Type': 'application/json'}

    log.info('Preparing Requests')
    log.debug('URL: ' + url)
    log.debug('Data: ' + str(data))
    log.debug('Headers: ' + str(headers))
    req = urllib2.Request(url, json.dumps(data), headers)
    log.info('Opening URL')
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        log.error('HTTPError = ' + str(e.code))
        sys.exit(3)
    except urllib2.URLError, e:
        log.error('URLError = ' + str(e.reason))
        sys.exit(4)
    except httplib.HTTPException, e:
        log.error('HTTPException')
        sys.exit(5)
    except Exception:
        import traceback
        log.error('generic exception: ' + traceback.format_exc())
        sys.exit(6)
    content = response.read()
    log.info(content)
