const recipesList = document.querySelector('#recipes-list');
const deleteModalLabel = document.querySelector('#deleteModalLabel');
const deleteRecipeButton = document.querySelector('#deleteRecipeButton');
const deleteModal = document.querySelector('#deleteModal');
const modalDialog = document.querySelector('.modal-dialog');
const alertMsg = document.querySelector('div[role=alert]');


const updateScreen = (msg) => {
    deleteModal.classList.remove('show');
    deleteModal.removeAttribute('role');
    deleteModal.removeAttribute('aria-modal');
    deleteModal.setAttribute('aria-hidden', 'true');
    document.querySelector('body').classList.remove('modal-open');
    alertMsg.classList.remove('d-none');
    alertMsg.textContent = msg;
}

recipesList.addEventListener('click', e => {
    const dish_element = e.target.offsetParent.parentElement
    const dish_name = e.target.textContent;

    deleteModalLabel.textContent = `Delete ${e.target.textContent}?`;
    deleteRecipeButton.addEventListener('click', () => {
        deleteRecipe(dish_name);
        updateScreen(`${dish_name} has been removed!`);
        dish_element.remove();
    });
});


const deleteRecipe = async (dishName) => {
    let entry = {dish_name: dishName};

    const response = await fetch(`${window.origin}/delete-recipe`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers ({
        "content-type": "application/json"
        })
    });

    if (response.status !== 200) { throw new Error('Cannot fetch the data'); }
}