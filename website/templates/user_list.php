{% extends "base.php" %}

{% block title %}
Master List
{% endblock %}

{% block content %}
<h1>Master List of Registered Users</h1> <br>

<!-- Table to display the Master List -->
<table border="1" cellpadding="10" cellspacing="0" style="width: 100%; text-align: center;">
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>RFID Tag Number</th>
            <th>Registration Date</th>
        </tr>
    </thead>
    <tbody>
        {% for user in users %}
        <tr>
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.rfid_tag }}</td>
            <td>{{ user.date_registered.strftime('%Y-%m-%d %H:%M:%S') }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

{% endblock %}
