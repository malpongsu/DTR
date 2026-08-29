{% extends "base.php" %}

{% block title %}RFID Attendance{% endblock %}

{% block content %}
<div class="rounded-3xl border border-sky-500/20 bg-slate-900/60 p-6 shadow-glow md:p-8">
    <div class="mx-auto max-w-3xl">
        <div class="mb-8 text-center">
            <p class="text-xs font-semibold uppercase tracking-[0.25em] text-sky-300">Daily Time Record</p>
            <h1 class="mt-3 text-3xl font-bold text-white md:text-4xl">Dipolog Cathedral</h1>
            <p class="mt-2 text-slate-300">RFID Attendance System</p>
        </div>

        <form method="post" id="attendance-form" class="space-y-5">
            <div class="rounded-2xl border border-sky-400/20 bg-slate-950/70 p-5">
                <label for="rfid_reader" class="mb-3 block text-xs font-semibold uppercase tracking-[0.2em] text-sky-300">Listening</label>
                <input type="text" id="rfid_reader" name="rfid_number" class="w-full rounded-xl border border-sky-500/30 bg-slate-950 px-4 py-4 text-center text-lg font-semibold tracking-[0.2em] text-sky-300 outline-none placeholder:text-sky-400/60" value="" autocomplete="off" spellcheck="false" inputmode="numeric" autofocus placeholder="Listening for RFID..." readonly aria-readonly="true">
            </div>
        </form>
    </div>
</div>

<div class="mt-10 rounded-3xl border border-slate-700 bg-slate-900/60 p-6 shadow-xl shadow-slate-950/40">
    <h2 class="mb-4 text-xl font-semibold text-white">Recent Attendance</h2>
    <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-700 text-left text-sm text-slate-200">
            <thead class="bg-slate-800/80 text-sky-300">
                <tr>
                    <th class="px-4 py-3 font-semibold">Name</th>
                    <th class="px-4 py-3 font-semibold">RFID</th>
                    <th class="px-4 py-3 font-semibold">Timestamp</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-slate-700 bg-slate-900/40">
                {% if recent_attendance %}
                    {% for entry in recent_attendance %}
                    <tr>
                        <td class="px-4 py-3">{{ entry.name }}</td>
                        <td class="px-4 py-3">{{ entry.rfid_tag }}</td>
                        <td class="px-4 py-3">{{ entry.timestamp }}</td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr>
                        <td colspan="3" class="px-4 py-6 text-center text-slate-400">No attendance has been recorded yet.</td>
                    </tr>
                {% endif %}
            </tbody>
        </table>
    </div>
</div>

<script>
    const form = document.getElementById('attendance-form');
    const input = document.getElementById('rfid_reader');

    function focusRfidInput() {
        input.value = '';
        input.placeholder = 'Listening for RFID...';
        input.focus();
    }

    focusRfidInput();

    input.addEventListener('click', function () {
        focusRfidInput();
    });

    input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            const value = input.value.trim();
            input.value = '';
            if (!value) return;
            form.submit();
            return;
        }

        if (event.key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
            input.value = input.value + event.key;
        }
    });
</script>
{% endblock %}
