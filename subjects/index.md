---
layout: default
title: Subjects
---

# 📚 Subjects

<div class="card-grid">

{% for subject in site.data.subjects %}

<a class="card"
   href="/subjects/{{ subject.id }}/">

{{ subject.icon }}

{{ subject.name }}

</a>

{% endfor %}

</div>