"""
This module allows the user to scrap every image from a list of url using multiprocessing.

The main motivation for using multiprocessing are:
    - Scrapping data from website involve a lot of HTTP request which
are very execution time consuming if done sequentially.
    - Delegating heavy file I/O operation to worker process
improve dramatically performance.

Each function can be imported individually but the entry point of the module should be
multiprocess_scrap_image_and_save_to_dest (list_of_url_and_dest_folder). It's from this function that the Pool of
worker are setup and launched


"""

import os
import re
import requests
import logging
import errno
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s][%(processName)s] [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
MAX_PROCESS = 300


def get_all_image_urls_from_one_page(web_page_url):
    """ return all images's url for a given website url

    The parsing of the html page is done with BeautifulSoup. We get all the url by looking for the src attribute of every
    <img> tag if the html page specified as a parameter.

    :param str web_page_url: l'url de la page dont on veut recupere toutes les urls d'image

    :return: the list of all the image url of the page
    """
    logger.info("START fetching all images urls from {}".format(web_page_url).upper())
    response = requests.get(web_page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        # it's a list of Tag object from BeautifulSoup
        if img_tags:
            return [img.get('src') for img in img_tags]
    else:
        logger.debug("response code {} from {}".format(response.status_code, web_page_url).upper())


def download_and_write_from_urls(dest_dir, web_page_url, images_urls):
    """ download and save in dest_dir every image reachable by urls found in images_urls

    :param str dest_dir: the path of the directory where all downloaded image should be saved
    :param str web_page_url: the url of the page we are scrapping
    :param list images_urls: the url of every image we want to download
    """

    logger.info("start downloading all image from {}".format(web_page_url).upper())
    for img_url in images_urls:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', img_url)
        if filename:
            filename = filename.group(1)
            filepath = '{}/{}'.format(dest_dir, filename)

            # if the image file is already there, we continue to the next image url
            if os.path.exists(filepath):
                logger.info(" file {} already exists, skip download".format(filename))
                continue

            # if the destination directory does not exist, we create it
            if not os.path.exists(dest_dir):
                try:
                    os.makedirs(dest_dir)
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            with open(filepath, 'wb') as f:
                if 'http' not in img_url:
                    img_url = '{}{}'.format(web_page_url, img_url)
                response = requests.get(img_url)
                if response.status_code == 200:
                    f.write(response.content)
                else:
                    logger.debug("status code {} when trying to download {}".format(response.status_code, img_url))
    logger.info("finish downloading all images from {}".format(web_page_url).upper())


def scrap_url_and_write_to_dest_dir(url_to_scrap_and_dest_folder):
    """ Worker function used for multiprocessing.

    Forced to take one argument to fit the Pool.map() one argument worker function constraint

    Step 1: Get a list containing the url of every image present in the url
    Step 2: Downloading and saving every image from the url list

    :param tuple (str,str) url_to_scrap_and_dest_folder: tuple containing the url to scrap image from and the dest folder where to save the images
    """
    url_to_scrap = url_to_scrap_and_dest_folder[0]
    dest_folder = url_to_scrap_and_dest_folder[1]

    all_image_urls = get_all_image_urls_from_one_page(url_to_scrap)
    download_and_write_from_urls(dest_folder, url_to_scrap, all_image_urls)


def multiprocess_scrap_image_and_save_to_dest(list_of_url_and_dest_folder):
    """ Using multiprocessing, this function scraps every image from a list of url and save them in the local destination directory

    Multiprocessing brings a huge improvement in term of execution time for scrapping process.
    The main reason being multiprocessing eliminates the latency due to sequential API call and I/O operations.

    We create as many workers as url to scrap to launch API calls and system I/O operation concurrently. The number of workers is maxed by
    MAX_PROCESS (300 by default) to avoid taking to much system memory

    :param list [tuple (str, str)] list_of_url_and_dest_folder: list of tuple containing an url to scrap and the
    destination folder where to save the scrapped images
    """
    t1 = time.time()
    number_of_process_to_create = min(len(list_of_url_and_dest_folder), MAX_PROCESS)
    if list_of_url_and_dest_folder:
        p = Pool(1)
        p.map(scrap_url_and_write_to_dest_dir, list_of_url_and_dest_folder)
        p.terminate()
        p.join()

        elapsed_time = time.time() - t1
        logger.info("it took {:0.2f}s with {} workers".format(elapsed_time, number_of_process_to_create))
    else:
        logger.error("the list of url is empty")
