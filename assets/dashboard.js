const searchInput = document.getElementById('searchInput');
const cards = Array.from(document.querySelectorAll('.intel-card'));
const buttons = Array.from(document.querySelectorAll('[data-filter]'));
function applyFilters(){
  const query = (searchInput?.value || '').toLowerCase().trim();
  const active = document.querySelector('[data-filter].active')?.dataset.filter || 'all';
  cards.forEach(card => {
    const text = card.innerText.toLowerCase();
    const tags = card.dataset.tags || '';
    const okQuery = !query || text.includes(query) || tags.includes(query);
    const okFilter = active === 'all' || tags.includes(active);
    card.style.display = okQuery && okFilter ? '' : 'none';
  });
}
if(searchInput) searchInput.addEventListener('input', applyFilters);
buttons.forEach(button => button.addEventListener('click', () => { buttons.forEach(b => b.classList.remove('active')); button.classList.add('active'); applyFilters(); }));
