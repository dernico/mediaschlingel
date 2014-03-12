# -*- coding: utf-8 -*-
try:
    import cover_grabber
    from cover_grabber.os.media_dir_walker import MediaDirWalker
except:
    print "Could not load Cover Grabber. Pls install from libs folder"

def grab_cover(mediadir, outputdir, overwrite = False):
    media_walker = MediaDirWalker(mediadir, outputdir, overwrite).do_walk_path()