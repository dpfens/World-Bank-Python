"""
A Python wrapper for the WorldBank API (See: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information)
"""

from __future__ import unicode_literals
from __future__ import print_function
import logging
import json
import functools

try:
    # Python 3
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib2 import Request, urlopen
    from urllib import urlencode

logger = logging.getLogger(__name__)


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


def _request(url, **kwargs):
    headers = kwargs.get('headers', {})
    parameters = kwargs.get('parameters', {})
    data = kwargs.get('data', {})

    parameters.setdefault('format', 'json')

    encoded_parameters = urlencode(parameters)
    if encoded_parameters:
        url = '%s?%s' % (url, encoded_parameters)

    logger.debug(url)
    request = Request(url)
    for key, value in headers.items():
        request.add_header(key, value)

    for key, value in data.items():
        request.add_data(key, value)

    try:
        response = urlopen(request)
    except Exception as e:
        logger.error(e)
        raise
    raw_response_data = response.read().decode("utf-8")
    logger.debug(raw_response_data)
    response_data = json.loads(raw_response_data)
    return response_data


domain = "https://api.worldbank.org/v2"


class Source(object):
    """
    Sources of information for WorldBank data

    See https://datahelpdesk.worldbank.org/knowledgebase/articles/898587-api-catalog-source-queries
    """
    __slots__ = ('id', 'name', 'description', 'url')

    def __init__(self, id, name, description, url):
        self.id = id
        self.name = name
        self.description = description
        self.url = url

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%s, name=%s, url=%r>' % (self.__class__.__name__, id(self), self.id, self.name, self.url)

    @classmethod
    def from_api(cls, data):
        """
        Returns a class instance from API data
        """
        source_id = data['id']
        name = data.get('value', data.get('name', None))
        name = name.encode('ascii', 'ignore')
        description = data.get('description', None)
        url = data.get('url', None)
        return cls(source_id, name, description, url)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances
        """
        url = '%s/sources' % domain
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        return summary, instances


class IncomeLevel(object):
    """
    See https://datahelpdesk.worldbank.org/knowledgebase/articles/898596-api-income-level-queries
    """
    __slots__ = ('id', 'name')

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%s, code=%s, name=%s>' % (self.__class__.__name__, id(self), self.id, self.code, self.name)

    @classmethod
    def from_api(cls, data):
        """
        Returns a class instance from API data
        """
        income_level_id = data['id']
        name = data['value']
        return cls(income_level_id, name)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances
        """
        url = '%s/incomeLevels' % domain
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        return summary, instances


class LendingType(object):
    """
    See https://datahelpdesk.worldbank.org/knowledgebase/articles/898608-api-lending-type-queries
    """
    __slots__ = ('id', 'name')

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%s, name=%s>' % (self.__class__.__name__, id(self), self.id, self.name)

    @classmethod
    def from_api(cls, data):
        """
        Returns a class instance from API data
        """
        lending_type_id = data['id']
        name = data['value']
        return cls(lending_type_id, name)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances
        """
        url = '%s/lendingTypes' % domain
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        return summary, instances


class Indicator(object):
    """
    An Indicator is dimension that can be measured for a country
    See https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-api-indicator-queries
    """
    __slots__ = ('id', 'name', 'source', 'topics', 'source_note', 'source_organization')

    def __init__(self, id, name, source, topics, source_note, source_organization):
        self.id = id
        self.name = name
        self.source = source
        self.topics = topics
        self.source_note = source_note
        self.source_organization = source_organization

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%s, name=%s, source_organization=%s>' % (self.__class__.__name__, id(self), self.id, self.name, self.source_organization)

    @classmethod
    def from_api(cls, data):
        """
        Returns a class instance from API data
        """
        indicator_id = data['id']
        name = data['name'].encode('ascii', 'ignore')
        source_data = data.get('source', None)
        topic_data = data.get('topics', [])
        source_note = data.get('sourceNote', None)
        source_organization = data.get('sourceOrganization', None).encode('ascii', 'ignore')
        source = Source.from_api(source_data)
        topics = []
        for item in topic_data:
            if 'id' not in item:
                continue
            topic = Topic.from_api(item)
            topics.append(topic)
        return cls(indicator_id, name, source, topics, source_note, source_organization)

    @classmethod
    @memoize
    def get(cls, indicator_id=None, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances
        """
        if indicator_id:
            url = '%s/indicators/%s' % (domain, indicator_id)
        if not indicator_id:
            url = '%s/indicators' % domain
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        return summary, instances

    @classmethod
    def by_source(cls, source, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances with a given source
        """
        url = '%s/source/%s/indicator' % (domain, source.id)
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        return summary, instances

    @classmethod
    def by_topic(cls, topic, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances with a given topic
        """
        url = '%s/topic/%s/indicator' % (domain, topic.id)
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        return summary, instances


class Region(object):
    """
    A region is a property of a Country
    See https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-api-country-queries
    """
    __slots__ = ('id', 'code', 'name')

    def __init__(self, id, code, name):
        self.id = id
        self.code = code
        self.name = name

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s %s>' % (self.__class__.__name__, id(self), self.name)

    @classmethod
    def from_api(cls, data):
        """
        Returns a class instance from API data
        """
        id = data['id']
        code = data['iso2code']
        name = data['value']
        return cls(id, code, name)


class AdminRegion(Region):
    """
    An admin region is a property of a Country
    See https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-api-country-queries
    """

    __slots__ = ('id', 'code', 'name')


class City(object):
    """
    A city is a property of a Country
    ex. country.capital # <City instance>

    See https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-api-country-queries
    """
    __slots__ = ('name', 'latitude', 'longitude')

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s %s %s latitude=%s, longitude=%s>' % (self.__class__.__name__, id(self), self.name, self.latitude, self.longitude)

    @classmethod
    def from_api(cls, data):
        """
        Returns a class instance from API data
        """
        name = data['name']
        latitude = data['latitude']
        longitude = data['longitude']
        return cls(name, latitude, longitude)


class Country(object):
    """
    A country
    See https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-api-country-queries
    """
    __slots__ = ('id', 'name', 'iso_code', 'region', 'admin_region', 'income_level', 'lending_type', 'capital')

    def __init__(self, id, name, iso_code, region, admin_region, income_level, lending_type, capital):
        self.id = id
        self.name = name
        self.iso_code = iso_code
        self.region = region
        self.admin_region = admin_region
        self.income_level = income_level
        self.lending_type = lending_type
        self.capital = capital

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%s, iso_code=%s, name=%s, region=%s, capital=%s>' % (self.__class__.__name__, id(self), self.id, self.iso_code, self.name, self.region, self.capital)

    @classmethod
    def from_api(cls, data):
        """
        Returns a class instance from API data
        """
        country_id = data['id']
        name = data['name']
        iso_code = data.get('iso2Code', None)
        region_data = data.get('region', None)
        admin_region_data = data.get('adminregion', None)
        income_level_data = data.get('incomeLevel', None)
        lending_type_data = data.get('lendingType', None)
        capital_city = data.get('capitalCity', None)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        region = Region.from_api(region_data)
        admin_region = AdminRegion.from_api(admin_region_data)
        income_level = IncomeLevel.from_api(income_level_data)
        lending_type = LendingType.from_api(lending_type_data)
        capital = City(capital_city, latitude, longitude)
        return cls(country_id, name, iso_code, region, admin_region, income_level, lending_type, capital)

    @classmethod
    def get(cls, iso_code=None, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances
        """
        url = '%s/countries' % domain
        if iso_code:
            url = '%s/%s' % (url, iso_code)
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        return summary, instances

    @classmethod
    def by_income_level(cls, income_level, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances with a given income_level
        """
        url = '%s/countries' % domain
        kwargs.setdefault('incomeLevel', income_level.id)
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        return summary, instances

    @classmethod
    def by_lending_type(cls, lending_type, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances with a given lending_type
        """
        url = '%s/countries' % domain
        kwargs.setdefault('lendingType', lending_type.id)
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        return summary, instances


class CountryIndicator(object):
    """
    An instance of a measure of a country for a given year
    See https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-api-indicator-queries
    """
    __slots__ = ('indicator', 'country', 'year', 'value', 'decimal')

    def __init__(self, indicator, country, year, value, decimal):
        self.indicator = indicator
        self.country = country
        self.year = year
        self.value = value
        self.decimal = decimal

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '<%s %s country=%s, indicator=%s, year=%s, value=%s>' % (self.__class__.__name__, id(self), self.country, self.indicator, self.year, self.value)

    @classmethod
    def from_api(cls, data):
        """
        Returns a class instance from API data
        """
        country = data['country']
        indicator_data = data['indicator']
        indicator_summary, indicators = Indicator.get(indicator_data['id'])
        indicator = indicators[0]
        year = data['date']
        value = data['value']
        if value:
            value = float(value)
        decimal = data['decimal']
        return cls(indicator, country, year, value, decimal)

    @classmethod
    def get(cls, indicator, country=None, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances
        """
        start = kwargs.pop('start', None)
        end = kwargs.pop('end', None)
        date = kwargs.get('date', None)
        if start and end and not date:
            kwargs.setdefault('%s:%s' % (start, end), None)

        if country:
            iso_code = country.iso_code
        else:
            iso_code = 'all'
        url = '%s/countries/%s/indicators/%s' % (domain, iso_code, indicator.id)
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        if country:
            for instance in instances:
                instance.country = country
        return summary, instances


class Topic(object):
    """
    A Topic that a given indicator may have
    See https://datahelpdesk.worldbank.org/knowledgebase/articles/898611-api-topic-queries
    """
    __slots__ = ('id', 'name', 'note')

    def __init__(self, id, name, note):
        self.id = id
        self.name = name
        self.note = note

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%s, name=%s>' % (self.__class__.__name__, id(self), self.id, self.name)

    @classmethod
    def from_api(cls, data):
        """
        Returns a class instance from API data
        """
        topic_id = data['id']
        name = data['value']
        note = data.get('sourceNote', None)
        return cls(topic_id, name, note)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a tuple of a dictionary summary, and a list of class instances
        """
        url = '%s/topics/' % domain
        summary, data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data]
        return summary, instances


class Catalog(object):
    """
    A Dataset in the World Bank Open Data Datalog

    See https://datahelpdesk.worldbank.org/knowledgebase/articles/902049-data-catalog-api
    """

    def __init__(self, id, **kwargs):
        self.id = id
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%s>' % (self.__class__.__name__, id(self), self.id)

    @classmethod
    def from_api(cls, data):
        """
        Returns a class instance from API data
        """
        catalog_id = data['id']
        metatypes = data['metatype']
        metadata = {}
        for metatype in metatypes:
            metadata[metatype['id']] = metatype['value']
        return cls(catalog_id, **metadata)

    @classmethod
    def get(cls, catalog=None, field=[], **kwargs):
        """
        Returns a dictionary with a list of class instances
        """
        field = ';'.join(field)
        url = '%s/datacatalog/' % domain
        if catalog:
            url = '%s/%s' % (url, catalog.id)
        if field:
            url = '%s/metatypes/%s' % (url, field)
        data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data['datacatalog']]
        return instances

    @classmethod
    def search(cls, query, **kwargs):
        """
        Returns a list of class matching the query
        """
        url = '%s/v2/datacatalog/search/%s' % (domain, query)
        data = _request(url, parameters=kwargs)
        instances = [cls.from_api(item) for item in data['datacatalog']]
        return instances


if __name__ == '__main__':
    summary, indicators = Indicator.get()
    summary, country_indicators = CountryIndicator.get(indicators[0])
    summary, countries = Country.get()
    summary, lending_types = LendingType.get()
    summary, topics = Topic.get()
    summary, sources = Source.get()
    summary, income_levels = IncomeLevel.get()
    summary, indicators = Indicator.get()
    summary, countries = Country.by_income_level(income_level=income_levels[0])
    summary, country = Country.by_lending_type(lending_types[0])
    summary, indicators = Indicator.by_source(sources[0])
    summary, indicators = Indicator.by_topic(topics[0])
    summary, countryindicators = CountryIndicator.get(indicators[0])
    catalog = Catalog.get()
