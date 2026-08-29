{% extends "base.php" %}

{% block title %}Admin Dashboard{% endblock %}

{% block content %}
<div class="rounded-3xl border border-slate-700 bg-slate-900/80 p-6 shadow-glow md:p-8">
    <div class="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
            <p class="text-xs font-semibold uppercase tracking-[0.25em] text-sky-300">Operations Center</p>
            <h1 class="mt-2 text-3xl font-bold text-white">Admin Dashboard</h1>
        </div>
        <a href="/admin/logout" class="inline-flex rounded-xl border border-slate-600 px-4 py-2 text-sm font-medium text-slate-100 transition hover:border-sky-400 hover:text-sky-300">Logout</a>
    </div>

    <div class="mb-8 grid gap-4 md:grid-cols-3">
        <div class="rounded-2xl border border-slate-700 bg-slate-950/60 p-5">
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-sky-300">Total Users</p>
            <h2 class="mt-3 text-3xl font-bold text-white">{{ total_users }}</h2>
        </div>
        <div class="rounded-2xl border border-slate-700 bg-slate-950/60 p-5">
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-sky-300">Monthly Attendance</p>
            <h2 class="mt-3 text-3xl font-bold text-white">{{ total_records }}</h2>
        </div>
        <div class="rounded-2xl border border-slate-700 bg-slate-950/60 p-5">
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-sky-300">Monthly Report</p>
            <a href="/admin/report" class="mt-3 inline-flex rounded-lg bg-sky-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-sky-400">View Report</a>
        </div>
    </div>

    <div class="mb-8 rounded-2xl border border-slate-700 bg-slate-950/50 p-5">
        <h4 class="mb-4 text-xl font-semibold text-white">Register User</h4>
        <form method="post" class="grid gap-3 md:grid-cols-[1.2fr_1.2fr_0.6fr]">
            <input type="text" name="name" class="rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none focus:border-sky-400" placeholder="Full name" required>
            <input type="text" name="rfid_tag" class="rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none focus:border-sky-400" placeholder="RFID tag" required>
            <button type="submit" class="rounded-xl bg-emerald-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-emerald-400">Add</button>
        </form>
    </div>

    <div class="rounded-2xl border border-slate-700 bg-slate-950/50 p-5">
        <h4 class="mb-4 text-xl font-semibold text-white">Registered Users</h4>
        <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-slate-700 text-left text-sm text-slate-200">
                <thead class="bg-slate-800/80 text-sky-300">
                    <tr>
                        <th class="px-4 py-3 font-semibold">ID</th>
                        <th class="px-4 py-3 font-semibold">Name</th>
                        <th class="px-4 py-3 font-semibold">RFID Tag</th>
                        <th class="px-4 py-3 font-semibold">Created</th>
                        <th class="px-4 py-3 font-semibold">Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-700 bg-slate-900/40">
                    {% for user in users %}
                    <tr>
                        <td class="px-4 py-3">{{ user.id }}</td>
                        <td class="px-4 py-3">{{ user.name }}</td>
                        <td class="px-4 py-3">{{ user.rfid_tag }}</td>
                        <td class="px-4 py-3">{{ user.created_at }}</td>
                        <td class="px-4 py-3">
                            <div class="flex flex-col gap-2 md:flex-row">
                                <form method="post" action="/admin/users/{{ user.id }}/edit" class="flex flex-col gap-2">
                                    <input type="text" name="name" value="{{ user.name }}" class="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 outline-none focus:border-sky-400" required>
                                    <input type="text" name="rfid_tag" value="{{ user.rfid_tag }}" class="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 outline-none focus:border-sky-400" required>
                                    <button type="submit" class="rounded-lg bg-amber-400 px-3 py-2 text-sm font-semibold text-slate-950 hover:bg-amber-300">Update</button>
                                </form>
                                <form method="post" action="/admin/users/{{ user.id }}/delete">
                                    <button type="submit" class="mt-2 rounded-lg bg-red-500 px-3 py-2 text-sm font-semibold text-white hover:bg-red-400" onclick="return confirm('Delete this user?')">Delete</button>
                                </form>
                            </div>
                        </td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="5" class="px-4 py-6 text-center text-slate-400">No users registered yet.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
