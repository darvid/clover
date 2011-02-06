"""
    clover
    ~~~~~~

    A simplistic COLOURlovers interface.

    :copyright: Copyright 2010 David 'dav' Gidwani
    :license: BSD, see LICENSE.
"""
import datetime
import json
import urllib
import urllib2

from commons.core.graphics.color import Color, Palette


__version__ = "0.0.1"


def url_join(*parts):
    return reduce(lambda a,b: a.rstrip("/") + "/" + b, map(str, parts))


class ColourLovers(object):
    """Baseclass for objects that use the COLOURlovers API."""

    _DATETIME_FMT = "%Y-%m-%d %H:%M:%S"
    _COMMON_SLOTS = [
        "id",
        "title",
        "userName",
        "numViews",
        "numVotes",
        "numComments",
        "numHearts",
        "rank",
        "dateCreated",
        "description",
        "url",
        "imageUrl",
        "badgeUrl",
        "apiUrl"
    ]
    API_URL = "http://colourlovers.com/api/"
    DEFAULT_OPTIONS = {
        "format": "json"
    }

    @classmethod
    def make_request(cls, *path, **options):
        options.update(cls.DEFAULT_OPTIONS)
        url = url_join(
            cls.API_URL,
            url_join(*path),
            "?" + urllib.urlencode(options)
        )
        return json.loads(urllib2.urlopen(url).read())


class Color(ColourLovers, Color):
    """Represents a COLOURlovers *color*.

    See :class:`sausage.Color`.
    """

    @classmethod
    def populate(cls, data):
        color = cls(**data["rgb"])
        map(lambda (key, value): setattr(color, key, value), filter(
            lambda (key, value): key not in ("hex", "rgb", "hsv"),
            data.items()))
        color.dateCreated = datetime.datetime.strptime(color.dateCreated,
            cls._DATETIME_FMT)
        return color

    @classmethod
    def from_id(cls, color_id):
        result = cls.make_request("color", color_id)
        if result:
            return cls.populate(result[0])

    @classmethod
    def from_new(cls, **options):
        return map(cls.populate, cls.make_request("colors", "new"))

    @classmethod
    def from_top(cls, **options):
        return map(cls.populate, cls.make_request("colors", "top"))

    @classmethod
    def from_random(cls, max_rank=None):
        return cls.populate(cls.make_request("colors", "random")[0])


class Palette(ColourLovers, Palette):
    """Represents a COLOURlovers *palette*.

    See :class:`sausage.Palette`.
    """

    __slots__ = ColourLovers._COMMON_SLOTS + ["colorWidths"]

    @classmethod
    def populate(cls, data):
        palette = cls()
        map(lambda (key, value): setattr(palette, key, value), data.items())
        palette.colors = map(Color.from_hex, palette.colors)
        palette.dateCreated = datetime.datetime.strptime(palette.dateCreated,
            cls._DATETIME_FMT)
        return palette

    @classmethod
    def from_id(cls, palette_id):
        result = cls.make_request("palette", palette_id)
        if result:
            return cls.populate(result[0])

    @classmethod
    def from_new(cls, **options):
        return map(cls.populate, cls.make_request("palettes", "new"))

    @classmethod
    def from_top(cls, **options):
        return map(cls.populate, cls.make_request("palettes", "top"))

    @classmethod
    def from_random(cls, max_rank=None):
        return cls.populate(cls.make_request("palettes", "random")[0])

    def __repr__(self):
        return "<Palette({0})>".format(self.colors)
