const restore_btn = document.querySelector('#restore-btn');
const file_input = document.querySelector('#backupfileToRestore');

file_input.addEventListener('change', () => {
    restore_btn.classList.remove('disabled');
});

// if (file_input.value) {
//     restore_btn.classList.remove('disabled');
// }

// Toggle add item section