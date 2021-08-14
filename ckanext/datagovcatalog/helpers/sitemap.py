from future import standard_library
standard_library.install_aliases()

import os

from urllib.parse import urljoin
from ckan.lib.base import config


def get_sitemap_url():
    s3_url = config.get('ckanext.geodatagov.s3sitemap.aws_s3_url', 'https://filestore.data.gov/')
    s3_path = config.get('ckanext.geodatagov.s3sitemap.aws_storage_path', 'gsa/catalog-next/sitemap/')

    return urljoin(s3_url, s3_path + 'sitemap.xml')


def create_sitemap_url():
    robot_txt = ("User-agent: *\nDisallow: /dataset/rate/\nDisallow: /revision/\n"
                 "Disallow: /dataset/*/history\nDisallow: /api/\nCrawl-Delay: 10\n"
                 "Sitemap: %s"
                 % get_sitemap_url())

    path = os.path.dirname(os.path.abspath(__file__)) + '/../public/robots.txt'
    with open(path, "w+") as robot_file:
        robot_file.write(robot_txt)
