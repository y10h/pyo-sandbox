from lanyon import url

@url.register(match="posts/*")
def default(**kwargs):
    print "default url=%s" % (kwargs,)
    return '/blog/$year/$month/$day/$slug/'
