from urlparse import urljoin
from ckan.lib.base import config


def get_sitemap_url():
    s3_url = config.get('ckanext.geodatagov.s3sitemap.aws_s3_url', 'https://filestore.data.gov/')
    s3_path = config.get('ckanext.geodatagov.s3sitemap.aws_storage_path', 'gsa/catalog-next/sitemap/')
    
    return urljoin(s3_url, s3_path, 'sitemap.xml')
    

