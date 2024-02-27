import asyncio

from infrastructure import mongo_setup
from services import package_service, user_service
from services.user_service import user_count


async def main():
    print_header()
    await mongo_setup.init_connection('pypi', 'user', 'password', 'admin')
    await summary()

    while True:
        print("[s] Show summary statistics")
        print("[f] Search the database for packages")
        print("[p] Most recently updated packages")
        print("[u] Create a new user")
        print("[r] Create a release")
        print("[x] Exit program")
        resp = input("Enter the character for your command: ").strip().lower()
        print('-' * 40)

        match resp:
            case 's':
                await summary()
            case 'f':
                await search_for_package()
            case 'p':
                await recently_updated()
            case 'u':
                await create_user()
            case 'r':
                await create_release()
            case 'x':
                break
            case _:
                print("Sorry, we don't understand that command.")

        print()  # give the output a little room each time.

    print('bye!')


def print_header():
    pad = 30
    print('/' + "-" * pad + '\\')
    print('|' + ' ' * pad + '|')
    print('|        PyPI CLI v1.0 ' + ' ' * (pad - 22) + '|')
    print('|' + ' ' * pad + '|')
    print('\\' + "-" * pad + '/')
    print()


async def summary():
    package_count = await package_service.package_count()
    release_count = await package_service.release_count()
    users_count = await user_service.user_count()

    print('PyPI Package Stats')
    print(f'Packages: {package_count:,}')
    print(f'Releases: {release_count:,}')
    print(f'Users: {users_count:,}')
    print()


async def search_for_package():
    pass


async def create_release():
    pass


async def create_user():
    pass


async def recently_updated():
    pass

if __name__ == '__main__':
    asyncio.run(main())