from nevow import appserver
from twisted.application import service, strports
import insert_data

site = appserver.NevowSite(insert_data.Root())
application = service.Application('NevowTemplatesInsertData')
httpd = strports.service("tcp:8000", site)
httpd.setServiceParent(application)
