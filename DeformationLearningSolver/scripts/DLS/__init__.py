__author__ = "Webber Huang"
__contact__ = "xracz.fx@gmail.com"
__website__ = "http://riggingtd.com"


#----------------------------------------------------------------------
def launch():
    """"""
    from DLS.startup import setup
    reload(setup)
    setup.launch()