<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {
                theme: {
                    extend: {
                        colors: {
                            ink: '#081722',
                            panel: '#0f1f2d',
                            panelAlt: '#13293d',
                            accent: '#38bdf8',
                            accentSoft: '#a5f3fc',
                            success: '#22c55e',
                            warning: '#f59e0b',
                            danger: '#ef4444'
                        },
                        boxShadow: {
                            glow: '0 0 0 1px rgba(56,189,248,0.25), 0 20px 40px rgba(8, 23, 34, 0.45)'
                        }
                    }
                }
            }
        </script>
        <title>{% block title %}Dipolog Cathedral Attendance{% endblock %}</title>
    </head>
    <body class="min-h-screen bg-slate-950 text-slate-100 antialiased">
        <nav class="border-b border-sky-500/20 bg-slate-950/80 backdrop-blur">
            <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div class="flex h-16 items-center justify-between">
                    <a href="/" class="text-lg font-bold tracking-wide text-white">DTR System</a>
                    <button class="inline-flex items-center rounded-md border border-slate-700 p-2 text-slate-200 md:hidden" type="button" data-toggle="collapse" data-target="#navbar">
                        <span class="sr-only">Open navigation</span>
                        <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                    <div class="hidden items-center space-x-2 md:flex">
                        <a class="rounded-lg px-3 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-800 hover:text-sky-300" href="/">Home</a>
                        <a class="rounded-lg px-3 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-800 hover:text-sky-300" href="/attendance">Attendance</a>
                        <!-- <a class="rounded-lg px-3 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-800 hover:text-sky-300" href="/add-user">Register RFID</a> -->
                        <a class="rounded-lg px-3 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-800 hover:text-sky-300" href="/user-list">Master List</a>
                        <a class="rounded-lg px-3 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-800 hover:text-sky-300" href="/admin/login">Admin Login</a>
                        {% if session.get('admin_logged_in') %}
                        <a class="rounded-lg px-3 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-800 hover:text-sky-300" href="/admin/dashboard">Dashboard</a>
                        <a class="rounded-lg px-3 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-800 hover:text-sky-300" href="/admin/logout">Logout</a>
                        {% endif %}
                    </div>
                </div>
                <div class="collapse md:hidden" id="navbar">
                    <div class="space-y-2 pb-4 pt-2">
                        <a class="block rounded-lg px-3 py-2 text-slate-200 hover:bg-slate-800" href="/">Home</a>
                        <a class="block rounded-lg px-3 py-2 text-slate-200 hover:bg-slate-800" href="/attendance">Attendance</a>
                        <a class="block rounded-lg px-3 py-2 text-slate-200 hover:bg-slate-800" href="/add-user">Register RFID</a>
                        <a class="block rounded-lg px-3 py-2 text-slate-200 hover:bg-slate-800" href="/user-list">Master List</a>
                        <a class="block rounded-lg px-3 py-2 text-slate-200 hover:bg-slate-800" href="/admin/login">Admin Login</a>
                        {% if session.get('admin_logged_in') %}
                        <a class="block rounded-lg px-3 py-2 text-slate-200 hover:bg-slate-800" href="/admin/dashboard">Dashboard</a>
                        <a class="block rounded-lg px-3 py-2 text-slate-200 hover:bg-slate-800" href="/admin/logout">Logout</a>
                        {% endif %}
                    </div>
                </div>
            </div>
        </nav>

        <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="mb-4 rounded-xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-slate-100 shadow-lg" role="alert">
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            {% block content %}{% endblock %}
        </main>

        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" crossorigin="anonymous"></script>
        <script type="text/javascript" src="{{ url_for('static', filename='index.js') }}"></script>
    </body>
</html>
