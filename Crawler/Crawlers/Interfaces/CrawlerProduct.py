import dateparser

from Crawler.Crawlers.CrawlerProcess import CrawlerProcess
from Crawler.Objects.Products.ObjectReviewsScore import ObjectReviewScore

class CrawlerProduct(CrawlerProcess):

    name = 'CrawlerEbay'

    url = 'http://ebay.com'
    domain = 'ebay.com'

    start_urls = (url,)
    allowed_domains = [domain]

    availableToBuy = True
    cssAvailableToBuy = "#binBtn_btn"

    cssTitle = "#itemTitle::text"
    cssItemCondition = "#vi-itm-cond::text"
    cssTimeLeft = "span.timeMs::attr(timems)"
    cssShippingSummary = "#shSummary"

    cssQuantityAvailable = "#qtySubTxt span::text"
    cssQuantitySold = "span.vi-qtyS-hot-red.vi-qty-vert-algn.vi-qty-pur-lnk a::text"

    cssItemSpecifications = "div.itemAttr "
    #cssItemConditionDetails = "#vi-cond-addl-info"
    cssItemConditionDetails = ""
    #cssItemBrand = "tr td h2 span"
    cssItemBrand = ""
    #cssItemMaterial = ""
    cssItemMaterial = ""

    cssFullDescription = "#desc_div"

    cssAuthor = "span.mbg-nw::text"
    cssAuthorLink = "#mbgLink::attr(href)"

    cssAuthorScore = "span.mbg-l a::text"
    cssAuthorFeedbackOverall = "#si-fb::text"

    cssItemId = "#descItemNumber::text"

    cssDateText = ""
    cssDate = ""

    cssImages = "td.tdThumb div img"

    cssBreadcrumbsChildrenList = "#vi-VR-brumb-lnkLst table tr td h2 ul li"
    cssBreadcrumbsChildrenListElementHref = 'a'
    cssBreadcrumbsChildrenListElement = 'a span'

    cssShipping = ""

    removeShortDescription = True


    cssListPrice = "#orgPrc::text"
    cssYouSave ="#youSaveSTP::text"
    cssPrice = "#prcIsum::text"
    cssWatching = "span.vi-buybox-watchcount::text"

    cssRatingScoresList = "ul.ebay-review-list li.ebay-review-item"
    cssRatingScoresListElementValue = "p.ebay-review-item-stars"
    cssRatingScoresListElementScore = "p.ebay-review-item-stars"

    cssReviewsList = "div.reviews div.ebay-review-section"
    cssReviewsListElementUsername = "div a"
    cssReviewsListElementDate = "div span::text"
    cssReviewsListElementRatingScore = ""
    cssReviewsListElementRatingScoreStars = "div div span i.fullStar"
    cssReviewsListElementTitle = "div p.review-item-title::text"
    cssReviewsListElementBody = "div p.review -item-content"
    cssReviewsListElementPurchased = "div p.review-attr"
    cssReviewsListElementThumbsUp = "div.review-btns div a span.review-section-rr-txt span.positive-h-c::text"
    cssReviewsListElementThumbsDown = "div.review-btns div a span.review-section-rr-txt span.negative-h-c::text"


    # variables

    itemCondition = ''
    itemSpecifications = ''
    itemConditionDetails = ''
    itemBrand = ''
    itemMaterial = ''

    timeLeft = ''
    shippingSummary = ''
    shipping = []

    authorScore = 0
    authorFeedbackOverall = 0

    itemId = ''
    quantityAvailable = 0
    quantitySold = 0


    listPrice = ''
    youSave = ''
    price = ''
    watching = ''

    ratingScoresList = []
    reviewsList = []

    def crawlerProcess(self, response, url):

        super().crawlerProcess(response, url)

        if self.removeShortDescription:
            self.shortDescription = ''
            self.ogDescription = ''

        if self.cssTitle != '':
            self.title = ''.join(response.css(self.cssTitle)).strip()

        if self.cssItemCondition != '':
            self.itemCondition = ''.join(response.css(self.cssItemCondition)).strip()

        if self.cssTimeLeft != '':
            self.timeLeft = ''.join(response.css(self.cssTimeLeft)).strip().strip()

        if self.cssQuantityAvailable != '':
            self.quantityAvailable = ''.join(response.css(self.cssQuantityAvailable)).strip()

        if self.cssQuantitySold != '':
            self.quantitySold = ''.join(response.css(self.cssQuantitySold)).strip()

        if self.cssShippingSummary != '':
            self.shippingSummary = ''.join(response.css(self.cssShippingSummary).extract()).strip()


        if self.cssItemSpecifications != '':
            self.itemSpecifications = ''.join(response.css(self.cssItemSpecifications)).strip()

        if self.cssItemConditionDetails != '':
            self.itemConditionDetails = ''.join(response.css(self.cssItemConditionDetails)).strip()

        if self.cssItemBrand != '':
            self.itemBrand = ''.join(response.css(self.cssItemBrand)).strip()

        if self.cssItemMaterial != '':
            self.itemMaterial = ''.join(response.css(self.cssItemMaterial)).strip()

        self.fullDescription = ''.join(response.css(self.cssFullDescription).extract()).strip()

        if self.cssAuthor != '':
            self.author = ''.join(response.css(self.cssAuthor)).strip()

        if self.cssAuthorLink != '':
            self.authorLink = ''.join(response.css(self.cssAuthorLink)).strip()

        if self.cssAuthorScore != '':
            self.authorScore = ''.join(response.css(self.cssAuthorScore)).strip()

        if self.cssAuthorFeedbackOverall != '':
            self.authorFeedbackOverall = ''.join(response.css(self.cssAuthorFeedbackOverall)).strip()

        if self.cssItemId != '':
            self.itemId = ''.join(response.css(self.cssItemId)).strip()

        if self.cssDateText != '':  #text format like 22 Jul 2017
            date = ' '.join(response.css(self.cssDate).extract()).strip()
            print("DATEEE",date)
            self.date = dateparser.parse(date)
        else: #timestamp format
            if self.cssDate != '':
                self.date = ''.join(response.css(self.cssDate))

        if self.cssImages != '':
            self.images = []

            images = response.css(self.cssImages)
            for i, image in enumerate(images):
                imageSrc = image.css('::attr(src)').extract_first()
                imageAlt = image.css('::attr(alt)').extract_first()

                self.images.append({'src': imageSrc, 'alt': imageAlt})

        if self.cssListPrice != '':
            self.listPrice = ''.join(response.css(self.cssListPrice))

        if self.cssYouSave != '':
            self.youSave = ''.join(response.css(self.cssYouSave))

        if self.cssPrice != '':
            self.price = ''.join(response.css(self.cssPrice))

        if self.cssWatching != '':
            self.watching = ''.join(response.css(self.cssWatching))

        if self.cssAvailableToBuy != '':
            self.availableToBuy = False
            if len(response.css(self.cssAvailableToBuy)) >0:
                self.availableToBuy = True


        if self.cssRatingScoresList != '' and len(self.title) > 0:
            self.ratingScoresList = []

            for i in range(1, 100):
                ratingScoreObject = response.css(self.cssRatingScoresList + ':nth-child(' + str(i) + ')')
                ratingScore = ''.join(ratingScoreObject.css(self.cssRatingScoresListElementScore+ '::text')).strip()
                ratingValue = ''.join(ratingScoreObject.css(self.cssRatingScoresListElementValue+ '::text')).strip()

                if ratingScore != '' and ratingValue != '':
                    self.ratingScoresList.append(ObjectReviewScore(ratingScore, ratingValue))

        if self.cssReviewsList != '' and len(self.title) > 0:
            self.reviewsList = []

            for i in range(1, 100):

                reviewObject = response.css(self.cssReviewsList + ':nth-child(' + str(i) + ')')
                reviewUsername = ''.join(reviewObject.css(self.cssReviewsListElementUsername)).strip()
                reviewDate = ''.join(reviewObject.css(self.cssReviewsListElementDate)).strip()
                reviewTitle = ''.join(reviewObject.css(self.cssReviewsListElementTitle)).strip()
                reviewBody = ''.join(reviewObject.css(self.cssReviewsListElementBody)).strip()

                if self.cssReviewsListElementRatingScore != '':
                    reviewScore = ''.join(reviewObject.css(self.cssReviewsListElementRatingScore)).strip()

                if self.cssReviewsListElementRatingScoreStars != '': #with stars
                    reviewScore = len(reviewObject.css(self.cssReviewsListElementRatingScoreStars))

                reviewPurchased = ''.join(reviewObject.css(self.cssReviewsListElementPurchased)).strip()
                reviewThumbsUp = ''.join(reviewObject.css(self.cssReviewsListElementThumbsUp)).strip()
                reviewThumbsDown = ''.join(reviewObject.css(self.cssReviewsListElementThumbsDown)).strip()

                if ratingScore != '' and ratingValue != '':
                    self.ratingScoresList.append(ObjectReviewScore(ratingScore, ratingValue))


    def validate(self):
        if (len(self.title) > 3) and (len(self.fullDescription) > 40) and self.availableToBuy:
            return 'product'

        return ''

    def toString(self):

        super().toString()

        if len(self.itemCondition) > 0: print("Item Condition", self.itemCondition)
        if len(self.itemSpecifications) > 0: print("Item Specs", self.itemSpecifications)
        if len(self.itemConditionDetails) > 0: print("Item Condition Details", self.itemConditionDetails)
        if len(self.itemBrand) > 0: print("Item Brand", self.itemBrand)
        if len(self.itemMaterial) > 0: print("Item Material", self.itemMaterial)
        if len(self.timeLeft) > 0: print("Time Left", self.timeLeft)
        if len(self.authorScore) > 0: print("Author Score", self.authorScore)
        if len(self.authorFeedbackOverall) > 0: print("Author Feedback Overall", self.authorFeedbackOverall)
        if len(self.itemId) > 0: print("Item ID", self.itemId)

        if len(self.quantityAvailable) > 0: print("Quantity Available", self.quantityAvailable)
        if len(self.quantitySold) > 0: print("Quantity Sold", self.quantitySold)

        if len(self.images) > 0: print("Images", self.images)
        if len(self.shippingSummary) > 0: print("Shipping Summary", self.shippingSummary)
        if len(self.shipping) > 0: print("Shipping", self.shipping)

        if len(self.listPrice) > 0: print("List Price", self.listPrice)
        if len(self.youSave) > 0: print("You Save", self.youSave)
        if len(self.price) > 0: print("Price", self.price)
        if len(self.watching) > 0: print("Watching", self.watching)

        if len(self.ratingScoresList) >0: print("Rating Scores List", self.ratingScoresList)

        print("Available To Buy", self.availableToBuy)