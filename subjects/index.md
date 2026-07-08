---
layout: default
title: Subjects
---
<section class="page-header">

<h1>

📚 Subjects

</h1>

<p>

Choose a subject to access theory and practical resources.

</p>

</section>

<div class="subjects-grid">

{% for subject in site.data.subjects %}

{% include subject-card.html subject=subject %}

{% endfor %}

</div>