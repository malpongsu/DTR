{% extends "base.php" %}
{% block title %}
Dipolog Cathedral Attendance
{% endblock %}

{% block content %}
<h1>Attendance Tracking</h1>

<!-- Form for RFID attendance entry -->
<form action="/" method="POST">
  <div class="form-group">
    <label for="rfidNumber">Enter RFID Number:</label>
    <input type="text" id="rfidNumber" name="rfid_number" class="form-control" placeholder="Enter RFID number" required>
  </div>
  
</form>

{% endblock %}


