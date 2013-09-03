# stdlib
import argparse

# artisan
from artisan import Artisan


def console():
    """
    Parse arguments and create new Artisan instance
    """
    parser = argparse.ArgumentParser(
        description='Start web server using passed directory and port'
    )
    parser.add_argument(
        'method',
        help='directory to serve from',
        type=str,
        choices=['craft', 'ship']
    )
    args = parser.parse_args()

    # Run program
    artisan = Artisan()
    return getattr(artisan, args.method)()


# Do not run if imported
if __name__ == '__main__':
    console()
