journeyplanner
==============

An innovative way of accomplishing journey planning with Megabus [Utilizing many algorithms from busapp]

<h1>Application</h1>
<p>journeyplanner is the backend for a frontend:<br><tr> <a href="http://www.megabusfinder.appspot.com">Here</a>

The application accomplishes extensible travel search capabilities for any desired route through
a large travel company called <a href="http://us.megabus.com">megabus</a>.  
</p>
<h1>The problem</h1>
<p>
<b>megabus</b> has all sorts of stops, nodes, that travel to each other, but they
only allow for the use to plan a trip from <b>one</b> node to it's <b>first degree</b> connections nodes.  
</p>
<h1>
An example
</h1>
<p> I'm trying to book travel from St. Louis, MO to Milwaukee, WI.  The closest first degree node
that St. Louis, MO has to Milwaukee, WI is Chicago, IL.  I as a user must book, and plan this trip from
St. Louis, MO to Chicago, IL in a tab.  In a parallel tab I must check out the trips from Chicago, IL to Milwaukee, IL
and make sure that the times are in accordance with one another acrosss these 2 tabs.  This number of tabs will
grow as hops grows.  Say you're going even farther from St. Louis, MO to Orlando, FL, for example.  To do this trip 
on megabus you have to go from St. Louis, MO to Memphis, TN; Memphis, TN to Atlanta, GA; Atlanta, GA to Orlando, FL
That's 3 open tabs comparing multiple times over maybe even multiple days.  Sounds like a headache, and it is!
This all assumes, of course, that the user knows as much about their routes as I do and knows that Memphis, TN
has a route to Atlanta, GA....
</p>

<h1>Solution</h1>
<p>
<a href="http://www.megabusfinder.appspot.com"><b>my app</b></a><br>
You can simply fill the form with St. Louis, MO and Milwaukee, WI as departure and arrival cities, respectively, and 
let the app do all the trip planning for you.  These cities are abitrary and the app works to connect any two cities
that megabus services via this user-friendly method.</p>

