from glob import glob
from io import TextIOWrapper
from json import JSONDecoder
from os.path import basename, dirname
from zipfile import ZipFile


class Oshiri(ZipFile):

    def __init__(self, *args, text='en_US'):

        super().__init__(*args)

        # From: [{'0.png': [{'x': 10, ...}, {'x': 12, ...}], {'2.png': [{'x': 3, ...}, ...]}]
        # To:   [{'image': '0.png', 'contents': [{'x': 10, ...}, {'x': 12, ...}]}, {'image': '2.png', 'contents': [{'x': 3, ...}, ...]}]
        # We are starting from a list of one-item dictionaries, so
        # doing a popitem() returns their only value in a (key, item) tuple,
        # from which we generate a new, more usable list of dictionaries:
        self.index = [{'image': image, 'contents': contents} for image, contents in [item.popitem() for item in JSONDecoder().decode(TextIOWrapper(self.open('texts/' + text + '.json')).read())['index']]]

        # Dictionary with the styles files (copied in their entirety) used by the index file:
        styles = {dirname(item['style']): JSONDecoder().decode(TextIOWrapper(self.open('styles/' + dirname(item['style']) + '.json')).read()) for page in self.index for item in page['contents']}

        # Replace the "style" index for every item in the index list with
        # a reference to the actual style:
        for page in self.index:
            for item in page['contents']:
                item['style'] = styles[dirname(item['style'])][basename(item['style'])]


    def getFonts(self):

        for font in (font for font in self.namelist() if dirname(font) == 'fonts' and font != 'fonts/'):
            yield self.open(font).read()


    def getImage(self, page):

        return self.open('images/' + page).read()
