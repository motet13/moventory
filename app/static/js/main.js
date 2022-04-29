// set, reset, and grab new elements and return it 
const setElements = () => {
    let table_body = document.querySelector("tbody");
    let new_table_body = document.createElement("tbody");
    return {table_body, new_table_body};
}

// HTML Template for products a table
const insertHTML = (incoming, len, el) => {
    let base = `${window.origin}`;
    incoming.forEach((obj) => {
        let url_for = new URL(`/index/${obj.id}`, base);
        el.innerHTML += `
        <tr>
            <td><a href="${url_for}" type="button" class="text-decoration-none"
                data-bs-toggle="modal" data-bs-target="#staticBackdrop"
                onclick="modal(${obj.id});">${obj.product_name}</a></td>
            <td class="text-center">${obj.package_type}</td>
            <td class="text-center">${obj.quantity}</td>
            <td class="text-end">${level(obj.quantity, obj.min_quantity, obj.max_quantity)}</td>
        </tr>
        `
    })
    return el;
}

// Construct and insert html in browser
const view = (returnedData) => {
    let el = setElements();
    insertHTML(returnedData, returnedData.length, el.new_table_body)
    el.table_body.parentNode.replaceChild(el.new_table_body, el.table_body);
}

// For some reason sort functions only works on FIREFOX Browser
// sort by packages
const sortPackage = () => view(res.sort((a, b) => a.package_type.toUpperCase() > b.package_type.toUpperCase()));
// sort by names
const sortName = () => view(res.sort((a, b) => a.product_name.toUpperCase() > b.product_name.toUpperCase()));
// sort by quantity
const sortQuantity = () => view(res.sort((a, b) => a.quantity - b.quantity));

// FETCH the searched data requested from server
async function submit_entry() {
    let search = document.getElementById("search");
    let table_body = document.querySelector("tbody");
    let new_table_body = document.createElement("tbody");
    let entry = { search: search.value };

    if (entry.search !== "") {
        const response = await fetch(`${window.origin}/search-entry`, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(entry),
            cache: "no-cache",
            headers: new Headers ({
            "content-type": "application/json"
            })
        });

        if (response.status !== 200) {
            throw new Error('Cannot fetch the data');
        }

        const data = await response.json().catch(err => console.log('rejected', err.message));
        let base = `${window.origin}`;
        let url_for = new URL(`/index/${data.id}`, base);
 
        new_table_body.innerHTML += `
        <tr>
            <td><a href="${url_for}" type="button" class="text-decoration-none" data-bs-toggle="modal" data-bs-target="#staticBackdrop"
            onclick="modal(${data.id});">${data.product_name}</a></td>
            <td class="text-center">${data.package_type}</td>
            <td class="text-center">${data.quantity}</td>
            <td class="text-end">${level(data.quantity, data.min_quantity, data.max_quantity)}</td>
        </tr>
        `
        table_body.parentNode.replaceChild(new_table_body, table_body);
    }
}

// Add active class on current page nav-link
const nav_link = document.querySelectorAll('.nav-link');

nav_link.forEach(item => {
    if (document.URL === item.href) {
        item.classList.add('active');
    }
});