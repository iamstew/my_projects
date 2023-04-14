function changeTheme() {
    if (localStorage.getItem('theme') == 'dark') {
        localStorage.setItem('theme', 'light');
        document.body.classList.remove('dark-theme');
    } else if (localStorage.getItem('theme') == 'light') {
        localStorage.setItem('theme', 'dark');
        document.body.classList.add('dark-theme');
    }
}

if (localStorage.getItem('theme') == 'dark') {
    document.body.classList.add('dark-theme');
}
else if (localStorage.getItem('theme') == null) {
    localStorage.setItem('theme', 'light')
}
else if (localStorage.getItem('theme') == 'light') {
    document.body.classList.remove('dark-theme');
}