{% extends "base.php" %}

{% block title %}
Add User
{% endblock %}

{% block content %}
<h1>Register New User for RFID</h1><br>

<!-- Form for adding a new user -->
<form action="/add_user" method="POST">
    <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" class="form-control" placeholder="Enter user's name" required>
    </div>

    <div class="form-group">
        <label for="rfid_tag">RFID Tag Number:</label>
        <input type="text" id="rfid_tag" name="rfid_tag" class="form-control" placeholder="Enter RFID tag number" required>
    </div>

    <button type="submit" class="btn btn-primary">Register User</button>
</form>

{% endblock %}
