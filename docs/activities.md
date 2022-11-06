---
layout: main
index: 4
---

# Activities

## Publications

💠 The list of all publications can be downloaded
in the [Excel format](/download/publications.xlsx) 👍
or in the [CSV format](/download/publications.csv). 

{% assign current = "now" | date: "%Y" %}
{% for year in (2015..current) reversed %}
   {% include biblio.html year=year %}
{% endfor %}

