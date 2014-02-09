# -*- coding: utf-8 -*-

import cover_grabber
from cover_grabber.os.media_dir_walker import MediaDirWalker


def grab_cover(mediadir, outputdir, overwrite = False):
    media_walker = MediaDirWalker(mediadir, outputdir, overwrite).do_walk_path()