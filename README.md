# Introduction

This project analyzes the electricity trades between European states and
evaluates the carbon density of the electric generation system with
networks and identify the communities in them.

The work is divided into two parts. In the first part, real data is used
to construct the networks. A comparison is made between the network
built using data from the years before COVID-19 (2017-2019) and the
network built using data from the COVID-19 period (2020). This
evaluation aims to assess the perturbations in the European electric
system (electricity production, carbon density, and other network
properties) caused by the virus.

I used this data also to analyze the current interdependencies between
states through a reinterpretation of the HITS algorithm.

In the second part of the project, a simulation is conducted to
reconstruct and reorganize the electricity mix of the European states by
eliminating the most polluting sources (coal, oil, gas). The goal is to
achieve a clean energy transition in 2050.

In the simulation, certain assumptions and approximations were made
regarding the future energy consumption of Europe and what would
constitute an acceptable energy mix for the countries. These hypotheses
and approximations will be thoroughly explained in the subsequent
sections.

# How to run the code

Code is written in python, you can execute the codes in the following
way:

        python3 FileName.py

To successfully run the code, the following libraries are required:

-   pandas

-   numpy

-   networkx

-   matplotlib

you can install them using pip:

        pip install networkx

if you don’t have pip you can install them with the following command
line:

        sudo apt-get install pip

# Networks of the current electric grid

The networks I have built have different features. The dimensions of the
nodes are proportional to the amount of electricity produced by each
state. The color of the nodes represents the carbon density of energy
production in each state, while the width of the links represents the
quantity of electric power that passes through the nodes.

I used different datasets to create these networks. In the "DataSets"
folder of the repository, you can find the raw files I worked on:
"Flow_graph_2017-19.txt" and "Flow_graph_2020.txt" contain the data on
power flows between states, which were used to create the links of the
networks ([1](https://www.energygraph.info)). The file "Electricity_Production_TWh.txt" contains the energy
production of each state (in TWh), which I used to set the dimensions of
the nodes ([2](https://www.kaggle.com/datasets/prateekmaj21/electricity-production-by-source-world)). The file "share-elec-produc-by-source.txt" provides the
contribution of each type of electricity generation for each state,
which I used to calculate the carbon density ([3](https://www.kaggle.com/datasets/donjoeml/energy-consumption-and-generation-in-the-globe)). I applied six different
colorations: green for a production level below 100 gCO2/kWh, light
green for a production level between 100-200 gCO2/kWh, yellow for a
production level between 200-300 gCO2/kWh, orange for a production level
between 300-400 gCO2/kWh, red for a production level between 400-500
gCO2/kWh, and brown for a production level above 600 gCO2/kWh. The
carbon intensity of each source of energy is taken from IPCC ([4](https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf#page=7)).

The "DataSet" folder contains only raw and processed files that can be
ignored for code execution. The relevant files are all located in the
main directory.

## Influence of the COVID-19 on the European electricity grid

By executing the "2017-19.py" and "2020.py" scripts, we can obtain the
first two networks of the project. These are weighted directed networks
where the links are created by calculating the total balance, which is
determined by the difference in electricity flowing through two nodes in
both directions.

The first script creates a network using data from the first week of
2017 to the last week of 2019, taking the mean values
(<a href="#fig:2017-19" data-reference-type="ref"
data-reference="fig:2017-19">1</a>). The second script uses data from
all weeks of 2020 to create another network
(<a href="#fig:2020" data-reference-type="ref"
data-reference="fig:2020">2</a>).

Link density of the first network is 0.054 and for the second network is
0.055. In all the graphs of the project have been identified the
communities thanks to the built-in function of NetworkX (they are been
identified using the Louvain method ([5](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.louvain.louvain_communities.html))), communities are logged to the
terminal by running the code.

<figure id="fig:2017-19">
<img src="2017-19.png" style="width:86.0%" />
<figcaption><span id="fig:2017-19" label="fig:2017-19"></span>Network of
the European electricity grid in the years 2017-2019, for a better
visualization run the code.</figcaption>
</figure>

<figure id="fig:2020">
<img src="2020.png" style="width:86.0%" />
<figcaption><span id="fig:2020" label="fig:2020"></span>Network of the
European electricity grid in the year 2020, for a better visualization
run the code.</figcaption>
</figure>

In the first network, representing the years 2017-2019, the total
production of energy is 5025.3 TWh, and the carbon density is 313.8
gCO2/kWh. In the second network, representing the year of the COVID-19
pandemic, the total production of energy is 4830.7 TWh, and the carbon
density is 279.3 gCO2/kWh. This indicates a reduction in total energy
production by 3.9% and a decrease in carbon density by 11.0%.

These observations suggest that during the year of the COVID-19
pandemic, there was a decrease in energy production and a reduction in
carbon intensity, possibly due to changes in energy consumption
patterns, economic activity, and environmental policies implemented
during that period. We can observe a relatively big reduction in carbon
density also because the two source of energy that can be easily
modulated and programmable are coal and gas, which are known for their
high carbon emissions.

## HITS algorithm

From the previous networks has been calculated the HITS algorithm that
it’s implemented on the library of NetworkX ([6](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.hits_alg.hits.html#hits)).

Hyperlink-Induced Topic Search (HITS; also known as hubs and
authorities) is a link analysis algorithm that rates Web pages, a good
hub represents a page that pointed to many other pages, while a good
authority represents a page that is linked by many different hubs. The
scheme assigns two scores for each page: its authority, which estimates
the value of the content of the page, and its hub value, which estimates
the value of its links to other pages.

Within this project, I have reinterpreted the meaning of the HITS
algorithm. Nodes with a high value of hubs indicate nodes that have a
surplus of electricity production, enabling them to export energy to
neighboring nodes. Instead, nodes with a high value of authorities
represent nodes with a deficit of electricity production, making them
highly dependent on other nodes for their energy supply.

The values of hits algorithm are in tables
(<a href="#tab:hits1719" data-reference-type="ref"
data-reference="tab:hits1719">1</a>) and
(<a href="#tab:hits2020" data-reference-type="ref"
data-reference="tab:hits2020">2</a>).

|     | Hubs  |     |     | Authorities |
|:---:|:-----:|:----|:---:|:-----------:|
| FRA | 0.326 |     | ITA |    0.307    |
| CHE | 0.272 |     | GBR |    0.113    |
| DEU | 0.154 |     | ESP |    0.110    |
| SVN | 0.076 |     | CHE |    0.108    |
| AUT | 0.042 |     | DEU |    0.081    |
| NLD | 0.042 |     | AUT |    0.071    |
| CZE | 0.037 |     | NLD |    0.061    |
| SWE | 0.013 |     | POL |    0.039    |
| NOR | 0.009 |     | BEL |    0.038    |
| BEL | 0.009 |     | CZE |    0.016    |
| POL | 0.004 |     | LUX |    0.016    |
| UKR | 0.003 |     | SVK |    0.011    |
| PRT | 0.003 |     | HUN |    0.007    |
| SVK | 0.003 |     | DNK |    0.007    |
| IRL | 0.002 |     | FIN |    0.006    |
| RUS | 0.002 |     | SVN |    0.006    |
| LTU | 0.002 |     | LTU |    0.001    |
| LVA | 0.000 |     | SWE |    0.001    |
| MNE | 0.000 |     | UKR |    0.000    |
| BLR | 0.000 |     | ROU |    0.000    |
| HRV | 0.000 |     | MDA |    0.000    |
| DNK | 0.000 |     | LVA |    0.000    |
| EST | 0.000 |     | BLR |    0.000    |
| HUN | 0.000 |     | ALB |    0.000    |
| GRC | 0.000 |     | HRV |    0.000    |
| BIH | 0.000 |     | RUS |    0.000    |
| SRB | 0.000 |     | MNE |    0.000    |
| BGR | 0.000 |     | SRB |    0.000    |
| ROU | 0.000 |     | MKD |    0.000    |
| ALB | 0.000 |     | BIH |    0.000    |
| TUR | 0.000 |     | GRC |    0.000    |
| MKD | 0.000 |     | TUR |    0.000    |
| ITA | 0.000 |     | BGR |    0.000    |
| FIN | 0.000 |     | IRL |    0.000    |
| ESP | 0.000 |     | MLT |    0.000    |
| GBR | 0.000 |     | FRA |    0.000    |
| LUX | 0.000 |     | EST |    0.000    |
| MDA | 0.000 |     | PRT |    0.000    |
| MLT | 0.000 |     | NOR |    0.000    |

Values of hubs and authorities of the nodes for the years before the
COVID-19 (2017-2019).

|     | Hubs  |     |     | Authorities |
|:---:|:-----:|:----|:---:|:-----------:|
| FRA | 0.393 |     | ITA |    0.386    |
| CHE | 0.292 |     | DEU |    0.153    |
| SVN | 0.061 |     | GBR |    0.140    |
| SWE | 0.048 |     | CHE |    0.094    |
| DEU | 0.043 |     | ESP |    0.073    |
| AUT | 0.034 |     | FIN |    0.032    |
| BEL | 0.032 |     | POL |    0.025    |
| NLD | 0.029 |     | AUT |    0.018    |
| DNK | 0.022 |     | BEL |    0.016    |
| MNE | 0.01  |     | CZE |    0.010    |
| CZE | 0.008 |     | HUN |    0.009    |
| IRL | 0.006 |     | LTU |    0.009    |
| NOR | 0.005 |     | DNK |    0.008    |
| RUS | 0.005 |     | HRV |    0.007    |
| SVK | 0.004 |     | LUX |    0.006    |
| UKR | 0.002 |     | SVN |    0.006    |
| LTU | 0.002 |     | SVK |    0.003    |
| POL | 0.001 |     | NLD |    0.002    |
| HUN | 0.001 |     | SWE |    0.001    |
| BLR | 0.001 |     | ALB |    0.001    |
| LVA | 0.000 |     | UKR |    0.001    |
| EST | 0.000 |     | ROU |    0.000    |
| BIH | 0.000 |     | SRB |    0.000    |
| BGR | 0.000 |     | LVA |    0.000    |
| SRB | 0.000 |     | BLR |    0.000    |
| ALB | 0.000 |     | MDA |    0.000    |
| HRV | 0.000 |     | MNE |    0.000    |
| MKD | 0.000 |     | MKD |    0.000    |
| ITA | 0.000 |     | RUS |    0.000    |
| TUR | 0.000 |     | GRC |    0.000    |
| ROU | 0.000 |     | TUR |    0.000    |
| GBR | 0.000 |     | BIH |    0.000    |
| GRC | 0.000 |     | MLT |    0.000    |
| LUX | 0.000 |     | IRL |    .000     |
| MDA | 0.000 |     | BGR |    0.000    |
| MLT | 0.000 |     | FRA |    0.000    |
| PRT | 0.000 |     | PRT |    0.000    |
| ESP | 0.000 |     | EST |    0.000    |
| FIN | 0.000 |     | NOR |    0.000    |

Values of hubs and authorities of the nodes on the year of the COVID-19
(2020).

## centrality measures

With this project we can determine also some centralities measures
running the file "unweighted_2017-19.py", thanks to this code we can
obtain a new weighted undirected graph in which links are created with
the sum of the electricty flows that passes through the nodes in both
directions (fig. <a href="#fig:unweighted" data-reference-type="ref"
data-reference="fig:unweighted">3</a>). I used the same dataset of
"2017-19.py" file.

Link density of this graph is 0.108 and also the total flux has been
calculated, the total flux of the electricity grid is 48.1 GW.

Communities are logged to the terminal by running the code.

<figure id="fig:unweighted">
<img src="unweighted.png" style="width:100.0%" />
<figcaption>Weighted undirected network of the European electric grid
that represent all the flow through the nodes (for a better
visualization run the code). </figcaption>
</figure>

The centralities that have been calculated are four: current flow
betweennes centrality (CFBC on table
<a href="#tab:centralities" data-reference-type="ref"
data-reference="tab:centralities">3</a>), edge current flow betweennes
centrality, current flow closeness centralities (CFCC on table
<a href="#tab:centralities" data-reference-type="ref"
data-reference="tab:centralities">3</a>), laplacian centralities (LC on
table <a href="#tab:centralities" data-reference-type="ref"
data-reference="tab:centralities">3</a>).

The current flow betweenness centrality (computed thanks to
corresponding NetworkX function ([7](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.current_low_betweenness_centrality.html#networkx.algorithms.centrality.current_flow_betweenness_centrality))) is calculated by measuring the amount
of current that passes through that node when electrical current is
injected at all possible source nodes and extracted at all possible sink
nodes in the network. The more current that flows through a node, the
higher its current flow betweenness centrality ([8](https://www.centiserver.org/centrality/Current-Flow_Betweenness_Centrality/)).

The edge current flow betweenness centrality (computed thanks to
corresponding NetworkX function ([9](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.edge_current_flow_betweenness_centrality.html#networkx.algorithms.centrality.edge_current_flow_betweenness_centrality))) has the same aim of the current flow
betweenness centrality but for the edges.

The current flow closeness (computed thanks to corresponding NetworkX
function ([10](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.current_flow_closeness_centrality.html#networkx.algorithms.centrality.current_flow_closeness_centrality))) centrality is variant of closeness centrality based on
effective resistance between nodes in a network. This metric is also
known as information centrality ([11](https://www.centiserver.org/centrality/Current-Flow_Closeness_Centrality/)).

|     | CFBC  |     |     |  CFCC   |     |     |  LC   |
|:---:|:-----:|:----|:---:|:-------:|:----|:---:|:-----:|
| DEU | 0.451 |     | DEU | 12431.9 |     | DEU | 0.483 |
| FRA | 0.281 |     | CHE | 11862.3 |     | FRA | 0.295 |
| ITA | 0.268 |     | AUT | 11808.6 |     | CHE | 0.288 |
| SWE | 0.238 |     | FRA | 11778.1 |     | AUT | 0.170 |
| HUN | 0.234 |     | ITA | 11652.6 |     | ITA | 0.167 |
| AUT | 0.191 |     | CZE | 11498.8 |     | NLD | 0.144 |
| UKR | 0.187 |     | NLD | 11305.9 |     | CZE | 0.136 |
| CHE | 0.172 |     | POL | 11018.2 |     | SWE | 0.117 |
| POL | 0.153 |     | HUN | 10956.5 |     | DNK | 0.092 |
| NLD | 0.151 |     | SWE | 10884.9 |     | ESP | 0.084 |
| SVK | 0.144 |     | SVK | 10804.1 |     | GBR | 0.075 |
| HRV | 0.143 |     | DNK | 10655.2 |     | POL | 0.074 |
| GRC | 0.143 |     | GBR | 10374.8 |     | BEL | 0.069 |
| CZE | 0.142 |     | BEL | 10325.5 |     | NOR | 0.065 |
| SRB | 0.138 |     | NOR | 10292.9 |     | FIN | 0.059 |
| FIN | 0.124 |     | SVN | 9967.9  |     | SVK | 0.050 |
| LTU | 0.119 |     | UKR | 9717.4  |     | HUN | 0.043 |
| DNK | 0.114 |     | ESP | 9712.4  |     | SVN | 0.032 |
| ROU | 0.110 |     | FIN | 9698.3  |     | LTU | 0.018 |
| SVN | 0.106 |     | HRV | 8953.1  |     | RUS | 0.018 |
| BGR | 0.103 |     | LTU | 8916.2  |     | LUX | 0.017 |
| NOR | 0.100 |     | RUS | 8725.4  |     | UKR | 0.016 |
| GBR | 0.097 |     | SRB | 8261.4  |     | PRT | 0.015 |
| RUS | 0.090 |     | ROU | 7820.8  |     | HRV | 0.013 |
| BIH | 0.074 |     | GRV | 7722.9  |     | GRC | 0.011 |
| BEL | 0.055 |     | BGR | 7623.9  |     | BGR | 0.009 |
| MNE | 0.055 |     | PRT | 7223.9  |     | SRB | 0.009 |
| ESP | 0.053 |     | EST | 6918.0  |     | ROU | 0.008 |
| MKD | 0.041 |     | LVA | 6682.3  |     | EST | 0.008 |
| ALB | 0.040 |     | BIH | 6620.9  |     | LVA | 0.005 |
| EST | 0.036 |     | MKD | 6420.2  |     | MKD | 0.005 |
| LVA | 0.033 |     | LUX | 5936.0  |     | BIH | 0.005 |
| BLR | 0.033 |     | MNE | 5736.7  |     | TUR | 0.004 |
| TUR | 0.022 |     | TUR | 5557.9  |     | MNE | 0.003 |
| LUX | 0.002 |     | BLR | 5416.1  |     | BLR | 0.003 |
| PRT | 0.000 |     | ALB | 5173.8  |     | IRL | 0.002 |
| IRL | 0.000 |     | IRL | 3995.7  |     | ALB | 0.002 |
| MDA | 0.000 |     | MDA | 1957.2  |     | MLT | 0.002 |
| MLT | 0.000 |     | MLT | 1899.7  |     | MDA | 0.001 |

Values of current flow betweenness centrality, current flow closeness
centrality and laplacian centrality of the network.

The Laplacian centralities (computed thanks to corresponding NetworkX
function ([12](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.laplacian_centrality.html#networkx.algorithms.centrality.laplacian_centrality))) provides insights into the overall influence or significance
of nodes in a network, nodes with high Laplacian centrality are those
that are well-connected to other nodes and have a high influence within
the network. They represent key positions that bridge different parts of
the network or act as connectors between communities ([13](https://www.centiserver.org/centrality/Laplacian_Centrality/)).

The values of the edge current flow betweenness centrality are not fully
reported in this relation because there are too many, the first four
edges are: SWE \<  − \>FIN=0.078, ITA \<  − \>FRA=0.075,
CHE \<  − \>DEU=0.074, ITA \<  − \>CHE=0.071.

By running the code, you will be able to view all the values that are
logged to the terminal.

# Simulation of the electricity grid in 2050

In the second part of the project, when running the file "Evolution.py,"
you will be able to observe an initial plot of the European grid. This
plot considers not the energy production of the states but rather the
energy consumption, taking into account electricity exchange through the
edges. Following this, a simulation presents a potential scenario
illustrating the transition towards greener electricity generation in
Europe. However, to proceed with the simulation, certain assumptions
must be made.

There are numerous scenarios regarding the electricity consumption of
Europe in 2050. In this project, I have chosen a median value that
assumes an increment of 40% in consumption for simplicity. For this
reason, the consumption of each state has been increased by this
percentage.

Subsequently, the coal, oil, and gas supply are eliminated, and the
deficit of each state is calculated, accounting for the increment in
consumption that each state needs to meet. In order to distribute the
new power required to fill this gap, two parameters are considered: the
PIL (Product of Internal Load) of the states and the closeness
centrality of the states, which is calculated on an undirected,
unweighted network of European links.

At this stage, we have identified surplus or deficit in electricity for
each state. The sum of all contributions is naturally zero. Prior to
simulating the creation of network links, adjustments are made to the
balance. A function is implemented to restrict states from importing
more than 5% of their own energy consumption and exporting more than 15%
(these values may seem small, but with the increase in consumption,
trade between states leads to a significant development of
interconnections).

Now, the algorithm for the propagation of electricity can begin,
creating the links of the network. The criteria are as follows: a state
with surplus energy supply exports a single unit of electricity (set at
100 W) to neighboring states experiencing a deficit. If there are no
neighbors with a deficit, the algorithm allows exporting to states that
don’t have a deficit, enabling them to export in subsequent iterations.
The algorithm runs recursively until all nodes in the network have a
neutral energy supply budget (fig
<a href="#fig:evo" data-reference-type="ref"
data-reference="fig:evo">4</a>).

<figure id="fig:evo">
<img src="evolution.png" style="width:100.0%" />
<figcaption>Network of the European electricity grid after the
simulation (for a better visualization run the code). </figcaption>
</figure>

The final step involves determining the energy sources that each state
needs to implement. Among the available technologies, solar energy, wind
energy, and nuclear energy are the only scalable and clean options.
Solar and wind energy are not programmable source, so without a storage
technologies that can satisfy the European need (today a technology that
can store this amount of energy doesn’t exist) we need to use also a
clean and programmable source like nuclear energy. Today Germany, which
have an amount of solar and wind near to 50%, starts to have some
problems in managing the stability of his electric grid and they starts
to need a quite big amount of storage technologies for his managing that
now are satisfied by gas and coal.

Based on these considerations, I propose that 50% of the energy mix be
met by solar and wind energy, while the remaining portion is fulfilled
by nuclear power. It is important to acknowledge that this is a
generalized approach, as each state may have varying conditions and
geographical characteristics that allow for a larger or smaller reliance
on solar and wind energy.

In Table <a href="#tab:GW" data-reference-type="ref"
data-reference="tab:GW">4</a>, you will find the power allocation and
total consumption for each state resulting from the simulation. If you
run the code, on the terminal are logged the weight of all the links of
the networks.

For the calculation of the new power I considered the mean capacity
factor in Europe for each energy source: 1 TWh for each GW of installed
solar capacity, 2.5 TWh for each GW of installed wind capacity, and 7.5
TWh for each GW of installed nuclear capacity. For the same reasons
mentioned before, these values are generalized, as each state may have
different characteristics. For instance, Italy may have a significant
amount of solar capacity but a smaller wind capacity, while the United
Kingdom may have a substantial wind capacity but a lower solar capacity.

Link density of the final graph is 0.054, communities are logged to the
terminal by running the code.

| Nation | Solar/Wind (GW) | Nuclear (GW) | Total consumption (TWh) |
|:------:|:---------------:|:------------:|:-----------------------:|
|  ALB   |    1.92-4.8     |     0.0      |          10.5           |
|  AUT   |   19.76-49.40   |     0.0      |          105.9          |
|  BIH   |    3.24-8.10    |     1.23     |          18.2           |
|  BEL   |   23.92-59.80   |     0.0      |          126.5          |
|  BGR   |   10.52-26.30   |     1.19     |          54.3           |
|  BLR   |   10.04-25.10   |     2.93     |          47.8           |
|  CHE   |   17.76344.40   |     0.0      |          92.3           |
|  CZE   |   21.80-54.50   |     2.05     |          101.9          |
|  DEU   |  84.04-210.10   |    52.01     |          817.0          |
|  DNK   |    3.08-7.70    |     2.23     |          49.6           |
|  EST   |    2.36-5.90    |     1.09     |          14.5           |
|  ESP   |  45.40-113.50   |    18.31     |          397.6          |
|  FIN   |   26.56-66.40   |     0.0      |          123.2          |
|  FRA   |  157.76-394.40  |     0.0      |          721.2          |
|  GBR   |  84.88-212.20   |     5.71     |          485.2          |
|  GRC   |   14.84-37.10   |     2.60     |          84.5           |
|  HRV   |   4.28-10.70    |     0.35     |          26.8           |
|  HUN   |   12.80-32.00   |     0.0      |          64.4           |
|  IRL   |   4.28-10.70    |     3.21     |          42.4           |
|  ITA   |  65.92-164.80   |    22.44     |          460.5          |
|  LTU   |    2.60-6.50    |     0.0      |          17.4           |
|  LUX   |    1.00-2.50    |     0.0      |           6.2           |
|  LVA   |    1.88-4.70    |     0.24     |          10.5           |
|  MDA   |    1.48-3.70    |     0.51     |           8.2           |
|  MNE   |    0.96-2.40    |     0.12     |           5.6           |
|  MKD   |    1.84-4.60    |     0.39     |          10.3           |
|  MLT   |    0.60-1.50    |     0.19     |           3.6           |
|  NLD   |   32.28-80.70   |     6.92     |          169.8          |
|  NOR   |  43.12-107.80   |     0.0      |          187.0          |
|  POL   |   37.88-94.70   |    17.44     |          242.8          |
|  PRT   |   12.08-30.20   |     2.15     |          77.5           |
|  ROU   |   15.44-38.60   |     1.03     |          85.6           |
|  SRB   |   10.20-25.50   |     1.67     |          50.0           |
|  RUS   |  260.64-651.60  |    66.64     |         1449.7          |
|  SWE   |  40.76-101.90   |     0.0      |          203.4          |
|  SVN   |    3.84-9.60    |     0.40     |          21.9           |
|  SVK   |   8.04-20.10    |     0.0      |          42.4           |
|  TUR   |  61.92-154.80   |    21.81     |          401.8          |
|  UKR   |   34.68-86.70   |     4.65     |          197.3          |

Values of current flow betweenness centrality, current flow closeness
centrality and laplacian centrality of the network.

# Conclusion

In this project, an analysis of the European power grid was conducted,
focusing on electricity exchanges between countries and evaluating
decarbonization scenarios. The analysis consisted of two distinct parts:
the first part utilized real data to construct networks and compare the
pre-COVID-19 (2017-2019) electricity network with the network during the
pandemic (2020) to assess the disruptions caused by the virus on the
European power system. The second part of the project involved
simulation to reconstruct and reorganize the energy mix of European
countries by phasing out the most polluting sources (coal, oil, gas) in
order to achieve a clean energy transition by 2050.

From the analysis of the networks constructed using real data, it was
observed that during the year of the COVID-19 pandemic, there was a 3.9%
reduction in total energy production and an 11.0% decrease in carbon
intensity. This suggests that during the pandemic, there was a decline
in energy production and a reduction in carbon intensity.

The analysis using the HITS algorithm allowed for the identification of
nodes with electricity surplus (hubs) and nodes with electricity deficit
(authorities). This information can be useful in understanding the
interdependencies among European countries and the role of each node in
the power grid.

In the simulation of a clean energy transition, certain assumptions and
approximations were made regarding future energy production and the
acceptable energy mix for European countries. The results of the
simulation will provide insights into how to reorganize electricity in
Europe to reduce environmental impact and achieve decarbonization goals
by 2050.

In conclusion, this project provides an in-depth analysis of electricity
exchanges among European countries, assessing the impact of the COVID-19
pandemic on the power system and proposing clean energy transition
scenarios. This information can be evaluate for policy decisions and
future strategies in managing and optimizing the European power system,
promoting greater sustainability and reducing carbon emissions.
