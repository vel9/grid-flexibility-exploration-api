This portfolio project is the backend for [Grid Exploration UI](https://github.com/vel9/grid-flexibility-exploration-ui)

It's an interactive version of "Resources Scheduled Day Ahead" chart of my data exploration [here](https://github.com/vel9/grid-flexibility-exploration/blob/main/HomeGridFlexibility.ipynb) - inspired by the flexible load profile discussion in Saul Griffith's *Electrify* (p.89).

It uses flask for REST APIs, queries Day Ahead prices from NYISO via [GridStatus](https://docs.gridstatus.io/en/latest/index.html) and finds optimal time/price windows for each resource.

It's a light-weight and simple backend that also contains fundamentals like:
* ORM (SQLAlchemy) for reading and writing from local sqlite3 database
* server-side validation
* unit tests, including external data source mocking