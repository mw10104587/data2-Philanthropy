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

We extracted donor names and amounts from their annual report, by using an online service [pdftable](https://pdftables.com/), and turned them into a 42,955 rows csv file.


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


![Cross Giving Chart](story-use%20data/images/graph-3.png "")

*Institutions are along the circumference according to the percentage of board members who donated to them. Colored chords connecting two institutions represent reciprocal relationships (the institutions have donated to each other through their board members). Gray chords connecting two institutions represent non-reciprocal relationships (one institution gave to the other, but the other did not give back). Lincoln Center, 9/11 Memorial and Mets are the largest player in the backscratching game*



###Code

#####Python/Parse pdf to csv
[File](https://github.com/mw10104587/data2-Philanthropy/blob/master/Python/ParsePDF2CSV.py)

<pre lang="text"><code>python ParsePDF2CSV.py file.csv stackType Year Institution [Fund Type]</code></pre>

<p> We extract donors data with pdf table, and download excel from the website. Some times when the names of donors are long, like: Jackie Harris Hochberg and Robert J Hochberg, it often turns into two row.

|Donors                |
|----------------------|
|Jackie Harris Hochberg|
|and Robert J Hochberg |


We manually move the second half of the data back to the first row, for all of these long donor names, and use this ParsePDF2CSV.py file to make it a csv file, adding year, institution and fund type into the data, trying reduce manual effort for journalists.

|Year|Donor                   |Amount       |Type|Institution  |
|---:|-----------------------:|------------:|---:|------------:|
|2013|The Starr Foundation    |"$25,000,000"|    |9/11 Memorial|
|2013|Bank of America         |"$20,000,000"|    |9/11 Memorial|
|2013|Bloomberg Philanthropies|"$15,000,000"|    |9/11 Memorial|
|2013|JPMorgan Chase Co       |"$15,000,000"|    |9/11 Memorial|


This is a command line tool that tackles with three kind of format.

1. par: the amount donation of each donor is listed parrallel to the donors name
2. stack: the amount of donation of each donors is stacked on the same column
3. stack-with-fundtype: the amount of donation is stacked with donors, and the fund type is parrallel to donors list.


### Future Plan

1. Currently there are a lot of donors who donate together, like **Jackie Harris Hochberg and Robert J Hochberg**, but we still take them as one person. We plan to parse them and split them into different rows in the future.
2. Currently there are similar names for companies and people, we plan to implement Fuzzy String matching.
3. Visualize data into web portable format. (Now on Gephi)

