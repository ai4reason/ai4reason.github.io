---
layout: ML
index: 40
---

# Activities

## Publications

{% assign current = "now" | date: "%Y" %}
{% for year in (2015..current) reversed %}
   {% include biblio.html year=year %}
{% endfor %}

