import vk_api
from vk_api import VkTools
from package.vk_token import token
import datetime


class VkBot:
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    now = datetime.datetime.now()

    def user_data(self, id_user):
        res = self.vk.users.get(user_ids=id_user, fields='city, sex, bdate')[0]
        year = None if 'bdate' not in res or not res['bdate'][-4:].isnumeric() else res['bdate'][-4:]
        city = None if 'city' not in res else res['city']['title']
        sex = None if 'sex' not in res else res['sex']
        # return res
        return {'name': res['first_name'], 'sex': sex, 'year': year, 'city': city}

    def vk_user_search(self, data):
        city = data['city']
        sex = 2 if data['sex'] == 1 else 1
        age = self.now.year - int(data['year'])
        age_from = age - 5 if sex == 1 else age  # Возраст от: на 5 лет младше пользователя, если муж
        age_to = age_from + 5 if sex == 2 else age  # Возраст до: на 5 лет старше пользователя, если жен
        rs = VkTools(self.vk).get_all_iter(
            method='users.search',
            max_count=1000,
            values={'is_closed': False, 'fields': 'relation, bdate', 'hometown': city, 'sex': sex, 'age_from': age_from,
                    'age_to': age_to, 'has_photo': 1, 'status': 6},
            key='items')
        return rs

    def get_vk_photos(self, id_user: str):
        res = self.vk_session.method('photos.get', {
            'album_id': 'profile',
            'extended': 1,
            'owner_id': id_user})
        info_list = []
        for i in res['items']:
            likes = i['likes']['count']
            comments = i['comments']['count']
            info_list.append([likes, comments, i['owner_id'], i['id'], i['sizes'][-1]['url']])
        sort_lst = sorted(info_list, key=lambda x: (x[1], x[0]))[-3:]
        return [f'photo{photo_data[2]}_{photo_data[3]}' for photo_data in sort_lst]


if __name__ == '__main__':
    a = VkBot()
    b = VkBot()
    # print(a.user_data('191576096'))
    # print(b.user_data('masagytov'))
    f = b.vk_user_search({'name': 'Радик', 'sex': 2, 'year': 1985, 'city': 'Москва'})
    print(f)
