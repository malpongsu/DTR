{% extends "base.php" %}

{% block title %}Admin Login{% endblock %}

{% block content %}
<div class="flex min-h-[70vh] items-center justify-center">
    <div class="w-full max-w-md rounded-3xl border border-sky-500/20 bg-slate-900/80 p-8 shadow-glow">
        <div class="mb-6 text-center">
            <p class="text-xs font-semibold uppercase tracking-[0.25em] text-sky-300">Secure Access</p>
            <h3 class="mt-3 text-2xl font-bold text-white">Admin Login</h3>
        </div>
        <form method="post" class="space-y-5">
            <div>
                <label for="username" class="mb-2 block text-sm font-medium text-slate-200">Username</label>
                <input type="text" id="username" name="username" class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-sky-400" required>
            </div>
            <div>
                <label for="password" class="mb-2 block text-sm font-medium text-slate-200">Password</label>
                <input type="password" id="password" name="password" class="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-sky-400" required>
            </div>
            <button type="submit" class="w-full rounded-xl bg-sky-500 px-4 py-3 text-base font-semibold text-slate-950 transition hover:bg-sky-400">Login</button>
        </form>
    </div>
</div>
{% endblock %}
