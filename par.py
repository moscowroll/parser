import bs4
import requests
import pprint

url = 'https://www.auction-house.ru/catalog/?show_type=list'
r = requests.get(url).text

soup = bs4.BeautifulSoup(r , 'html.parser')

# поиск блока контекта
InfoBlock = soup.find('div', {'class': "container", "id":"elements"})
content = InfoBlock.find('div', {'class': 'catalog-list short'})


# вывод названий групп объектов
Group_names = []

Object_types = content.find_all('tbody', {'class': 'group-header'})
for element in Object_types:
    object_name = element.find('span').text
    Group_names.append(object_name)
# print(names)


# ПЕРЕМЕННАЯ ДЛЯ ВСЕХ ОБЪЕКТОВ , ПОДЕЛЕННАЯ ПО ТИПАМ
ALL_OBJECTS={}


# вывод
Unique_object_type = {}

Preparing_for_sale = []
Auction_announced = []
Direct_selling=[]



Catalog_list_groups = content.find_all('tbody', {'class': 'catalog-list-group'})
# print(len(Catalog_list_groups)) 15
for number, group in enumerate(Catalog_list_groups):
    Group_objects = group.find_all('tr')
    # print(len(Group_objects)) 438
    for object in Group_objects:
        building = {}
        description = object.find('td', {'class': 'description'}).get('title')
        address = object.find('td', {'class': 'address'}).get('title')
        square = object.find('td', {'class': 'square'}).text.replace(' ','').replace(',' , '.')
        if square != '':
            square = float(square)
        else:
            square = None
        price = object.find('td', {'class': 'price'}).text.replace(' ','').replace(',' , '.')
        if price != '':
            price = float(price)
        else:
            price = None
        building['description'], building['address'], building['square'], building['price'] = description, address, square, price
        type = object.find('div', {'class': 'rollover'}).text.strip().lower()
        if type == "готовится к продаже":
            Preparing_for_sale.append(building)
        elif type == "прямая продажа":
            Direct_selling.append(building)
        else:
            Auction_announced.append(building)
        # print(len(Preparing_for_sale))
        # print(len(Auction_announced))
        # print(len(Direct_selling))
    Unique_object_type['Preparing_for_sale'] = Preparing_for_sale
    Unique_object_type['Auction_announced'] = Auction_announced
    Unique_object_type['Direct_selling'] = Direct_selling

    ALL_OBJECTS[Group_names[number]] = Unique_object_type
    Unique_object_type = {}
    Preparing_for_sale = Auction_announced = Direct_selling = []
    if number == 2:
        break
pprint.pprint(ALL_OBJECTS)
# print(ALL_OBJECTS)
