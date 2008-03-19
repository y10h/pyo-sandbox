from nevow import appserver
from twisted.application import service, strports
import condition

site = appserver.NevowSite(condition.Root())
application = service.Application('NevowTemplatesConditionalData')
httpd = strports.service("tcp:8000", site)
httpd.setServiceParent(application)
