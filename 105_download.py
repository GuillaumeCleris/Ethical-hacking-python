#!/usr/bin/env python
import requests


def download(url):
    # download file from the url
    get_response = requests.get(url)
    # print(get_response.content)

    # on split l'url en list par les / et on recupère le dernier élément
    file_name = url.split("/")[-1]

    # writing on disk
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


download("https://www.carmagazine.co.uk/Images/PageFiles/69400/GTRNismo_13.jpg")
