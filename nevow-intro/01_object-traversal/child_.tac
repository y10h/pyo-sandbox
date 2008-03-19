from nevow import appserver
from twisted.application import service, strports
import child_

site = appserver.NevowSite(child_.Root())
application = service.Application('NevowObjectTraversalChild')
httpd = strports.service("tcp:8000", site)
httpd.setServiceParent(application)
