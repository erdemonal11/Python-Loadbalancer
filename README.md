The load balancer has 4 optional algorithms for load distribution. The menu 
algorithms are divided into 2 parts dynamic and static: 
Statics: 
• Round-Robin: This is the simplest algorithm to just give each server a 
request one by one repeatedly. 
• Weighted-Round-Robin: This algorithm requires the servers to have 
weights defined in the load balancer. It gives each server as many 
requests as their weights one by one repeatedly. 
Dynamics: 
• Weighted-Response-Time: This is the most powerful algorithm the 
load balancer possesses, it returns the location of the server with the 
least response time. 
• Weighted-Least-Connection: This algorithm takes into account the 
current number of active connections to each server. Servers with 
fewer active connections are preferred for new requests. 

LOAD BALANCER 
The load balancer has a client socket always ready and listening, any client 
connected to this socket is given a location of a server which is returned by a 
function in the load balancer. This determines_Server function determine 
the next server according to the current algorithm of the load balancer. A 
response time dictionary with Server object instances as keys and response 
times (float) as values contains each response time for each server. 
Weighted-Response-Time algorithm works according to this dictionary. A 
server weights dictionary with Server object instances as keys and weights 
(integers) as values contains each weight value for each server. Weighted
Round-Robin algorithm works according to this dictionary. All server 
instances are kept in a list in the load balancer, for round robin and weighted 
round robin, an internal server index counter and weight counter 
are being used. A load balancer can listen to its servers to determine if a 
server is dead or alive. A server notifies the user when it has requested a 
computation and of its leave and notifies it again when the computation is completed.If the Weighted-Response-Time algorithm is being used, then the 
load balancer will also automatically detect each dead server by a 5-second 
timeout and remove them from the servers list. If the Weighted-Least
Connection algorithm is being used, then the load balancer will also detect 
the connections of each server and direct the next connection to the server 
that has the least connection number.

CLIENT 
The client's connection is handled by its class' connect() method. It takes 
ip(str), port(int), and lb(boolean) arguments, and if lb = True, then the client 
will request a server location and call connect() again with this new 
location, but this time as lb=False. When lb = False, then the client will ask 
an input from the user to determine what type of request to make to the 
server. 
3 types of requests are available: 
• Request the server's dictionary with the format {"file name" : "file 
type"}. 
• Request a file from the user with the filename taken as input from the 
user and download it to the local machine. 
• Request a computation that takes an integer value from the user and 
puts the server to sleep for as many seconds as that input value 
If at any point, a request is not successful and/or the server does not 
respond, the client will automatically turn back to the load balancer and 
ask for another server's location. 

SERVER 
The server is always listening but does not make a direct connection with the 
load balancer except to test response times. If a request is met successfully, then the socket is closed and set ready for the next 
connection. To send Tuple, List, and Dict type of data through the sockets, 
JSON.dumps() and JSON.loads() methods are used to serialize and de
serialize the data, respectively. All connection protocols are of TCP since 
there is no room for mistakes with the file transactions.

PLAYGROUND 
In the playground class, there is an input for several servers available 
between [1-50] and as many servers are instantiated and registered to the 
load balancer at the beginning. There can be one or more clients 
initiated but giving input from all clients would require execution in different 
command panels. All these clients and server and load balancer 
instances are run on different threads since committing a socket's listen() 
method would freeze the command panel and require more than one panel 
to monitor and operate.

How to run the Project? 
Running the playground.py file will be sufficient to test the project, 
connection information and input feedback will be more than enough to direct 
the user.

![image](https://github.com/erdemonal11/Python-Loadbalancer/assets/137915983/a9c60e0a-e4f4-46c2-bf74-e50e700e4d9d)
