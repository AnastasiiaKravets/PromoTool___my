
def xpath_of_text(text):
    # Find apostrophe in the future XPATH string, and split the string so that apostrophe will be alone and later
    # concatenated with the rest of the characters in the final XPATH expression
    text_with_modified_apostrophe = string_modified_for_xpath(text)

    # Search for unique/exact text on the page, currently not working with % character, but with others works OK
    full_xpath = "//div[@class='k-grid-content k-auto-scrollable']//td[./text()= %s]" % text_with_modified_apostrophe

    # Search for any string that contains given text (possible workaround if exact match doesn't work)
    # full_xpath = "//div[@class='k-grid-content k-auto-scrollable']//td[contains(text(), %s )]" % (role_name_modified)
    return full_xpath


# Search if there is any apostrophe in the XPATH string, and splits the string if apostrophe was found, in such way
# that string is divided by each located apostrophe.
# Then the string is reassembled with the concat() function when send to XPATH
def string_modified_for_xpath(xpath_name):
    # validate the string , convert the input to string just in case
    if len(xpath_name) > 0:
        item_text = str(xpath_name)

    # Locate the apostrophe in the string and modify it:
    # 1) surround it with double quotes \"'\"  ( backslashes are used as escape characters, meaning to show python that
    #    it is not string but real double quotes  which will be parsed by XPATH later )
    # 2) surround it with comas , \"'\", so that it will be used as part of concat() XPATH command which will later
    #    combine this apostrophe with other characters in the corresponding places in string
    if item_text.find("'") > 0:
        item_text = item_text.replace("'", "', \"'\", '")
        item_text = "concat('" + item_text + "')"
    # if there is no apostrophe then just put the XPATH in the apostrophes, and there will be no conflicts with other
    # apostrophes , because there is none present in the string
    else:
        item_text = "'" + item_text + "'"

    return item_text