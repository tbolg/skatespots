import requests
from bs4 import BeautifulSoup
import googlemaps
import json
import shutil
import os.path

def main():
    get_spots()
    download_images_from_json()

def get_spots():
    # Get spot name and link
    page_number = 1
    base_url = 'https://www.skateboard.com.au'
    location_list = []
    while True:
        skatespots_url = f'https://www.skateboard.com.au/listeo/HTML/results.cfm?country=Australia&state=&sort=&type=spot&lat=&long=&name=&glocal=&p={str(page_number)}'
        page = requests.get(skatespots_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        row_elems = soup.find_all('a', class_='listing-item-container')
        for row in row_elems:
            row_dict = {
                'link': base_url + row['href'],
                'address': row.find('span').text,
                'name': row.find('h3').text,
                'img': row.find('img')['src']
            }
            print(row_dict)
            location_list.append(row_dict)
        page_number += 1
        if len(row_elems) < 20:
            break

    # Get lat and lng from address
    coordinate_list = []
    gmaps = googlemaps.Client(key='AIzaSyALma_bIrPD2I6AcEQ5kHreIHVu7qXg8aI')
    for location in location_list:
        geocode_raw = gmaps.geocode(location['address'])
        #print(geocode_raw)
        geocode_result = geocode_raw[0]['geometry']['location']
        coordinate_dict = {
            'lat': geocode_result['lat'],
            'lng': geocode_result['lng']
        }
        coordinate_dict.update(location)
        coordinate_list.append(coordinate_dict)
        print(coordinate_dict)

    # Write to json file
    with open('spots.json', 'w') as spots_file:
        spots_file.write(json.dumps(coordinate_list))

def download_images_from_json():
    img_dir = 'imgs'
    try:
        os.mkdir(img_dir)
    except Exception:
        pass
    with open("spots.json", 'r') as spots_file:
        file_string = spots_file.read()
        file_json = json.loads(file_string)
        for row in file_json:
            response = requests.get(row['img'], stream=True)
            with open(os.path.join(img_dir, f'{row["img"].split("/")[-1]}'), 'wb') as img_file:
                print(row['img'])
                shutil.copyfileobj(response.raw, img_file)

if __name__ == "__main__":
    main()

