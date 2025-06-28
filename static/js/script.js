function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length == 2) return parts.pop().split(";").shift();
}

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

if (getCookie("theme") === "dark")
  document.documentElement.setAttribute('data-theme', 'dark');
else
  document.documentElement.setAttribute('data-theme', 'light');

