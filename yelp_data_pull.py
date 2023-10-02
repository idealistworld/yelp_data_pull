import requests
import csv

dataToScrape = []
collectedAndFormattedData = []

with open('yelp_link_list.csv', mode='r') as csv_file:
    csvreader = csv.reader(csv_file)
    for row in csvreader:
        dataToScrape.append(str(row[0]))

for link in dataToScrape:
    print(link)
    url = link
    html = requests.get(url)

    # Get the business name
    try:
        businessName = html.text[html.text.index(
            'class="css-1se8maq">')+20:html.text.index('class="css-1se8maq">')+90]
        businessNameEnd = businessName.index("</h1")
        businessName = businessName[0:businessNameEnd]
    except Exception as e:
        businessName = "N/A"

    # Get Average Rating
    try:
        averageRating = html.text[html.text.index(
            'class=" css-1fdy0l5"')+49:html.text.index('class=" css-1fdy0l5"')+80]
        averageRatingEnd = averageRating.index("<!--")
        averageRating = averageRating[0:averageRatingEnd]
    except Exception as e:
        averageRating = "N/A"

    # Get Total Ratings
    try:
        totalRatings = html.text[html.text.index(
            '<a href="#reviews" class="css-19v1rkv">')+40:html.text.index('<a href="#reviews" class="css-19v1rkv">')+80]
        totalRatingsEnd = totalRatings.index(")</a></span></")
        totalRatings = int(totalRatings[0:totalRatingsEnd].split(" ")[0])
    except Exception as e:
        totalRatings = "N/A"

    # Get Address
    try:
        streetAddress = html.text[html.text.index(
            ' raw__09f24__T4Ezm')+20:html.text.index(' raw__09f24__T4Ezm')+60]
        streetAddressEnd = streetAddress.index("</span></a></p")
        streetAddress = streetAddress[0:streetAddressEnd]
        cityInformation = html.text[html.text.index('<p class=" css-1sb02f4" data-font-weight="bold"><span class=" raw__09f24__T4Ezm">') +
                                    81:html.text.index('<p class=" css-1sb02f4" data-font-weight="bold"><span class=" raw__09f24__T4Ezm">')+120]
        cityInformationEnd = cityInformation.index('</span></p></address>')
        cityInformation = cityInformation[0:cityInformationEnd]
        address = streetAddress + ", " + cityInformation
    except Exception as e:
        address = "N/A"


    # Get Phone Number
    try:
        phoneNumber = html.text[html.text.index(
            '<p class=" css-na3oda">Phone number</p>')+91:html.text.index('<p class=" css-na3oda">Phone number</p>')+105]
    except Exception as e:
        phoneNumber = "N/A"

    # Get Business Site
    try:
        businessSite = html.text[html.text.index(
            '<p class=" css-na3oda">Business website</p>')+350:html.text.index('<p class=" css-na3oda">Business website</p>')+550]
        businessSite = businessSite[businessSite.index('role="link">') + 12:businessSite.index('</a></p></div><div')]
    except Exception as e:
        businessSite = "N/A"

    # Get Google Review Link
    try:
        googleReviewLink = 'https://www.google.com/search?q=' + \
            (businessName + address.replace(",", "")).replace(" ", "+")
    except Exception as e:
        googleReviewLink = "N/A"

    # Format the Shipping Address
    shippingAddress = businessName + "\n" + streetAddress + "\n" + cityInformation

    dataToImport = [businessName, url, googleReviewLink,
                    averageRating, totalRatings, address, shippingAddress, phoneNumber, businessSite]


    collectedAndFormattedData.append(dataToImport)

with open("business_data.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    fields = ['BusinessName', 'Yelp URL', 'Google Review Link',
              'Average Rating', 'Total Ratings', 'Address', 'Shipping Address', 'Phone Number', 'Business Site']
    csvwriter.writerow(fields)
    for dataSet in collectedAndFormattedData:
        csvwriter.writerow(dataSet)
