import logging

lg = None
def getLogger(lvl):
    global lg
    if lg is not None:
        return lg
    lg = logging.getLogger("logger")
    lg.setLevel(lvl)
    ch = logging.StreamHandler()
    ch.setLevel(lvl)
    formatter = logging.Formatter('[%(levelname)s] : %(message)s')
    ch.setFormatter(formatter)
    lg.addHandler(ch)
    return lg
