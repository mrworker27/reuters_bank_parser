import logging

def getLogger(lvl):
    lg = logging.getLogger("logger")
    lg.setLevel(lvl)
    ch = logging.StreamHandler()
    ch.setLevel(lvl)
    formatter = logging.Formatter('[%(levelname)s] : %(message)s')
    ch.setFormatter(formatter)
    lg.addHandler(ch)
    return lg
