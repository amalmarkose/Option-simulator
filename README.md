# Option-simulator
An option trading simulator for beginners in stock market to trade Nifty weekly and monthly options.

The simulator uses API from Firstock stock broker. Please open an account and obtain the API keys and vendor code to begin.
Please edit the wsgi.py file with your credentials. You will have to change the API key every 3 months as it expires.
I have used MySQL DB as SQLite was not good enough to handle the connections.
The 'optionchain' table in DB need to be populated in advance WITH 40 rows, please use dummy values for the 40 entries.
The option chain will not fetch by default but only after the user hover over the option chain div. This was done to reduce load on DB.
Manually enter the expiry date when creating new trade in the format '03NOV22'.

Please use the name 'options' for the virtualenv. A startserver.bat file is provided to reduce the hustle of starting up the server. Please do the needed changes in the paths and you are good to go.

Please note to run with 'Debug=True' as I have used static files. No copyrighted contents are used in this project.

Happy trading!

Main page.

![image](https://user-images.githubusercontent.com/40312761/198940851-c411819b-2195-4a11-89fe-9eff70fe421b.png)

All active trades.

![image](https://user-images.githubusercontent.com/40312761/198941043-585c0d63-fcd2-4b9e-9746-31f590cd6cc2.png)

Archives.

![image](https://user-images.githubusercontent.com/40312761/198941242-b9b43259-1681-4211-8918-c4d790c2d782.png)

New trade.

![image](https://user-images.githubusercontent.com/40312761/198941458-1000e8bd-727c-4fa5-a6cf-099cde3778e5.png)

