{% extends "base.php" %}

{% block title %}Attendance Report{% endblock %}

{% block content %}
<div class="rounded-3xl border border-slate-700 bg-slate-900/80 p-6 shadow-glow md:p-8">
    <div class="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
            <p class="text-xs font-semibold uppercase tracking-[0.25em] text-sky-300">Summary</p>
            <h1 class="mt-2 text-3xl font-bold text-white">Attendance Report</h1>
        </div>
        <a href="/admin/dashboard" class="inline-flex rounded-xl border border-slate-600 px-4 py-2 text-sm font-medium text-slate-100 transition hover:border-sky-400 hover:text-sky-300">Back to Dashboard</a>
    </div>

    <div class="overflow-x-auto rounded-2xl border border-slate-700 bg-slate-950/50">
        <table class="min-w-full divide-y divide-slate-700 text-left text-sm text-slate-200">
            <thead class="bg-slate-800/80 text-sky-300">
                <tr>
                    <th class="px-4 py-3 font-semibold">Month</th>
                    <th class="px-4 py-3 font-semibold">Records</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-slate-700 bg-slate-900/40">
                {% if report %}
                    {% for item in report %}
                    <tr>
                        <td class="px-4 py-3">{{ item.month }}</td>
                        <td class="px-4 py-3">{{ item.total }}</td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr>
                        <td colspan="2" class="px-4 py-6 text-center text-slate-400">No attendance records available.</td>
                    </tr>
                {% endif %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
