#!/usr/bin/env python3

import os
import uuid
import deepzoom


def createImg(filePath):
    SOURCE = filePath
    # Create Deep Zoom Image creator with weird parameters
    creator = deepzoom.ImageCreator(
        tile_size=128,
        tile_overlap=2,
        tile_format="png",
        image_quality=0.8,
        resize_filter="bicubic",
    )
    filepath, tmpfilename = os.path.split(filePath)
    newname = uuid.uuid4().hex
    dzi_path = filepath + "/diz/" + newname + ".dzi"
    # Create Deep Zoom image pyramid from source
    creator.create(SOURCE, dzi_path)
    return dzi_path
