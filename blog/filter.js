const search = document.querySelector('#search');
const buttons = [...document.querySelectorAll('[data-filter]')];
const stories = [...document.querySelectorAll('.story')];
const normalise = (value) => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
let sector = 'all';
const initial = new URLSearchParams(location.search).get('sector');
if (buttons.some(button => button.dataset.filter === initial)) sector = initial;
function update() {
  const query = normalise(search.value.trim());
  let count = 0;
  for (const story of stories) {
    story.hidden = !(sector === 'all' || story.dataset.sector === sector) || !normalise(story.dataset.search).includes(query);
    if (!story.hidden) count++;
  }
  for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.filter === sector));
  document.querySelector('#count').textContent = `${count} ${count === 1 ? 'artikel' : 'artikels'}`;
  document.querySelector('#empty').hidden = count > 0;
}
for (const button of buttons) button.addEventListener('click', () => { sector = button.dataset.filter; update(); });
search.addEventListener('input', update);
update();
