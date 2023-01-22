# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from .attr_dict import AttrDict
import configparser


class Config:
    """
    Wrapper for configparser
    """
    def __init__(self, path):
        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str
        config.sections()
        config.read(path)

        self.attrs = AttrDict(dict(config["CONFIG"]))
