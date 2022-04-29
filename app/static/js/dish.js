const recipeImage = document.querySelector('#recipe_image');
const screenMedia = window.matchMedia("(min-width: 576px)");

function changeLook(media) {
    if (screenMedia.matches) {
        recipeImage.classList.remove('d-flex', 'justify-content-sm-center');
    } else {
        recipeImage.classList.add('d-flex', 'justify-content-sm-center');
    }
}

changeLook(screenMedia) // Call listener function at run time
screenMedia.addEventListener('change', changeLook); // Attach listener function on state changes
