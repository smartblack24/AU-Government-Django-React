{% extends "mail_templated/base.tpl" %}

{% block subject %}
{{ invoice.matter.name }}
{% endblock %}

{% block body %}
{{ invoice.matter.description }}
{% endblock %}
