# populate_data.py
import os
import django
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()


def populate_test_data():
    User = get_user_model()

    # Очистка старых данных (осторожно!)
    # User.objects.all().delete()
    # Product.objects.all().delete()
    # Order.objects.all().delete()
    # Tariff.objects.all().delete()
    # UserSubscription.objects.all().delete()

    with transaction.atomic():
        # Создаем пользователей
        users_data = [
            {
                'username': 'ivanov',
                'email': 'ivanov@example.com',
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'password': 'password123',
                'phone': '+79161234567',
                'bio': 'Люблю программирование и спорт'
            },
            {
                'username': 'petrov',
                'email': 'petrov@example.com',
                'first_name': 'Петр',
                'last_name': 'Петров',
                'password': 'password123',
                'phone': '+79169876543',
                'bio': 'Фотограф и путешественник'
            },
            {
                'username': 'sidorova',
                'email': 'sidorova@example.com',
                'first_name': 'Мария',
                'last_name': 'Сидорова',
                'password': 'password123',
                'phone': '+79165554433',
                'bio': 'Дизайнер и художник'
            },
            {
                'username': 'admin_user',
                'email': 'admin@example.com',
                'first_name': 'Админ',
                'last_name': 'Админов',
                'password': 'admin123',
                'phone': '+79160000000',
                'bio': 'Системный администратор',
                'is_staff': True,
                'is_superuser': True
            }
        ]

        users = []
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                bio=user_data.get('bio', ''),
                is_staff=user_data.get('is_staff', False),
                is_superuser=user_data.get('is_superuser', False)
            )
            users.append(user)
            print(f"Создан пользователь: {user.username}")

        # Создаем продукты
        from products.models import Product

        products_data = [
            {'name': 'iPhone 15 Pro', 'price': 99999.99},
            {'name': 'MacBook Air M2', 'price': 89999.50},
            {'name': 'AirPods Pro', 'price': 24999.00},
            {'name': 'iPad Pro', 'price': 79999.00},
            {'name': 'Apple Watch Series 9', 'price': 39999.00},
            {'name': 'Samsung Galaxy S23', 'price': 74999.00},
            {'name': 'Sony WH-1000XM5', 'price': 29999.00},
            {'name': 'Xiaomi Robot Vacuum', 'price': 19999.50},
            {'name': 'Canon EOS R6', 'price': 149999.00},
            {'name': 'Nintendo Switch OLED', 'price': 27999.00}
        ]

        products = []
        for product_data in products_data:
            product = Product.objects.create(
                name=product_data['name'],
                price=product_data['price']
            )
            products.append(product)
            print(f"Создан продукт: {product.name} - {product.price} руб.")

        # Создаем тарифы
        from subscriptions.models import Tariff

        tariffs_data = [
            {'name': 'Базовый', 'discount_percent': 5},
            {'name': 'Стандартный', 'discount_percent': 10},
            {'name': 'Премиум', 'discount_percent': 15},
            {'name': 'Бизнес', 'discount_percent': 20},
            {'name': 'VIP', 'discount_percent': 25}
        ]

        tariffs = []
        for tariff_data in tariffs_data:
            tariff = Tariff.objects.create(
                name=tariff_data['name'],
                discount_percent=tariff_data['discount_percent']
            )
            tariffs.append(tariff)
            print(f"Создан тариф: {tariff.name} - {tariff.discount_percent}% скидка")

        # Создаем подписки пользователей
        from subscriptions.models import UserSubscription

        subscriptions_data = [
            {'user': users[0], 'tariff': tariffs[2], "is_active": True},  # Иванов - Премиум
            {'user': users[1], 'tariff': tariffs[1], "is_active": False},  # Петров - Стандартный
            {'user': users[2], 'tariff': tariffs[3], "is_active": False},  # Сидорова - Бизнес
        ]

        for sub_data in subscriptions_data:
            subscription = UserSubscription.objects.create(
                follower=sub_data['user'],
                tariff=sub_data['tariff']
            )
            print(f"Создана подписка: {sub_data['user'].username} - {sub_data['tariff'].name}")

        # Создаем заказы
        from products.models import Order, ProductOrder

        orders_data = [
            {
                'customer': users[0],
                'products': [
                    {'product': products[0], 'quantity': 1},  # iPhone
                    {'product': products[2], 'quantity': 2},  # AirPods
                ]
            },
            {
                'customer': users[1],
                'products': [
                    {'product': products[1], 'quantity': 1},  # MacBook
                    {'product': products[4], 'quantity': 1},  # Apple Watch
                ]
            },
            {
                'customer': users[2],
                'products': [
                    {'product': products[5], 'quantity': 1},  # Samsung
                    {'product': products[6], 'quantity': 1},  # Sony headphones
                    {'product': products[9], 'quantity': 2},  # Nintendo Switch
                ]
            },
            {
                'customer': users[0],
                'products': [
                    {'product': products[3], 'quantity': 1},  # iPad
                    {'product': products[7], 'quantity': 1},  # Xiaomi vacuum
                ]
            }
        ]

        for order_data in orders_data:
            # Создаем заказ
            order = Order.objects.create(
                customer=order_data['customer'],
                total_amount=0  # Будет рассчитано автоматически
            )

            # Добавляем продукты в заказ
            total_amount = 0
            for product_item in order_data['products']:
                product = product_item['product']
                quantity = product_item['quantity']

                ProductOrder.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

                # Рассчитываем общую сумму
                total_amount += product.price * quantity

            # Обновляем общую сумму заказа
            order.total_amount = total_amount
            order.save()

            print(f"Создан заказ #{order.id} для {order_data['customer'].username}")
            print(f"  Продукты: {[f'{p.product.name} x{p.quantity}' for p in order.order_with_products.all()]}")
            print(f"  Общая сумма: {order.total_amount} руб.")

        print("\n" + "=" * 50)
        print("Тестовые данные успешно созданы!")
        print("=" * 50)
        print(f"Пользователей: {User.objects.count()}")
        print(f"Продуктов: {Product.objects.count()}")
        print(f"Тарифов: {Tariff.objects.count()}")
        print(f"Подписок: {UserSubscription.objects.count()}")
        print(f"Заказов: {Order.objects.count()}")
        print("=" * 50)


if __name__ == "__main__":
    populate_test_data()