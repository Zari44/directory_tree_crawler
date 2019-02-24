import urllib
import os

comicCounter=len(os.listdir('/home/mzarudzki/Downloads/images'))+1  # reads the number of files in the folder to start downloading at the next comic
errorCount=0

def download_image(url, comicName):
    """
    download a comic in the form of

    url = http://www.example.com
    comicName = '00000000.jpg'
    """
    image=urllib.URLopener()
    image.retrieve(url,comicName)  # download comicName at URL

if __name__ == "__main__":
    os.chdir('/home/mzarudzki/Downloads/images')  # set where files download to
    try:
        url = "https://media.glamour.com/photos/5978ff1b998c9d5afe0b6050/16:9/w_1280%2Cc_limit/dakota-johnson-beauty-lede.jpg"
        download_image(url, "image")  # uses the function defined above to download the comic
        print url
    except IOError:  # urllib raises an IOError for a 404 error, when the comic doesn't exist
        print str("image does not exist")  # otherwise say that the certain comic number doesn't exist
    print "finished downloading"