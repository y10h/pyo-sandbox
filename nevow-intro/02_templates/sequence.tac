from nevow import appserver
from twisted.application import service, strports
import sequence

site = appserver.NevowSite(sequence.Root())
application = service.Application('NevowSequenceRenderer')
httpd = strports.service("tcp:8000", site)
httpd.setServiceParent(application)
