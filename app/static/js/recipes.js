const dishName = document.querySelector("input[name='dish_name']");
const dishDescription = document.querySelector("textarea[name='dish_description']");
const dishInstructions = document.querySelector("textarea[name='dish_instructions']");
const dishImage = document.querySelector("input[name='dish_image']");
const imageError = document.querySelector('#image-error');
const submit = document.querySelector("input[name='submit']");


dishImage.addEventListener('change', () =>  {
    let imageSize = dishImage.files[0].size;

    if (imageSize > 1000000) {
        imageError.classList.remove('d-none');
        dishImage.classList.add('border', 'border-danger');
        submit.setAttribute('disabled', '');
    } else {
        imageError.classList.add('d-none');
        dishImage.classList.remove('border', 'border-danger');
        submit.removeAttribute('disabled');
    }
});


if (typeof(dishImage.files[0]) !== 'undefined') {
    submit.addEventListener('click', (e) => {
        e.preventDefault();
        let imageSize = dishImage.files[0].size; 
        if (imageSize > 1000000) {
            console.log('sorry file is too large');
        }
    });
} 

const dishNameOutput = document.querySelector('#dish-name-output');
const dishDescriptionOutput = document.querySelector('#dish-description-output');
const ingredientsOutput = document.querySelector('#ingredients-output');
const instructionsOutput = document.querySelector('#instructions-output');
const addCircleOutline = document.querySelector('#add_circle_outline');
const addCircleOutlineInstructions = document.querySelector('#add_circle_outline_instructions');
const taskAlt = document.querySelector('#task_alt');


let resetInputs = () => {
    document.querySelector("input[name='dish_ingredient_name']").value = '';
    document.querySelector("input[name='dish_measurement_type']").value = '';
    document.querySelector("select[name='dish_ingredient_whole_measurements']").value = '';
    document.querySelector("select[name='dish_ingredient_fraction_measurements']").value = '';
}


let restInputs2 = () => {
    document.querySelector("input[name='dish_name']").value = '';
    document.querySelector("textarea[name='dish_description']").value = '';
}

resetInputs();
restInputs2();
submit.setAttribute('disabled', true);

let new_recipe = {
    "Name": "",
    "Description": "",
    "Ingredients": [],
    "Instructions": [],
    "Image": ""
}


let validateInputs = () => {
    let inputs = [dishName, dishDescription];
    inputs.forEach(el => {
        if (el.value == "") {
            el.parentElement.appendChild(document.createElement('span'));
            el.parentElement.children[1].classList.add('text-danger');
            el.parentElement.children[1].innerHTML = `Please fill in missing input above.`;
        }
        else if (el.parentElement.contains(el.parentElement.children[1]) && el.value != "") {
            el.parentElement.children[1].remove();
        }
    });
}


let validateAll = () => {
    validateInputs();
    let inputs = [dishName, dishDescription];
    inputs.forEach(el => {
        if (el.value == "") {
            submit.setAttribute('disabled', true);
        } else {
            submit.removeAttribute('disabled');
        }
    });
}


dishName.addEventListener('change', () => {
    dishNameOutput.innerHTML = dishName.value;
});


dishDescription.addEventListener('change', () => {
    dishDescriptionOutput.innerHTML = dishDescription.value;
});


addCircleOutlineInstructions.addEventListener('click', () => {
    instructionsOutput.innerHTML += `
        <li class="mb-1 p-1 bg-light border rounded">${dishInstructions.value}
        <i class="bi bi-dash-circle text-danger fs-5 float-end" onclick="remove_item(this);"></i></li>`;
    dishInstructions.value = '';
});


addCircleOutline.addEventListener('click', () => {
    let fraction_value = document.querySelector("select[name='dish_ingredient_fraction_measurements']").value;
    let whole = document.querySelector("select[name='dish_ingredient_whole_measurements']").value;
    let unit = document.querySelector("input[name='dish_measurement_type']").value;
    let item = document.querySelector("input[name='dish_ingredient_name']").value;

    if (fraction_value !== "") {
        let splitted_fraction = fraction_value.split('');
        ingredientsOutput.innerHTML += `
        <li class="mb-1 p-1 bg-light border rounded">
            <span>${whole}</span>
            <sup>${splitted_fraction[0]}</sup>&frasl;<sub>${splitted_fraction[2]}</sub>
            <span>${unit}</span>
            <span>${item}</span>
            <i class="bi bi-dash-circle text-danger fs-5 float-end" onclick="remove_item(this);"></i>
            </li>`
    } else {
        ingredientsOutput.innerHTML += `
        <li class="mb-1 p-1 bg-light border rounded">
            <span>${whole}</span>
            <sup></sup><sub></sub>
            <span>${unit}</span>
            <span>${item}</span>
            <i class="bi bi-dash-circle text-danger fs-5 float-end" onclick="remove_item(this);"></i>
            </li>`
    }
    resetInputs();
});

let remove_item = (e) => e.parentElement.remove();

let sup_sub = (sup, sub) => {
    if (sup === "") {
        return "";
    }
    return `${sup}/${sub}`;
}

const parseData = () => {
    let ingredientsArr = Array.from(ingredientsOutput.children);
    let instructionsArr = Array.from(instructionsOutput.children);
    new_recipe["Name"] = dishName.value;
    new_recipe["Description"] = dishDescription.value;
    ingredientsArr.forEach(element => {
        let whole = element.children[0].textContent;
        let fraction = sup_sub(element.children[1].textContent, element.children[2].textContent);
        let unit = element.children[3].textContent;
        let item = element.children[4].textContent;
        
        new_recipe["Ingredients"].push(
            {
                "measurement": {
                    "whole": whole,
                    "fraction": fraction
                },
                "unit": unit,
                "item": item,
            }
        )
        
    });
    instructionsArr.forEach(element => {
        let step = element.textContent.split('\n')[0];
        new_recipe["Instructions"].push(step);
    });

    if (dishImage.value != '') {
        new_recipe["Image"] = dishImage.files[0]['name'];
    } else {
        new_recipe["Image"] = 'default.jpg';
    }

    return new_recipe;
}

let send_data;
taskAlt.addEventListener('click', (e) => {
    e.preventDefault();
    send_data = parseData();
    validateAll();
});


const make_recipe = async () => {
    const response = await fetch(`${window.origin}/recipes-page/recipe-maker`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(send_data),
      cache: "no-cache",
      headers: new Headers ({
      "content-type": "application/json"
      })
    });
    if (response.status !== 200) { throw new Error('Cannot fetch the data'); }  
    const data = await response.json().catch(err => console.log('rejected', err.message));
    console.log(data);

    const formData = new FormData()
    formData.append('imageFile', dishImage.files[0])
    const response_img = await fetch(`${window.origin}/recipes-page/recipe-maker`, {
        method: "POST", 
        body: formData
    });
    if (response_img.status !== 200) { throw new Error('Cannot fetch the data'); }  
    const data2 = await response_img.json().catch(err => console.log('rejected', err.message));

    let alert = document.querySelector("#dish-alert");
    alert.classList.remove('d-none');
    alert.innerHTML = data2.response;
    restInputs2();
}


submit.addEventListener('click', (e) => {
    e.preventDefault();
    make_recipe();
});
  