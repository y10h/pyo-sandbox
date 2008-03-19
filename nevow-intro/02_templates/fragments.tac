from nevow import appserver
from twisted.application import service, strports
import fragments

site = appserver.NevowSite(fragments.Root())
application = service.Application('NevowFragmentsExample')
httpd = strports.service("tcp:8000", site)
httpd.setServiceParent(application)
