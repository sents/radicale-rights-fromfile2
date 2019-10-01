import configparser
import os.path
import posixpath
import re
from importlib import import_module
from radicale import storage


class Rights(BaseRights):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)
        self.filename = os.path.expanduser(configuration.get("rights", "file"))
        self.Storeclass = storage.load(configuration, logger)

    def authorized(self, user, path, permission):
        user = user or ""
        coll = self.Storeclass(path)
        displayname = coll.get_meta()["D:displayname"]
        displayname_escaped = re.escape(displayname)
        sane_path = storage.sanitize_path(path).strip("/")
        # Prevent "regex injection"
        user_escaped = re.escape(user)
        sane_path_escaped = re.escape(sane_path)
        regex = configparser.ConfigParser({
            "login": user_escaped,
            "path": sane_path_escaped,
            "displayname": displayname_escaped
        })
        try:
            if not regex.read(self.filename):
                raise RuntimeError("No such file: %r" % self.filename)
        except Exception as e:
            raise RuntimeError("Failed to load rights file %r: %s" %
                               (self.filename, e)) from e
        for section in regex.sections():
            try:
                re_user_pattern = regex.get(section, "user")
                re_collection_pattern = regex.get(section, "collection")
                re_displayname_pattern = regex.get(section, "displayname")
                # Emulate fullmatch
                user_match = re.match(r"(?:%s)\Z" % re_user_pattern, user)
                displayname_match = re.match(
                    r"(?:%s)\Z" % re_displayname_pattern, displayname)
                collection_match = user_match and re.match(
                    r"(?:%s)\Z" % re_collection_pattern.format(
                        *map(re.escape, user_match.groups())), sane_path)
            except Exception as e:
                raise RuntimeError("Error in section %r of rights file %r: "
                                   "%s" % (section, self.filename, e)) from e
            if user_match and collection_match:
                self.logger.debug("Rule %r:%r matches %r:%r from section %r",
                                  user, sane_path, re_user_pattern,
                                  re_collection_pattern, section)
                return permission in regex.get(section, "permission")
            else:
                self.logger.debug(
                    "Rule %r:%r doesn't match %r:%r from section"
                    " %r", user, sane_path, re_user_pattern,
                    re_collection_pattern, section)
        self.logger.info("Rights: %r:%r doesn't match any section", user,
                         sane_path)
        return False
