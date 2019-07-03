"""

This code scrap images from https://imparfaiteparis.com using the multiprocess scrapping module.

It scrap all the image from the clothing category specified in config.py. (the clothing category from imparfaiteparis are in French)

"""

from lxml import html
from config import CATEGORY_LIST_IMPARFAITE, IMPARFAITE_URL
from multiprocess_imagescrapper import multiprocess_scrap_image_and_save_to_dest
import logging
import requests

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
    xpath_list = '//*[@id="main"]/nav/ul'

    container = tree.xpath(xpath_list)
    if container:
        ul_element = container[0]
        target_li = ul_element[-2]
        target_a = target_li[0]
        number_of_page = int(target_a.text)
        return number_of_page
    else:
        logger.error("can't find last page number element with xpath".upper())
        return 1


def generate_url_and_dest_list_for_one_category_imparfaite(category):
    """

        Step 1: find the number of pages for the specified category (using xpath scrapping)
        Step 2: Generate the list of url

        The list of url should look like this:
            [('https://www.imparfaiteparis.com/product-category/vetements/skirts/1/?orderby=date', imparfaite/skirts)
            ('https://www.imparfaiteparis.com/product-category/vetements/skirts/2/?orderby=date', imparfaite/skirts)
                                                ....
            ('https://www.imparfaiteparis.com/product-category/vetements/skirts/18/?orderby=date', imparfaite/skirts)]

        :param str category: the name of the category e.g 'robe', 'tops', 'pantalon'
        :return: a list of tuple (url, dest_dir) containg urls to scrap for the specified clothing category and the dest directory where to save the images
        :rtype list
    """
    # type: str -> list

    logger.info("Start to construct all urls for the category \'{}\'".format(category).upper())

    category_url = "{}{}".format(IMPARFAITE_URL, category)
    number_of_page = scrap_last_page_index_for_one_category(category_url)

    dest_dir = 'scrapped_images/imparfaite/{}'.format(category)

    # using map and lambda, it generates a list of all page url for the specified clothing category with the destination directory
    all_urls_for_this_category_with_dest_dir = list(
        map(
            lambda i: ("{}/{}{}{}".format(category_url, '/page/', str(i), '/?orderby=date'), dest_dir)
            , range(1, number_of_page + 1)
        )
    )
    return all_urls_for_this_category_with_dest_dir


def generate_url_and_dest_list_imparfaite():
    """ return the list of every imparfaite website url to scrap and

        imparfaite website is divided into 10 clothing category, we want to scrap every image from every category

    :return: a list of tuple (url, dest_dir) containg urls to scrap and the dest directories where to save the images
    """
    # type: () -> list
    all_url_to_scraps = []
    for category_imparfaite in CATEGORY_LIST_IMPARFAITE:
        all_urls_for_this_category = generate_url_and_dest_list_for_one_category_imparfaite(category_imparfaite)
        all_url_to_scraps.extend(all_urls_for_this_category)
    return all_url_to_scraps


def main():
    """
        Step 1: Generate the list containing every url to scrap and directories paths to save the images
        Step 2: Feed the list to the scrapping Workers using the multiprocessing scrapper module
    """
    all_urls_to_scraps_and_dest_dir = generate_url_and_dest_list_imparfaite()
    multiprocess_scrap_image_and_save_to_dest(all_urls_to_scraps_and_dest_dir)


if __name__ == "__main__":
    main()

