# Based on https://github.com/micahsteinberg/redfin-recently-sold-property-scraper
import requests
import json
import csv

OUT_FILENAME = "recently_sold_redfin.csv"
TIME_RANGE_DAYS = 90


def create_sold_property_csv(filename):
    """
    Opens a templated csv file for storing sold property data.

    Parameters:
        filename (string): name of output file

    Returns:
        (file, csv.DictWriter): file object and writer for newly created csv file
    """

    csvFile = open(filename, "w", newline="")
    # clang-off
    fields = [
        "date_sold",\
        # This is the listing price.
        "price",\
        # This is price at which it was sold.
        "original_price",\
        "price_spread",\
        "square_footage",\
        "lot_size",\
        "number_bedrooms",\
        "number_bathrooms",\
        "year_built",\
#        "latitude",\
#        "longitude",\
        "property_type",\
        "street_number",\
        "street_name",\
#        "neighborhood",\
        "city",\
        "state",\
        "zip_code",\
        "days_until_sold",\
        "is_short_sale",\
        "url"
    ]
    # clang-on
    csvWriter = csv.DictWriter(csvFile, fieldnames=fields, restval="")
    csvWriter.writeheader()
    return (csvFile, csvWriter)


def get_sold_property_json(id):
    """
    Makes an HTTP request to redfin.com for a JSON containing data of properties
    withing input region id that were sold in the past input number of days.

    Searching by region id is the broadest search I'm aware of on refin.com that
    also won't contain repeated properties in multiple searches.

    Parameters:
        id (int): redfin region id to query for properties in
        days (int): number of days into the past the data will go

    Returns:
        dict: the content of the JSON file returned by redfin.com
    """

    # This url is approved for bots in redfin.com/txt, so its unnecessary to
    # include sleep logic as they won't block your IP
    url = "https://www.redfin.com/stingray/do/gis-search?al=1" +\
        "&num_homes=100000&region_id=" + str(id) + "&region_type=6" +\
        "&num_baths=1.25&max_num_baths=2&num_beds=2&max_num_beds=3" +\
        "&min_listing_approx_size=1200&sold_within_days=" + str(TIME_RANGE_DAYS)
    headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        jsonData = json.loads(r.content[4:])
    except (requests.ConnectionError, json.decoder.JSONDecodeError):
        # Failed to connect or read JSON properly. Skip this one.
        return
    return jsonData


def parse_sold_property_json(csvWriter, jsonData):
    """
    Parses JSON redfin.com sold property data and appends it to CSV file.

    Parameters:
        csvWriter (csv.DictWriter): writer to desired csv file
        jsonData (dict): data from redfin.com sold property JSON
    """

    # Return if JSON is empty or an error occured while being retreived
    if jsonData == None:
        return
    if jsonData["errorMessage"] != "Success":
        return

    # Construct and write new row for every property listed in the JSON
    for property in jsonData["payload"]["search_result"]:
        row = {}

        # For every field, check if it exists before adding it to prevent an exception
        if "date" in property:
            row.update(date_sold=property["date"])
            if "listing_added" in property:
                ms_until_sold = int(property["date"]) - int(
                    property["listing_added"])
                row.update(
                    days_until_sold=int(ms_until_sold / (1000 * 60 * 60 * 24)))
        if "price" in property:
            row.update(price=int(property["price"]))
            if "original_price" in property:
                row.update(original_price=int(property["original_price"]))
                row.update(
                    price_spread=int(property["original_price"]) -
                    int(property["price"]))
        if "sqft" in property:
            row.update(square_footage=property["sqft"])
        if "lotsize" in property:
            row.update(lot_size=property["lotsize"])
        if "beds" in property:
            row.update(number_bedrooms=property["beds"])
        if "baths" in property:
            row.update(number_bathrooms=property["baths"])
        if "year_built" in property:
            row.update(year_built=property["year_built"])
        if "type" in property:
            row.update(property_type=property["type"])


#        if "neighborhood" in property:
#            row.update(neighborhood=property["neighborhood"])
#        if "parcel" in property:
#            if "latitude" in property["parcel"]:
#                row.update(latitude=property["parcel"]["latitude"])
#            if "longitude" in property["parcel"]:
#                row.update(longitude=property["parcel"]["longitude"])
        if "address_data" in property:
            address = property["address_data"]
            if "number" in address:
                row.update(street_number=address["number"])
            if "street" in address and "type" in address:
                row.update(street_name = address["street"] + " "\
                    + address["type"])
            if "city" in address:
                row.update(city=address["city"])
            if "state" in address:
                row.update(state=address["state"])
            if "zip" in address:
                row.update(zip_code=address["zip"])
        if "is_short_sale" in property:
            row.update(is_short_sale=property["is_short_sale"])
        # Joana: added URL.
        if "URL" in property:
            row.update(url="https://redfin.com" + property["URL"])

        # Write the row to the CSV file
        csvWriter.writerow(row)

if __name__ == "__main__":
    # Create CSV file
    (csvFile, csvWriter) = create_sold_property_csv(OUT_FILENAME)

    # Joana: use instead only city ids of interest:
    idsOfInterest = [
        10229,  # Melrose
        9614,  # Malden
        10142,  # Medford
        29622,  # Winchester
        29663,  # Burlington
        16064  # Somerville
    ]

    for id in idsOfInterest:
        jsonData = get_sold_property_json(id)
        parse_sold_property_json(csvWriter, jsonData)
        csvFile.flush()

    print("\nCompleted!")

    csvFile.close()
