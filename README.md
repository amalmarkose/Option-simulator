# Option-simulator
An option trading simulator for beginners in stock market
The simulator uses API from Firstock stock broker. Please open an account and obtain the API keys and vendor code to begin.
Please edit the wsgi.py file with your credentials. You will have to change the API key every 3 months as it expires.
I have used MySQL DB as SQLite was not good enough to handle the connections.
The 'optionchain' table in DB need to be populated in advance, please use dummy values for the 40 entries.

Main page.

![image](https://user-images.githubusercontent.com/40312761/198940851-c411819b-2195-4a11-89fe-9eff70fe421b.png)

All active trades.

![image](https://user-images.githubusercontent.com/40312761/198941043-585c0d63-fcd2-4b9e-9746-31f590cd6cc2.png)

Archives.

![image](https://user-images.githubusercontent.com/40312761/198941242-b9b43259-1681-4211-8918-c4d790c2d782.png)

New trade.

![image](https://user-images.githubusercontent.com/40312761/198941458-1000e8bd-727c-4fa5-a6cf-099cde3778e5.png)

