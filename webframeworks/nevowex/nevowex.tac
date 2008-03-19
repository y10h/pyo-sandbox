from nevowex import get_nevow_site
from twisted.application import service, strports

application = service.Application('NevowEx')
httpd = strports.service("tcp:8000", get_nevow_site())
httpd.setServiceParent(application)
