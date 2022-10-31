# Option-simulator
An option trading simulator for beginners in stock market
The simulator uses API from Firstock stock broker. Please open an account and obtain the API keys and vendor code to begin.
Please edit the wsgi.py file with your credentials. You will have to change the API key every 3 months as it expires.
I have used MySQL DB as SQLite was not good enough to handle the connections.
The 'optionchain' table in DB need to be populated in advance, please use dummy values for the 40 entries.

