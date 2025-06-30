function toggleTheme() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';

  html.setAttribute('data-theme', newTheme);

  const darkIcons = document.querySelectorAll('.dark-icon');
  const lightIcons = document.querySelectorAll('.light-icon')

  darkIcons.forEach(icon => {
    icon.classList.toggle('hidden', newTheme === 'dark');
  });

  lightIcons.forEach(icon => {
    icon.classList.toggle('hidden', newTheme === 'light');
  });
}
