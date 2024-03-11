# World Bank API
A Python 2/3 wrapper for the World Bank API
See World Bank [Developer Information](https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information) to get information on the raw API


## Quickstart
```python
from worldbank import api as wb

summary, indicators = wb.Indicator.get()
summary, country_indicators = wb.CountryIndicator.get(indicators[0])
summary, countries = wb.Country.get()
summary, lending_types = wb.LendingType.get()
summary, topics = wb.Topic.get()
summary, sources = wb.Source.get()
summary, income_levels = wb.IncomeLevel.get()
summary, indicators = wb.Indicator.get()
summary, countries = wb.Country.by_income_level(income_level=income_levels[0])
summary, country = wb.Country.by_lending_type(lending_types[0])
summary, indicators = wb.Indicator.by_source(sources[0])
summary, indicators = wb.Indicator.by_topic(topics[0])
summary, country_indicators = wb.CountryIndicator.get(indicators[0])
```

Classes are used to store the data returned by the API and the `classmethods` and Instance Methods are used to fetch data from the API

* Catalog
* City
* Country
* CountryIndicator
* IncomeLevel
* Indicator
* LendingType
* Region
  * AdminRegion
* Source
* Topic

## Pagination
The API wrapper allows pagination and adjusting page sizes of data using the `page` number and `per_page` `number:
```python
from worldbank import api as wb

instances = []
current_page = 1
total_pages = float('inf')
total_instances = float('inf')
per_page = 500
while current_page <= total_pages:
    summary, page_instances = Indicator.get(page=current_page, per_page=per_page)
    total_pages = summary['pages']
    total_instances = summary['total']
    current_page += 1
    instances += page_instances
```
