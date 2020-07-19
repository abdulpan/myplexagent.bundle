SEARCH_PIC_URL = 'https://onejav.com/search/%s'
curID = "onejav"
SEARCH_TITLE_URL = 'https://www.javbus.com/%s'
#curID = "javbus"


def search(query, results, media, lang):
    try:
        Log('Search Query (title): %s' % str(SEARCH_TITLE_URL % query))

        movieid = HTML.ElementFromURL(SEARCH_TITLE_URL % query).xpath('//div[contains(@class,"container")]/h3')[0].text_content().strip()
        results.Append(MetadataSearchResult(id=curID + "|" + str(query), name=str(movieid), score=100, lang=lang))

        results.Sort('score', descending=True)
        Log(results)
    except Exception as e:
        Log(e)


def update(metadata, media, lang):
    if curID != str(metadata.id).split("|")[0]:
        return

    query = str(metadata.id).split("|")[1]
    Log('Update Query (image): %s' % str(SEARCH_PIC_URL % metadata.id))
    try:
        movie = HTML.ElementFromURL(SEARCH_PIC_URL % query).xpath('//div[contains(@class,"container")]')[0]

        # post
        image = movie.xpath('.//img[contains(@class,"image")]')[0]
        thumbUrl = image.get('src')
        thumb = HTTP.Request(thumbUrl)
        posterUrl = image.get('src')
        metadata.posters[posterUrl] = Proxy.Preview(thumb)

        # tags
        taglist = []
        metadata.genres.clear()
        for tagElem in HTML.ElementFromURL(SEARCH_TITLE_URL % query).xpath('//div[contains(@class,"container")]/span[contains(@class,"genre")]/a'):
            tag = tagElem.text_content().strip()
            metadata.genres.add(tag)
            taglist.append(tag)
        Log("Tags found: %s" % (' | '.join(taglist)))
        #metadata.title = metadata.name

        metadata.movie.xpath('.//p[contains(@class,"level has-text-grey-dark")]')[0].text_content().strip()
    except Exception as e:
        Log(e)
        Log("error")