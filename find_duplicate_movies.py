'''
ok so another one
once we have the "delete things not symlinked in ~/media" script
we can write a "delete useless symlinks in ~/media" script 
then run that one, followed by the first one

determine uselessness
[4:16 PM]
delete if that
[4:17 PM]
some things that make a symlink useless:
- it refers to a file that doesnt exist anymore
- it is not referred to in the Plex database
- there is another, higher-quality, version of the file already registered in the Plex database
'''
from plexclient import plex


""" Constants """
resolution_map = [ "sd", "480", "576", "720", "1080", "2k", "4k" ]


"""
Utility functions
"""

def pretty_print_media(media, deleting=False):
    for mp in media.parts:
        print(("~" if deleting else "") + f"{media.videoResolution}\t{media.width}x{media.height}  \t{int(sum(p.size for p in media.parts))}\t{m.title}\t\t{mp.file}")

"""
External calling functions
"""

def get_movies():
    movies = []
    for movie_section in ['B Movies', 'Movies']:
        movies += plex.library.section(movie_section).search()
    return movies

"""
Domain functions
"""    

def compare_media(a,b):
    if resolution_map.index(a.videoResolution) > resolution_map.index(b.videoResolution):
        return True
    if sum(p.size for p in a.parts) > sum(p.size for p in b.parts):
        return True
    if a.bitrate > b.bitrate:
        return True
    return False

def get_dupe_movies(movies):
    movies_with_dupes = []
    for m in movies:
        try:
            if len(m.media) > 1:
                movies_with_dupes.append(m)
        except NameError as e:
            print(e)
    return movies_with_dupes


def get_deletable_media(movie):
    max_me = movie.media[0]
    me_to_delete = []
    for me in movie.media[1:]:
        if compare_media(me, max_me):
            max_me = me
        else:
            me_to_delete.append(me)
    return me_to_delete, max_me

"""
Main runner
"""
if __name__ == "__main__":
    movies = get_movies()
    dupe_movies = get_dupe_movies(movies)

    to_delete = []
    for m in dupe_movies:
        deletable, max_me = get_deletable_media(m)
        to_delete += deletable

        pretty_print_media(max_me)
        for mee in deletable:
            pretty_print_media(mee, deleting=True)
        print()

    total_size = 0
    for me in to_delete:
        total_size += sum(p.size for p in me.parts)
    print()
    print(f"total space saved: {int(total_size/1024/1024/1024)} Gb")