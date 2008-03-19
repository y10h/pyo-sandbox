from nevow import appserver
from twisted.application import service, strports
import childFactory

site = appserver.NevowSite(childFactory.Root())
application = service.Application('NevowObjectTraversalChildFactory')
httpd = strports.service("tcp:8000", site)
httpd.setServiceParent(application)
