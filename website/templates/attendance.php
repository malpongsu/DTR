{% extends "base.php" %}

{% block title %}
Attendance List
{% endblock %}

{% block content %}
<h1>Dipolog Cathedral Attendance</h1>
<h2>DAILY TIME RECORD</h2>
<h3>For the month of {{ month_start.strftime('%m/%d/%Y') }} - {{ month_end.strftime('%m/%d/%Y') }}</h3> <br>

<!-- Attendance Table -->
<table border="1" cellpadding="10" cellspacing="0" style="width: 100%; text-align: center;">
    <thead>
        <tr>
            <th>Date</th>
            <th>IN</th>
        </tr>
    </thead>
    <tbody>
        <!-- Loop through each day of the month -->
        {% for day in range(1, 32) %}
        <tr>
            <td>{{ day }}</td> <!-- Date -->
            <td>
                <!-- Check if there is an attendance record for this day -->
                {% set attendance_record = attendance_list | selectattr('date', 'equalto', month_start.replace(day=day)) | first %}
                {% if attendance_record %}
                    {{ attendance_record.time_in.strftime('%H:%M:%S') }} <!-- Display IN Time -->
                {% else %}
                    <!-- Placeholder for empty records -->
                    <input type="text" name="time_in_{{ day }}" placeholder="Enter Time" />
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<!-- Placeholder for Name entry -->
<h3>NAME: ________________________________</h3>

{% endblock %}
