from nevow import appserver
from twisted.application import service, strports
import children

site = appserver.NevowSite(children.Root())
application = service.Application('NevowObjectTraversalChildren')
httpd = strports.service("tcp:8000", site)
httpd.setServiceParent(application)
