#  Presentation of the scrapping project

The motivation behind this scrapping project was to build a module that would allows developers to quickly write a scrapper for a specific website using multiprocessing.

Web scrapping multiples urls imply API call latency et I/O operations latency.
Multiprocessing fix those problems by making API call concurrently, same goes for I/O operations

**Multiprocessing eliminates the latency due to sequential API call and I/O operations.**

****The dataset scrapped could then be used to train an image classifier using machine learning techniques..****

The most important file here is `multiprocess_imagescrapper.py`.
It contains the tools for developer to efficently scrap the image of a given list of urls using **multiprocessing**

    def multiprocess_scrap_image_and_save_to_dest(list_of_url_and_dest_folder):

Just give it a list of tuple containing  url to scrap + the destination folder where to save the images.


`imparfaiteparis_scrapper.py` and `devredshop_scrapper.py`
are exemple of how you could use `multiprocess_imagescrapper.py`


Here we are scrapping images from two french clothing e-commerce:
[www.imparfaiteparis.com](https://www.imparfaiteparis.com/) and [www.devred.com](https://www.devred.com/)

![imparfaite_shop](read_me_images/imparfaite_shop.png?raw=true "Imparfaite shop")
![devred_shop](read_me_images/devred_shop.png?raw=true "Devred shop")

#  How to use the scrapping module

## STEP 1 Write some code to generate a list of urls to scrap
use `imparfaiteparis_scrapper.py` and `devredshop_scrapper.py` as examples to create your own scrapper.

Here, to scrap www.devred.com, I wrote `generate_url_and_dest_list_devred()`

    all_urls_to_scraps_and_dest_dir = generate_url_and_dest_list_devred()

## STEP 2 Give the list to multiprocess_scrap_image_and_save_to_dest(list_of_url_and_dest_folder)

    multiprocess_scrap_image_and_save_to_dest(all_urls_to_scraps_and_dest_dir)

## STEP 3 Relax and let the multiprocessing's Worker do their magic.


    19:11:09,216 [MainThread][PoolWorker-17] [INFO] START FETCHING ALL IMAGES URLS FROM HTTPS://WWW.DEVRED.COM/CHAUSSURESACCESSOIRES/?P=1
    19:11:09,217 [MainThread][PoolWorker-18] [INFO] START FETCHING ALL IMAGES URLS FROM HTTPS://WWW.DEVRED.COM/CHAUSSURESACCESSOIRES/?P=2
    19:11:09,221 [MainThread][PoolWorker-19] [INFO] START FETCHING ALL IMAGES URLS FROM HTTPS://WWW.DEVRED.COM/CHAUSSURESACCESSOIRES/?P=3
    19:11:09,224 [MainThread][PoolWorker-20] [INFO] START FETCHING ALL IMAGES URLS FROM HTTPS://WWW.DEVRED.COM/CHAUSSURESACCESSOIRES/?P=4
    19:11:09,228 [MainThread][PoolWorker-21] [INFO] START FETCHING ALL IMAGES URLS FROM HTTPS://WWW.DEVRED.COM/CHAUSSURESACCESSOIRES/?P=5
    19:11:09,564 [MainThread][PoolWorker-5] [INFO] START DOWNLOADING ALL IMAGE FROM HTTPS://WWW.DEVRED.COM/PANTALON/?P=3
    19:11:09,659 [MainThread][PoolWorker-1] [INFO] START DOWNLOADING ALL IMAGE FROM HTTPS://WWW.DEVRED.COM/PULL/?P=2
    19:11:10,169 [MainThread][PoolWorker-21] [INFO] START DOWNLOADING ALL IMAGE FROM HTTPS://WWW.DEVRED.COM/CHAUSSURESACCESSOIRES/?P=5
    19:11:10,198 [MainThread][PoolWorker-5] [INFO]  file DEVRED_AH18_Web-Soldes-EMS.png already exists, skip download





## Installation

- All the `code` required to get started
- Images of what it should look like

### Clone

- Clone this repo to your local machine using `https://github.com/ne-il/multiprocessing_image_scraper`

### Setup


Install the dependencies:
```shell
$ pip install requirement.txt
```

Try the two scrappers:
```shell
$ python imparfaiteparis_scrapper.py
$ python devredshop_scrapper.py
```

The images will be saved in `./scrapped_images/`
## Authors

* [**Neil Anteur**](https://www.linkedin.com/in/neil-anteur-a29683138/) - *Initial work* -  [ne-il](https://github.com/ne-il)




