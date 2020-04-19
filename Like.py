import requests
import constants
import datetime


def dict_to_list_of_tuples(dictionary):
    l = []
    for key in dictionary:
        l.append((key, dictionary[key]))
    return l


def get_user(user_ids):
    payload = {
        'v': 5.71,
        'access_token': constants.ACCESS_TOKEN,
        "user_ids": user_ids,
    }
    response = requests.get('https://api.vk.com/method/users.get', params=payload)
    return response


def get_friends(user_id):
    payload = {
        'v': 5.71,
        'access_token': constants.ACCESS_TOKEN,
        "user_id": user_id,
        "fields": "bdate"
    }
    return requests.get('https://api.vk.com/method/friends.get', params=payload)


def how_old(str_bdate):
    curr_year, curr_month, curr_day = str(datetime.date.today()).split('-')
    try:
        day_bdate, month_bdate, year_bdate = str_bdate.split('.')
    except ValueError:
        return None
    if int(month_bdate) < int(curr_month):
        return int(curr_year) - int(year_bdate)
    elif int(month_bdate) > int(curr_month):
        return int(curr_year) - int(year_bdate) - 1
    elif int(curr_day) < int(day_bdate):
        return int(curr_year) - int(year_bdate) - 1
    else:
        return int(curr_year) - int(year_bdate)


def count_number_age(dict_age, age):
    try:
        dict_age[age] += 1
    except KeyError:
        dict_age[age] = 1
    return dict_age[age]


def get_list_id(owner_id):
    payload = {
        'v': 5.71,
        'access_token': constants.ACCESS_TOKEN,
        'owner_id': owner_id,
        'album_id': 'profile',
        'photo_sizes': 0
    }
    list_items = requests.get(
        'https://api.vk.com/method/photos.get',
        params=payload
    ).json()['response']['items']
    list_id_items = []
    for i in list_items:
        list_id_items.append(i['id'])
    return list_id_items


def who_likes(owner_id, item_id):
    payload = {
        'v': 5.71,
        'access_token': constants.ACCESS_TOKEN,
        "type": 'photo',
        'owner_id': owner_id,
        'item_id': item_id,
        'extended': 1,
    }
    # print(requests.get('https://api.vk.com/method/likes.getList', params=payload).json())
    likes_list_of_photo_profile = requests.get(
        'https://api.vk.com/method/likes.getList',
        params=payload
    ).json()['response']['items']
    return likes_list_of_photo_profile


def count_likes(list_person_who_likes, res):
    for person_like in list_person_who_likes:
        res_item = list(filter(lambda person: person['id'] == person_like['id'], res))
        if res_item:
            res_item[0]['count'] += 1
        else:
            res.append(
                {
                    'id': person_like['id'],
                    'first name': person_like['first_name'],
                    'last name': person_like['last_name'],
                    'count': 1,
                }
            )

    return res


if __name__ == '__main__':
    """
    This script create a list, which show how many likes you get from each person
    """
    user_ids = input("Enter user_ids. For example we have url of home page https://vk.com/id195168265, id195168265 is user_ids\n" )
    id = get_user(user_ids).json()['response'][0]['id']
    list_id = get_list_id(id)
    res = []
    for i in list_id:
        list_peson_like = who_likes(id, i)
        res = count_likes(list_peson_like, res)
    print(sorted(res, key=lambda dict: dict['count'], reverse=True))

