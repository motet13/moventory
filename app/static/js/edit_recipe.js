const dishName = document.querySelector("input[name='dish_name']");
const dishDescription = document.querySelector("textarea[name='dish_description']");
const dishInstructions = document.querySelector("textarea[name='dish_instructions']");
const dishImage = document.querySelector("input[name='dish_image']");
const imageError = document.querySelector('#image-error');
const submit = document.querySelector("input[name='submit']");
const dishNameOutput = document.querySelector('#dish-name-output');
const dishDescriptionOutput = document.querySelector('#dish-description-output');
const ingredientsOutput = document.querySelector('#ingredients-output');
const instructionsOutput = document.querySelector('#instructions-output');
const addCircleOutline = document.querySelector('#add_circle_outline');
const addCircleOutlineInstructions = document.querySelector('#add_circle_outline_instructions');
const taskAlt = document.querySelector('#task_alt');
const img = document.querySelector('img');
let is_send_image_activated = false

console.log(response_data);

// functions & eventListeners
const remove_item = (e) => e.parentElement.remove();
const resetIngredientInputs = () => {
    document.querySelector("input[name='dish_ingredient_name']").value = '';
    document.querySelector("input[name='dish_measurement_type']").value = '';
    document.querySelector("select[name='dish_ingredient_whole_measurements']").value = '';
    document.querySelector("select[name='dish_ingredient_fraction_measurements']").value = '';
}

const resetNameDescriptionInputs = () => {
    document.querySelector("input[name='dish_name']").value = '';
    document.querySelector("textarea[name='dish_description']").value = '';
}

const validateInputs = () => {
    let inputs = [{"output": dishNameOutput, "input": dishName}, {"output": dishDescriptionOutput, "input": dishDescription}];
    inputs.forEach(el => {
        if (el.output.textContent == "") {
            el.input.classList.add('border', 'border-danger');
        }
        else {
            el.input.classList.remove('border', 'border-danger');
        }
    });
}

const validateAll = () => {
    if (response_data.Name == "" || response_data.Description == "") {
        submit.setAttribute('disabled', true);
        console.log(`Please fill in the red borders below`)
    } else {
        submit.removeAttribute('disabled');
    }
}

const sup_sub = (sup, sub) => {
    if (sup === "") {
        return "";
    }
    return `${sup}/${sub}`;
}


const filePreview = () => {
    const file = dishImage.files[0];
    const reader = new FileReader();
  
    reader.addEventListener('load', function () {
      // result is a base64 string
      img.src = reader.result;
    }, false);
  
    if (file) {
      reader.readAsDataURL(file);
      is_send_image_activated = true;
    }
}


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
        filePreview();
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


const parseData = () => {
    let ingredientsArr = Array.from(ingredientsOutput.children);
    let instructionsArr = Array.from(instructionsOutput.children);

    if (response_data.Name !== dishNameOutput.textContent) {
        response_data['New_Name'] = dishNameOutput.textContent;
    } else {
        response_data.Name = dishNameOutput.textContent;
    }
    
    response_data.Description = dishDescriptionOutput.textContent;
    response_data.Ingredients = [];
    response_data.Instructions = [];
    ingredientsArr.forEach(element => {
        let whole = element.children[0].textContent;
        let fraction = sup_sub(element.children[1].textContent, element.children[2].textContent);
        let unit = element.children[3].textContent;
        let item = element.children[4].textContent;
        
        response_data.Ingredients.push(
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
        response_data.Instructions.push(step);
    });
    return response_data;
}

let send_data;
taskAlt.addEventListener('click', (e) => {
    e.preventDefault();
    send_data = parseData();
    validateAll();
});

const ingredientOutputTemplate = (fraction, whole, unit, item) => {
    if (fraction) {
        let splitted_fraction = fraction.split('');
        return `
        <li class="mb-1 p-1 bg-light border rounded">
            <span>${whole}</span>
            <sup>${splitted_fraction[0]}</sup>&frasl;<sub>${splitted_fraction[2]}</sub>
            <span>${unit}</span>
            <span>${item}</span>
            <i class="bi bi-dash-circle text-danger fs-5 float-end" onclick="remove_item(this);"></i>
            </li>`
    } else {
        return `
        <li class="mb-1 p-1 bg-light border rounded">
            <span>${whole}</span>
            <sup></sup><sub></sub>
            <span>${unit}</span>
            <span>${item}</span>
            <i class="bi bi-dash-circle text-danger fs-5 float-end" onclick="remove_item(this);"></i>
            </li>`
    }
}

const instructionOutputTemplate = (val) => {
    return `
        <li class="mb-1 p-1 bg-light border rounded">${val}
        <i class="bi bi-dash-circle text-danger fs-5 float-end" onclick="remove_item(this);"></i>
        </li>`;
}

dishName.addEventListener('change', () => {
    dishNameOutput.innerHTML = dishName.value;
    validateInputs();
});

dishDescription.addEventListener('change', () => {
    dishDescriptionOutput.innerHTML = dishDescription.value;
    validateInputs();
});

addCircleOutline.addEventListener('click', () => {
    let fraction_value = document.querySelector("select[name='dish_ingredient_fraction_measurements']").value;
    let whole = document.querySelector("select[name='dish_ingredient_whole_measurements']").value;
    let unit = document.querySelector("input[name='dish_measurement_type']").value;
    let item = document.querySelector("input[name='dish_ingredient_name']").value;
    ingredientsOutput.innerHTML += ingredientOutputTemplate(fraction=fraction_value, whole=whole, unit=unit, item=item);
    resetIngredientInputs();
});

addCircleOutlineInstructions.addEventListener('click', () => {
    instructionsOutput.innerHTML += instructionOutputTemplate(val=dishInstructions.value);
    dishInstructions.value = '';
});


const edit_recipe = async () => {
    const response = await fetch(`${window.origin}/recipes-page/edit/${response_data.Name}`, {
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
    let alert = document.querySelector("#dish-alert");
    alert.classList.remove('d-none');
    alert.innerHTML = data.response;
}


const send_image = async () => {
    const formData = new FormData()
    formData.append('imageFile', dishImage.files[0])
    const response = await fetch(`${window.origin}/recipes-page/edit/image`, {
        method: "POST", 
        body: formData
    });
    if (response.status !== 200) { throw new Error('Cannot fetch the data'); }  
    const data = await response.json().catch(err => console.log('rejected', err.message));
}


submit.addEventListener('click', (e) => {
    e.preventDefault();
    edit_recipe();
    if (is_send_image_activated) {send_image();}
});




// Initial page - Output data on the edit page
dishName.value = response_data.Name;
dishDescription.value = response_data.Description;
submit.setAttribute('disabled', true);
dishNameOutput.innerHTML = response_data.Name;
dishDescriptionOutput.innerHTML = response_data.Description;
response_data.Ingredients.forEach(element => {
    let fraction_value = element.measurement.fraction
    let whole = element.measurement.whole
    let unit = element.unit
    let item = element.item
    ingredientsOutput.innerHTML += ingredientOutputTemplate(fraction=fraction_value, whole=whole, unit=unit, item=item);
});

response_data.Instructions.forEach(element => instructionsOutput.innerHTML += instructionOutputTemplate(val=element));