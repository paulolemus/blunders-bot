import yaml
import os
import os.path
import logging

logger = logging.getLogger(__name__)


def load_config(config_file):
    try:
        with open("./secret.txt") as token_stream:
            token = token_stream.read().strip()
    except EnvironmentError as e:
        logger.error("You are missing a secret.txt file with your required Lichess API token.")
        raise e

    with open(config_file) as stream:
        try:
            CONFIG = yaml.safe_load(stream)
        except Exception as e:
            logger.error("There appears to be a syntax problem with your config.yml")
            raise e

        # Add token to config from different file.
        CONFIG["token"] = token

        token_section = ["token", str, "External section `token` must be a string."]
        if token_section[0] not in CONFIG:
            raise Exception("Your secret.txt file does not have the required token.")
        elif not isinstance(CONFIG[token_section[0]], token_section[1]):
            raise Exception(token_section[2])

        # [section, type, error message]
        sections = [["url", str, "Section `url` must be a string wrapped in quotes."],
                    ["engine", dict, "Section `engine` must be a dictionary with indented keys followed by colons.."],
                    ["challenge", dict, "Section `challenge` must be a dictionary with indented keys followed by colons.."]]
        for section in sections:
            if section[0] not in CONFIG:
                raise Exception("Your config.yml does not have required section `{}`.".format(section[0]))
            elif not isinstance(CONFIG[section[0]], section[1]):
                raise Exception(section[2])

        engine_sections = [["dir", str, "´dir´ must be a string wrapped in quotes."],
                           ["name", str, "´name´ must be a string wrapped in quotes."]]
        for subsection in engine_sections:
            if subsection[0] not in CONFIG["engine"]:
                raise Exception("Your config.yml does not have required `engine` subsection `{}`.".format(subsection))
            if not isinstance(CONFIG["engine"][subsection[0]], subsection[1]):
                raise Exception("´engine´ subsection {}".format(subsection[2]))

        if CONFIG["token"] == "xxxxxxxxxxxxxxxx" or len(CONFIG["token"]) <= 2:
            raise Exception("Your secret.txt Lichess API token is probably wrong.")

        if not os.path.isdir(CONFIG["engine"]["dir"]):
            raise Exception("Your engine directory `{}` is not a directory.")

        # Engine discovery, with optional exe extension.
        extension = ".exe"
        engine_dir = CONFIG["engine"]["dir"]
        engine_name = CONFIG["engine"]["name"]
        engine = os.path.join(engine_dir, engine_name)

        if not os.path.isfile(engine) and CONFIG["engine"]["protocol"] != "homemade":
            # Could not find base name, so try to find with extension.
            engine_ext = os.path.join(engine_dir, engine_name + extension)
            if os.path.isfile(engine_ext):
                CONFIG["engine"]["name"] = engine_ext
                engine = engine_ext
            else:
                raise Exception("The engine %s file does not exist." % engine)

        if not os.access(engine, os.X_OK) and CONFIG["engine"]["protocol"] != "homemade":
            raise Exception("The engine %s doesn't have execute (x) permission. Try: chmod +x %s" % (engine, engine))

    return CONFIG
