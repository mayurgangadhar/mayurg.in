---
layout: default
title: Home
---

<section class="hero">

    <h1>Medical Resources</h1>

    <p>
        Organized study material for Final Year MBBS students.
        Theory notes, practical resources and previous papers in one place.
    </p>

    <a class="hero-button" href="/subjects/">
        Browse Subjects →
    </a>

</section>

<section class="subjects-preview">

    <h2>Subjects</h2>

    <div class="subject-grid">

        {% for subject in site.data.subjects %}

        <a class="subject-card" href="/subjects/{{ subject.id }}/">

            <div class="subject-icon">

                {{ subject.icon }}

            </div>

            <h3>{{ subject.name }}</h3>

        </a>

        {% endfor %}

    </div>

</section>