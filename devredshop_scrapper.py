"""

Some code to use the multiprocess scrapping library

"""

import requests
from lxml import html
from config import *
from multiprocess_imagescrapper import multiprocess_scrap_image_and_save_to_dest
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def scrap_last_page_index_for_one_category(category_url):
    # type: (str) -> int
    """ Return the index of the  ast page for a specified clothing category

    The function use xpath to get the index of the last page so, the number of page for a given category.

    :param str category_url:
    :return:
    """
    page = requests.get(category_url)
    tree = html.fromstring(page.content)

    container = tree.xpath("//div[contains(@class, 'pages')]")
    if container:
        div_element = container[0]
        target_ol = div_element[1]
        target_li = target_ol[-2]
        target_a = target_li[0]
        number_of_page = int(target_a.text)
        return number_of_page
    else:
        logger.error("can't find last page number element with xpath".upper())
        return -1

def generate_url_and_dest_list_for_one_category_devred(category_clothing):
    """ return the list of every imparfaite website url to scrap and

        imparfaite website is divided into 10 clothing category, we want to scrap every image from every category

    :return: a list of tuple (url, dest_dir) containg urls to scrap and the dest directories where to save the images
    """
    # type: () -> list
    category_url = '{}{}/'.format(DEVRED_URL,category_clothing)

    number_of_page = scrap_last_page_index_for_one_category(category_url)

    dest_dir = "scrapped_images/devred/{}".format(category_clothing)

    # using map and lambda, it generates a list of all page url for the specified clothing category with the destination directory
    all_urls_for_this_category = list(
        map(
            lambda i: ("{}{}{}".format(category_url, '?p=', str(i)), dest_dir), range(1, number_of_page + 1)
        )
    )

    return all_urls_for_this_category


def generate_url_and_dest_list_devred():
    """ return the list of every imparfaite website url to scrap and

        imparfaite website is divided into 10 clothing category, we want to scrap every image from every category

    :return: a list of tuple (url, dest_dir) containg urls to scrap and the dest directories where to save the images
    """
    # type: () -> list
    all_url_to_scraps = []
    for category_imparfaite in CATEGORY_LIST_DEVRED:
        all_urls_for_this_category = generate_url_and_dest_list_for_one_category_devred(category_imparfaite)
        all_url_to_scraps.extend(all_urls_for_this_category)
    return all_url_to_scraps

def main():
    """


        Step 1: Generate the list containing every url to scrap and directories path to save the images
        Step 2: Feed the list to the scrapping Workers using the multiprocessing scrapper module
    """

    all_urls_to_scraps_and_dest_dir = generate_url_and_dest_list_devred()
    multiprocess_scrap_image_and_save_to_dest(all_urls_to_scraps_and_dest_dir)

if __name__ == "__main__":
    main()
