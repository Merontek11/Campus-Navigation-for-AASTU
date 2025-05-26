from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Place, Category

class CampusNavigationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='adminpass')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.category = Category.objects.create(name_en="Library")
        self.place = Place.objects.create(
            name="Main Library",
            category="library",
            description="A quiet place to study.",
            latitude=9.03,
            longitude=38.75,
        )

    def test_get_places_list(self):
        url = reverse('place-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_place(self):
        url = reverse('place-list')
        data = {
            "name": "New Lab",
            "category": "lab",  
            "description": "Computer lab",
            "latitude": 9.04,
            "longitude": 38.76,
        }
        response = self.client.post(url, data, format='json')
        print("Create Place Response:", response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_single_place(self):
        url = reverse('place-detail', args=[self.place.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_place(self):
        url = reverse('place-detail', args=[self.place.id])
        data = {"name": "Updated Library"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Update response:", response.data)


    def test_delete_place(self):
        url = reverse('place-detail', args=[self.place.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_categories_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_category(self):
    #     url = reverse('category-list')
    #     data = {"name_en": "Cafeteria"}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_create_category(self):
        url = reverse('category-list')
        data = {
        "name_en": "Cafeteria",
        "name_am": "መጠጣቤት"
               }
        response = self.client.post(url, data, format='json')
        print("Create Category Response:", response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_single_category(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        url = reverse('category-detail', args=[self.category.id])
        data = {"name_en": "Updated Category"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name_en"], "Updated Category")

    def test_delete_category(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_search_place_by_name(self):
        url = reverse('place-list') + '?search=Library'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("Library" in place["name"] for place in response.data))

    def test_filter_place_by_category(self):
        url = reverse('place-list') + f'?category={"library"}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print("Create Category Response:", response.data) 
        self.assertTrue(all(place["category"] == "library" for place in response.data))

    def test_invalid_long_search_query(self):
        long_query = 'a' * 101
        url = reverse('place-list') + f'?search={long_query}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)











