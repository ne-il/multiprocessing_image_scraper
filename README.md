#  Presentation of the scrapping project

The motivation behind this scrapping project was to be able to scrap clothing image rapidly from any website.

The dataset scrapped could then be used to train an image classifier using machine learning techniques..

The most important file here is `multiprocess_imagescrapper.py`.
It contains the tools for developer to efficently scrap the image of a given list of urls using **multiprocessing**

Just give it a list of tuple containing  url to scrap + the destination folder where to save the images.


`imparfaiteparis_scrapper.py` and `devredshop_scrapper.py`
are exemple of how you could use `multiprocess_imagescrapper.py`


Here we are scrapping images from two french clothing e-commerce:
[www.imparfaiteparis.com](https://www.imparfaiteparis.com/)
![imparfaite_shop](read_me_images/imparfaite_shop.png?raw=true "Imparfaite shop")


and [www.devred.com](https://www.devred.com/)
![devred_shop](read_me_images/devred_shop.png?raw=true "Devred shop")


