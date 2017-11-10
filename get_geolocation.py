#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys

from PIL import Image
from PIL.ExifTags import TAGS


def findPhotos(baseDir):
    matches = []
    for root, dirnames, filenames in os.walk(baseDir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.JPG' or \
                os.path.splitext(filename)[1] == '.jpg':
                matches.append(os.path.join(root, filename))
    return matches


def get_exif(fn):
    ret = {}
    try:
        i = Image.open(fn)
        info = i._getexif()
        if info is not None:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
            return ret
    except IOError:
        return None


def get_geolocation(path):
    fotos = findPhotos(path)

    for foto in fotos:
        a = get_exif(foto)
        if a is not None:
            lat = [float(x) / float(y) for x, y in a['GPSInfo'][2]]
            latref = a['GPSInfo'][1]
            lon = [float(x) / float(y) for x, y in a['GPSInfo'][4]]
            lonref = a['GPSInfo'][3]

            lat = lat[0] + lat[1] / 60 + lat[2] / 3600
            lon = lon[0] + lon[1] / 60 + lon[2] / 3600

            if latref == 'S':
                lat = -lat
            if lonref == 'W':
                lon = -lon

            print "%s, %s, %s" % (os.path.basename(foto), lat, lon)


if (len(sys.argv) < 2):
    print """
    Script para crear csv con las coordenadas de las fotos de entrada
    Uso: get_geolocation.py directorio_para_buscar_imagenes > coor.csv
    """
    sys.exit(2)
else:
    baseDir = sys.argv[1]
    get_geolocation(baseDir)