# data2-Philanthropy

This is a project about 20 Cultural Institutions' philanthropy data in New York City. We tried to find out the cross giving, which a board member of museum A donates to museum B, and the board member of museum B donates back. The project is initiated in the class of Mark Hansen's data II in Columbia University. 

<h3>Data</h3>
We collected the data from the following 20 Institutions, said to be the richest institutions based on ranking by Crain’s New York.

- Carnegie Hall 
- Lincoln Center
- Met
- Met Opera
- MoMA
- Philharmonic
- Amnh
- Art and Design
- Brooklyn Public Library
- Frick
- New York Public Library 
- 911 memorial
- Cooper Hewitt/Smithsonian
- New York Transit Museum 
- The Morgan Library and Museum
- WNET (Thirteen, WLIW, etc.)
- 92 Street Y
- Roundabout Theatre Company
- WNYC 
- Brooklyn Academy of Music

We extracted donor names and amounts from their annual report, by using an online service "pdftable", and turned them into a 42,955 rows csv file.


<h3>Tools</h3>
- R
- Python
- d3.js
- Gephi


<h3>Some Results</h3>

![Percentage of Board Member's donation](story-use%20data/images/bar-chart.jpg "Each bar represents the percentage of an institution's total donation income that was provided by other institution's board members.")

*Each bar represents the percentage of an institution's total donation income that was provided by other institution's board members.*

![Donors connections](story-use%20data/images/graph-1.png "")

*Each cluster represents an institution. The inner group of circles at the center of each institution represents the institution's board members. Blue arrows represent donations. The outer circles of each cluster represent the institution's most powerful donors. The red arrows call attention to donors who appear in multiple clusters--donors who donate to multiple institutions. This network shows how big each institution's donor network is and which institution's share similar donor bases*
