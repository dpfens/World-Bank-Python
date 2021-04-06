# World Bank API
A Python 2/3 wrapper for the World Bank API
See World Bank [Developer Information](https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information) to get information on the raw API

## Classes
Classes are used to store the data returned by the API and the `classmethods` and Instance Methods are used to fetch data from the API

- [Catalog](#catalog)
- [City](#city)
- [Country](#country)
- [CountryIndicator](#countryindicator)
- [IncomeLevel](#incomelevel)
- [Indicator](#indicator)
- [LendingType](#lendingtype)
- [Region](#region)
    - [AdminRegion](#adminregion)
- [Source](#source)
- [Topic](#topic)


### Catalog
The Data Catalog API provides programmatic access to the list of datasets in the [World Bank’s Open Data Catalog](https://data.worldbank.org/data-catalog/) with associated metadata.  Each metatype returned is added to the instance as an attribute.

#### Instance Attributes
- id

See [World Bank Catalog API](https://datahelpdesk.worldbank.org/knowledgebase/articles/902049-data-catalog-api) for more details

### City
A city in a [country](#country). A `country`'s `capital` is a `City` instance

#### Instance Attributes
- name
- latitude
- longitude

#### Instance Methods
- get(page=1, per_page=50]

### Country
A country existing in the World Bank database

#### Instance Attributes
- id
- name
- iso_code
- region - a [Region](#region) instance
- admin_region - an [AdminRegion](#adminregion) instance
- income_level - an [IncomeLevel](#incomelevel) instance
- lending_type - a [LendingType](#lendingtype) instance
- capital - A [City](#city) instance

#### Instance Methods
- get(iso_code=None, page=1, per_page=50]
    - If an iso_code is not provided, returns a list of all [Countries](#country).  If an iso_code is provided, returns a [Country](#country) instance of the given iso_code.
- by_income_level(income_level]
    - Returns [Countries](#country) that all have a given [IncomeLevel](#incomelevel)
- by_lending_type(lending_type]
    - Returns [Countries](#country) that all have a given [LendingType](#lendingtype)

See the [World Bank Country API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-api-country-queries) for more details

### CountryIndicator
A measure of an [Indicator](#indicator) for a given country for a given year

#### Instance Attributes
- Indicator - an instance of an [Indicator](#indicator)
- country
    - id
    - name
- year - year when the measure of the indicator occurred
- value - floating point number
- decimal - a measure of precision of the returned value

#### Instance Methods
- get(indicator, country='all', page=1, per_page=50, start=None, end=None]
    - Returns instances of `CountryIndicator` for a given [Indicator](#indicator).  If a `start` year and `end` year are provided, returns `CountryIndicators` where `start` >= year <= `end`.
    - If a country is provided, only returns `CountryIndicators` for the given country. If a country is not provided, returns `CountryIndicators` for the [Indicator](#indicator) for all countries.

See the [World Bank Indicator API](See https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-api-indicator-queries) for more details


### IncomeLevel
Income levels show the income category of a particular country as identified by the World Bank.  For more information see the [World Bank Country and Lending Groups](https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups) page.

#### Instance Attributes
- id
- name

#### Instance Methods
- get(page=1, per_page=50]
    - Returns a list of all [IncomeLevels](#incomelevel)

See the [World Bank Income Level API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898596-api-income-level-queries) for more details.

### Indicator

#### Instance Attributes
- id
- name
- source - A [Source](#source) instance
- topics - A list of [Topics](#topic)
- source_note - a description of the indicator by the `source_organization`
- source_organization - The name of the organization providing the data for the indicator

#### Instance Methods
- get(indicator_id=None, page=1, per_page=50]
    - If a indicator_id is provided, returns a single [Indicator](#indicator).  If an indicator_id is not provided, then all [Indicators](#indicator) will be returned based on the `page` and `per_page` parameter
- by_source(source, page=1, per_page=50]
    - Returns [Indicators](#indicator) that all come from the [Source](#source)
- by_topic(topic]
    - Returns [Indicators](#indicator) that all have a given [Topic](#topic)

See the [World Bank Indicator API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-api-indicator-queries) for more details.

### LendingType
The World Bank classified countries according to the type of lending they are eligible for through the World Bank.  For more information see the [World Bank Country and Lending Groups](https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups) page.

#### Instance Attributes
- id
- name

#### Instance Methods
- get(page=1, per_page=50]
    - Returns a list of all [LendingTypes](#lendingtypes)

See the [World Bank Lending Type API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898608-api-lending-type-queries) for more details

### Region

#### Instance Attributes
- id
- name

#### AdminRegion

#### Instance Attributes
- id
- name

### Source
An organization that provides data as [CountryIndicators](#countryindicator) for a given number of [Indicators](#indicator)

#### Instance Attributes
- id
- name
- description
- url

#### Instance Methods
- get(page=1, per_page=50]
    - Returns a list of all [Sources](#source)

See the [World Bank Source API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898587-api-catalog-source-queries) for more details

### Topic
A high-level category that all [Indicators](#indicator) are mapped to

#### Instance Attributes
- id
- name
- note

#### Instance Methods
- get(page=1, per_page=50]
    - Returns a list of all [Topics](#topic)

See the [World Bank Topic API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898611-api-topic-queries) for more details
