const emptyItems = document.querySelector('.empty-items');
let modalTitle = document.querySelector(".modal-title");
let modalBody = document.querySelector(".modal-body-first");
let genList = document.querySelector("#gen-prod-list");
const spinner = document.querySelector('#load');
const productList = document.querySelector('.product-list');
const detailsPane = document.querySelector('#details-pane');
const utilityBtn = document.querySelector('#utility-btn');

if (!numItems) { 
  emptyItems.classList.remove('empty-items');
  productList.classList.add('d-none');
}

genList.addEventListener('click', () => {
  spinner.classList.add('spinner-grow');
});

// spinner.style.display = 'none';

if (activateGen === true) {
  genList.classList.remove('disabled');
}

res.forEach((prod) => {
    let url_for = new URL(`/${prod.id}`, `${window.origin}`);

    document.querySelector("tbody").innerHTML += `
    <tr>
        <td><a href="${url_for}" type="button" class="text-decoration-none" data-bs-toggle="modal" data-bs-target="#staticBackdrop"
          onclick="modal(${prod.id});">${prod.product_name}</a></td>
        <td class="text-center">${prod.package_type}</td>
        <td class="text-center">${prod.quantity}</td>
        <td class="text-end"> ${level(prod.quantity, prod.min_quantity, prod.max_quantity)} </td>
    </tr>
    `
});


// (Callback function to modal async function) Show Modal when product is clicked
const showModal = (data) => {
    modalTitle.innerHTML = `${data.product_name}`

    modalBody.innerHTML = `
    <div class="d-flex flex-column">
        <dl class="row">
            <dt class="col-sm-6">Type:</dt>
            <dd class="col-sm-6">${data.product_type}</dd>
            <dt class="col-sm-6">Current Quantity:</dt>
            <dd class="col-sm-6">${data.quantity}</dd>
        </dl>
    </div>`;
};


//modal async function to request product object by id
//Call showModal function to render html
const modal = async (prodID) => {

  const response = await fetch(`${window.origin}/${prodID}`);
  const data = await response.json();

  return showModal(data);
}


const update_quantity = async () => {
  let modalTitle = document.querySelector(".modal-title");
  let quantityValue = document.querySelector("#qty-value");

  let entry = { 
    prod_name: modalTitle.textContent,
    qty_value: quantityValue.value
  };
  
  const response = await fetch(`${window.origin}/quantity-entry`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers ({
    "content-type": "application/json"
    })
  });

  if (response.status !== 200) { throw new Error('Cannot fetch the data'); }

  const data = await response.json().catch(err => console.log('rejected', err.message));

  thisProd = document.querySelectorAll('tr > td > a');

  thisProd.forEach((prod) => {
    if (data.product_name === prod.textContent) {
      prod.parentNode.parentNode.children[2].textContent = data.quantity;
      prod.parentNode.parentNode.children[2].nextElementSibling.innerHTML = level(data.quantity, data.min_quantity, data.max_quantity);
      
      // Update res object so html view is also updated.
      res.forEach(item => {
        if (item.product_name === data.product_name) {
          item.quantity = data.quantity;
        }
      });
    }
  });
}

// Search and filter products
const productsNode = document.querySelector('tbody');
const filterProducts = (term) => {
  Array.from(productsNode.children)
    .filter((product) => !product.textContent.toLowerCase().includes(term))
    .forEach((product) => product.classList.add('d-none'));

  Array.from(productsNode.children)
    .filter((product) => product.textContent.toLowerCase().includes(term))
    .forEach((product) => product.classList.remove('d-none'));
};

const search = document.querySelector('#search');
  search.addEventListener('keyup', ()  => {
    const term = search.value.trim();
    filterProducts(term);
  });

// Button for to show utility section
// utilityBtn.addEventListener('click', () => {
//   if (detailsPane.classList.contains('hide-utility-pane')) {
//     detailsPane.classList.remove('hide-utility-pane');
//     detailsPane.classList.add('show-utility-pane');
//   } else {
//     detailsPane.classList.add('hide-utility-pane');
//     detailsPane.classList.remove('show-utility-pane');
//   }
// });