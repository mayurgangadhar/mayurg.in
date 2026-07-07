---
layout: default
title: Notes
---

# 📚 Medical Library

<div class="card-grid">

{% assign sorted_notes = site.notes | sort: "title" %}

{% for note in sorted_notes %}

<a class="card" href="{{ note.url }}">

<h3>{{ note.title }}</h3>

<p>{{ note.subject }}</p>

</a>

{% endfor %}

</div>