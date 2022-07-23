import os
import logging
import datetime
import time
import requests
import optparse
import settings

from gmaps import GmapAPI

logger = logging.getLogger(__name__)


URL = 'https://www.rocadebordeaux.com/rocade.png'
PLACE_ID_EMILE_COUNORD = 'ChIJD9w0JnAoVQ0RG9b6vJKDFgQ'
PLACE_ID_LACANAU_OCEAN = 'ChIJRTaiWMX_AUgRaTXw4dRDK8A'


def download_and_save(url, filename):
    r = requests.get(url)
    if r.status_code != 200:
        raise RuntimeError('Error get')
    content = r.content
    with open(filename, 'wb') as f:
        f.write(content)


def direction_store(filename, trajets):
    gmap = GmapAPI(settings.API_KEY)
    durations = [
        str(gmap.get_duration('place_id:'+origin, 'place_id:'+destination))
        for origin, destination in trajets
    ]
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    with open(filename, 'a') as f:
        f.write('\t'.join([now_str, *durations]) + '\n')


def work():
    logger.info('Work')
    now = datetime.datetime.now()
    folder_path = now.strftime('data/%Y/%m')
    os.makedirs(folder_path, exist_ok=True)
    filename = now.strftime('%Y%m%d-%H%M%S-%A-rocade.png')
    filepath = os.path.join(folder_path, filename)
    download_and_save(URL, filepath)
    direction_store(os.path.join(folder_path, 'durations.csv'), (
        (PLACE_ID_EMILE_COUNORD, PLACE_ID_LACANAU_OCEAN),
        (PLACE_ID_LACANAU_OCEAN, PLACE_ID_EMILE_COUNORD),
    ))


def main(delay):
    while True:
        try:
            work()
        except Exception:
            logger.exception('Error during processing')
        time.sleep(delay)


if __name__ == '__main__':
    FORMAT = "%(asctime)-15s %(name)s %(levelname)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    parser = optparse.OptionParser()
    parser.add_option('-d', '--delay', dest='delay', type='int',
                      default=15 * 60, help='delay in seconds')
    (options, args) = parser.parse_args()
    try:
        main(options.delay)
    except KeyboardInterrupt:
        print('Exit...')
