from nevow import appserver
from twisted.application import service, strports
import formal_simple

site = appserver.NevowSite(formal_simple.Root())
application = service.Application('NevowFormalSimpleExample')
httpd = strports.service("tcp:8000", site)
httpd.setServiceParent(application)
