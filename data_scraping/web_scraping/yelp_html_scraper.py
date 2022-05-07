# region import libraries
import json
import requests
from bs4 import BeautifulSoup as bs
import sys
import re
import io
import datetime
# endregion


def initialize_prog():
    global start_time
    start_time = datetime.datetime.now()
    print(f"Program started at {start_time}")


def extract_html(website):
    '''
    Summary:
    ----------
    Extracts html using BeautifulSoup from website

    Params:
    ----------
    website : str
        The website to be analyzed
    
    Outputs:
    ----------
    soup (bs4.BeautifulSoup): object
        object containing html
    '''
    try:
        # Accessing website
        page = requests.get(website)

        # Checking connection
        if str(page.status_code) != '200':
            print("[ERROR] Bad connection. ")
            sys.exit()

        # Parsing HTML
        soup = bs(page.content, 'html.parser')
        print(f"\nSuccessful connection and parsing of:\n{website}")

        return soup

    except Exception as ex:
        print(f"[ERROR] extract_html: {ex.args}")
        sys.exit()


def extract_by_tag_type(soup):
    '''
    Summary:
    ----------
    Separates html tags and adds to dict based on tag type

    Params:
    ----------
    soup (bs4.BeautifulSoup) : object
        html to be analyzed
    
    Outputs:
    ----------
    tag_data_dict: dictionary
        dictionary containing tag types and data
    '''
    try:
        # Find tag types in html
        unique_tags = sorted(list(set([tag.name for tag in soup.find_all()])))

        print(unique_tags)

        tag_data_dict = {}

        for tag in unique_tags:
            # _tags = list(soup.find_all(re.compile(tags_dict[tag])))
            _tags = list(soup.find_all(re.compile(tag)))

            tag_dict = {}
            for _tag in _tags:
                tag_value = str(_tag.text).replace("\n", " ")
                notes = ""

                if (tag == 'a') or (tag == 'link'):
                    notes = str(_tag.get("href"))

                _tag_data_dict = {
                    "Value": tag_value,
                    "Tag Type": tag,
                    "Tag Name": _tag.name,
                    "Notes": notes
                }
                tag_dict.update({tag_value: _tag_data_dict})

            tag_data_dict.update({tag: tag_dict})

        return tag_data_dict

    except Exception as ex:
        print(f"[ERROR] extract_by_tag_type: {ex}")
        sys.exit()


def extract_by_class_type(soup):
    '''
    Summary:
    ----------
    Separates html tags and adds to dict based on
    tag type and class description

    Params:
    ----------
    soup (bs4.BeautifulSoup) : object
        html to be analyzed

    Outputs:
    ----------
    tag_final_dict: dictionary
        dictionary containing tag types and data
    '''
    try:
        # Identification of tag types and classes
        tag_class_dict = {
            'Website Header': ['h1', '''lemon--h1__373c0__2ZHSL heading--h1__373c0_
            __56D3 undefined heading--inline__373c0__1jeAh'''],

            'Company Phone': ['p', '''lemon--p__373c0__3Qnnj text__373c0__2U54h text
            -color--normal__373c0__NMBwo text-align--left__373c0__1Uy60'''],

            'Company Info Website(s)': ['a', '''lemon--a__373c0__IEZFH link__373c0__2-XHa link-c
            olor--blue-dark__373c0__4vqlF link-size--inherit__373c0__nQcnG'''],

            'COVID 19 Update': ['p', '''lemon--p__373c0__3Qnnj text__373c0__2U54
            h text-color--normal__373c0__NMBwo text-align--left__373c0__
            1Uy60 text-size--large__373c0__1j9OF'''],

            'Updated Services': ['span', '''lemon--span__373c0__3997G text__373c0__2U54h text
            -color--normal__373c0__NMBwo text-align--left__373c0__1Uy60 text-
            weight--semibold__373c0__3F7rQ text-size--large__373c0__1j9OF'''],

            'Health & Safety Measures': ['span', '''lemon--span__373c0__3997G text__373c0__2U54h 
            text-color--normal__373c0__NMBwo text-align--left__373c0__1Uy60 te
            xt-weight--semibold__373c0__3F7rQ text-size--
            large__373c0__1j9OF'''],

            'Link': ['a', '''lemon--a__373c0__IEZFH link__373c0__2-XHa link-color--
            inherit__373c0__2f-vZ link-size--inherit__373c0__nQcnG'''],

            'Review / Rating': ['span', '''lemon--
            span__373c0__3997G raw__373c0__3rKqk'''],

            'Image': ['img', '''lemon--img__373c0__3GQUb 
            photo-box-img__373c0__35y5v'''],

            'User ID': ['span', '''lemon--span__373c0__3997G text__373c0__2Kxyz
             fs-block text-color--blue-dark__373c0__1jX7S text-align--left
            __373c0__2XGa- text-weight--bold__373c0__1elNz'''],

            'Restaurants Also Viewed': ['span', '''lemon--span__373c0__3997G text__373c0__
            2Kxyz text-color--normal__373c0__3xep9 text-align--
            left__373c0__2XGa- text-size--inherit__373c0__2fB3p'''],
            }

        # Creation of dict to store all values
        tag_final_dict = {}

        # For each major section identified in tag_class_dict, do the following
        for item in tag_class_dict:
            i = 0

            # Find all tags, extract info, and add to tag_dicts which
            # are added to tag_final_dict
            tag_data_dict = {}
            tag_type = tag_class_dict[item][0]
            tag_class = tag_class_dict[item][1]

            for tag in soup.findAll(tag_type, {"class": tag_class}):
                # notes section is used for hyperlinks or image descriptions
                notes = ""
                tag_dict = {}
                tag_value = str(tag.text).replace("\n", " ")

                # Handling of special cases
                if str(tag_type) == 'a' or 'link':
                    notes = str(tag.get("href"))

                if str(tag_type) == 'img':
                    notes = str(tag.get("alt"))

                if (str(item) == 'Company Phone') and (re.search('[a-zA-Z]', str(tag_value)) is not None):
                    print('''\t[NOTE] Phone class identified but
                            non-numeric characters detected.''')
                else:
                    i += 1
                    tag_dict = {
                            "Index":    i,
                            "Value":    tag_value,
                            "Tag Type": str(tag).replace("\n", " "),
                            "Tag Name": tag.name,
                            "Notes":    notes
                        }
                    tag_dict_name = f"{item} {i}"
                    tag_data_dict.update({tag_dict_name: tag_dict})

            tag_final_dict.update({item: tag_data_dict})

        return tag_final_dict

    except Exception as ex:
        print(f"[ERROR] extract_by_class_type: {ex}")
        sys.exit()


def save_export_data(tag_dict, soup, website):
    '''
    Summary:
    ----------
    Exports data to html, txt, and json files

    Params:
    ----------
    tag_dict : dictionary
        dictionary containing tag types and data
    soup (bs4.BeautifulSoup) : object
        html to be analyzed
    webite : str
        scraped website
    
    Outputs:
    ----------
    None
    '''
    try:
        save_directory = 'C:\\Users\\User\\Desktop\\'
        webname = str(website.split("/")[-1])
        fname_html = save_directory + webname + ".html"
        fname_dict = save_directory + webname + "_class_dict.txt"
        fname_json = save_directory + webname + "_json_dict.json"

        with io.open(fname_dict, "w", encoding="utf-8") as f:
            dict_data = str(tag_dict).replace(": {", "\n\t:{").replace("},", "},\n\n")
            f.write(dict_data)
            f.close()

        with io.open(fname_html, "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))
            f.close()

        with open(fname_json, 'w') as f:
            json.dump(tag_dict, f)

    except Exception as ex:
        print(f"[ERROR] save_export_data: {ex}")
        sys.exit()


def terminate_prog():
    global end_time
    end_time = datetime.datetime.now()
    runtime = end_time - start_time
    print(f"Program finished at {end_time}")
    print(f"Performance: {runtime} seconds\n\n")


if __name__ == "__main__":
    initialize_prog()

    # Websites to parse
    websites = ['https://www.yelp.com/biz/the-truck-stop-culver-city-3',
                'https://www.yelp.com/biz/burger-lounge-culver-city-4']

    # User input on structure of json object
    json_structure_op = input('''JSON can be structured by tag type or
    website class structure. \n[1] Tag Type\n[2] Website Class \n''')

    for website in websites:
        # Extract html
        soup = extract_html(website)

        # Creating dictionary either based on tag type and
        # class or only on tag type
        if json_structure_op.lower().replace(" ", "") == 'websiteclass':
            tag_dict = extract_by_class_type(soup)
        else:
            tag_dict = extract_by_tag_type(soup)

        # Exporting to json and saving data
        save_export_data(tag_dict, soup, website)

        print(f"\nFinishing parsing of {website}\n")

    terminate_prog()
