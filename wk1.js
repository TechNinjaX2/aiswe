document.querySelectorAll('.complete-btn').forEach(button => {
  button.addEventListener('click', () => {
    const card = button.closest('.course-card');
    card.classList.toggle('completed');

    button.textContent = card.classList.contains('completed')
      ? 'Completed ✅'
      : 'Mark as Completed';
  });
});

