// Define a function to perform changes based on the content of an input field
function perform_content_changes() {
    // Get the value of the input field with ID "id_content"
    let data = $('#id_content').val();

    // Attempt to parse the data as JSON
    try {
        // Parse the JSON data and replace single quotes with double quotes
        let json_data = JSON.parse(data.substring(1, data.length - 1).replace(/'/g, '"'));
        
        // Remove the existing content div
        $('#Contentcustom-content').remove();
        
        // Load new content based on the parsed JSON data
        load_content('Content', '#id_content', '#content-container');
    } catch (error) {
        // Handle any errors if JSON parsing fails
    }
}
// Define a function to perform changes based on the content of an input field
function perform_form_changes() {
    // Get the value of the input field with ID "id_content"
    let data = $('#id_form').val();

    // Attempt to parse the data as JSON
    try {
        // Parse the JSON data and replace single quotes with double quotes
        let json_data = JSON.parse(data.substring(1, data.length - 1).replace(/'/g, '"'));
        
        // Remove the existing content div
        $('#Formcustom-content').remove();
        
        // Load new content based on the parsed JSON data
        load_content('Form', '#id_form', '#form-container');
    } catch (error) {
        // Handle any errors if JSON parsing fails
    }
}

// Define a function to load content based on JSON data
function load_content(field_name, id_reference, container_id) {
    // Check if the container element exists
    if ($(container_id).length == 0) {
        // Create a new container div if it doesn't exist
        let container = document.createElement('div');
        container.id = container_id.substring(1 , container_id.length);
        // Create a private container for the field name and a button
        let private_container = document.createElement('div');
        private_container.id = container_id.substring(1 , container_id.length) + "-private";
        $('#content').append(container);
        $('#content').append(private_container);
    }
    // deleting "" in the container_id
    container_id = container_id.substring(1, container_id.length);


    // Get the value of the input field with the given ID
    let data = $(id_reference).val();
    // get the outer container of the card 
    let outer_container = document.getElementById(container_id);
    outer_container.classList.add('card', 'card-body', 'col-12', 'col-lg-9');
    // Check if the private container is empty
    if (document.getElementById(container_id + '-private').childElementCount == 0) {
        // get the private container
        let private_container = document.getElementById(container_id + '-private');
        // Create a container for the field name and a button
        let name_button_container = document.createElement('div');
        name_button_container.classList.add('row', 'container');
        name_button_container.style.justifyContent = 'space-between';
        // Create a name element for the field
        let container_name = document.createElement('h2');
        container_name.innerHTML = field_name;
        container_name.style.fontWeight = 'bold';
        // Append the name element to the container
        name_button_container.appendChild(container_name);
        // check if this form is change form or not
        if (change) {
             // Create a button to add new content
            let button = document.createElement('button');
            button.classList.add('btn', 'btn-primary');
            button.innerHTML = 'Add ' + field_name;

            // Add an onclick event handler to the button
            button.onclick = function () {

                // Prompt the user to enter the name of the new content
                let new_content = prompt('Enter the name of the new ' + field_name);
                if (new_content == null) {
                    return;
                }

                // Get the data from the input field
                let data = $(id_reference).val();
                // Parse the JSON data and check if the new content already exists
                let json_data = JSON.parse(data.substring(1, data.length - 1).replace(/'/g, '"'));
                if (new_content in json_data) {
                    alert('This ' + field_name + ' already exists');
                    return;
                }

                // Add the new content to the JSON data and update the input field value
                // Check if the field is a form or not
                if (field_name == 'Form') {
                    // Handle the adding of new form content
                    $('#Formcustom-content').remove();
                    // Check if the form is an input, checkbox, or radio
                    if ($('#form-selection').val() == 'input') {
                        json_data[new_content] = '';
                    } else {
                        json_data[new_content] = [$('#form-selection').val() , {}];
                    }
                    // Convert the JSON data to a string and update the input field value
                    let to_save_data = JSON.stringify(json_data);
                    to_save_data = to_save_data.replace(/"/g, "'");
                    $(id_reference).val(`"${to_save_data}"`);
                    console.log(json_data)
                    load_content('Form', '#id_form', '#form-container');
                }else {
                    // Handle the adding of new content
                    json_data[new_content] = [];
                    // Convert the JSON data to a string and update the input field value
                    let to_save_data = JSON.stringify(json_data);
                    to_save_data = to_save_data.replace(/"/g, "'");
                    $(id_reference).val(`"${to_save_data}"`);
                    $('#Contentcustom-content').remove();
                    load_content('Content', '#id_content', '#content-container');
                }

            }
            // if is form add selection to select the added form type
            if (field_name == 'Form') {
                // Create a selection element for the form type
                let button_selection_container = document.createElement('div');
                // Create a selection element for the form type
                let selection = document.createElement('select');
                selection.id = 'form-selection';
                // Create options for the selection element
                let options = ['input' , 'checkbox' , 'radio'];
                // Add the options to the selection element
                for (let op in options) {
                    let option = document.createElement('option');
                    option.innerHTML = options[op];
                    selection.appendChild(option);
                }
                button.classList.add('ml-4');
                selection.classList.add('mr-4');
                button_selection_container.appendChild(selection);
                button_selection_container.appendChild(button) 
                name_button_container.appendChild(button_selection_container);
            }else {
                // Append the button and container name to the container
                let button_selection_container = document.createElement('div');
                button_selection_container.appendChild(button) 
                name_button_container.appendChild(button_selection_container);
            }
        }
        // Append the button and container name to the private container
        private_container.appendChild(name_button_container);
        // Append the private container to the outer container
        outer_container.appendChild(private_container);
    }
    // Create a container for the content
    let container = document.createElement('div');
    container.id = field_name + 'custom-content';
    outer_container.appendChild(container);
    // Check if the data is null
    if (data == 'null') {
        $(id_reference).val('"{}"');
        data = '"{}"';
    }
    // Check if the data is empty
    // load the content
    let json_data = JSON.parse(data.substring(1, data.length - 1).replace(/'/g, '"'));
    // Loop through the JSON data and add elements to the container
    for (let key in json_data) {
        // Create a container for the name and delete button
        let name_container = document.createElement('div');
        name_container.classList.add('container', 'row', 'mt-2');

        // Create a name element for the key
        let name = document.createElement('h5');
        let delete_button = document.createElement('i');
        delete_button.className = 'fas fa-times ml-2';
        delete_button.style.color = 'red';
        delete_button.style.fontSize = '0.7rem';
        delete_button.style.cursor = 'pointer';
        delete_button.id = key;

        // Define onclick behavior for the delete button
        delete_button.onclick = function () {
            // Remove the item from the JSON data and update the input field value
            delete json_data[key];
            name_container.remove();
            let to_save_data = JSON.stringify(json_data);
            to_save_data = to_save_data.replace(/"/g, "'");
            $(id_reference).val(`"${to_save_data}"`);
            $(`#${field_name}custom-content`).remove();
            load_content(field_name, id_reference, '#' + container_id);
        };

        // Set the name and add it to the name container
        name.innerHTML = key;
        name.style.fontWeight = 'bold';
        name_container.appendChild(name);

        // Add the delete button to the name container
        name_container.appendChild(delete_button);

        // Add the name container to the content container
        document.getElementById(field_name + 'custom-content').appendChild(name_container);

        // Create an option container for each key
        let option_container = document.createElement('div');
        option_container.style.border = '1px solid black';
        option_container.style.borderRadius = '0.5rem';
        option_container.classList.add('row');
        option_container.id = key;
        option_container.classList.add('ml-2');
        let listContainer = document.getElementById(field_name + 'custom-content');

        // Check if the value is an array
        if (json_data[key] instanceof Array) {
            // If it's an array, iterate through each item
            let list = json_data[key];
            
            // Check if the array represents radio buttons or checkboxes
            let is_radio_or_checkbox = false;
            if (list.length >= 2) {
                if ((list[0] == 'checkbox' || list[0] == 'radio') && list[1] instanceof Object) {
                    is_radio_or_checkbox = true;
                }
            }

            // Loop through each item in the array
            for (let i = 0; i < list.length; i++) {
                // Skip the first item if it represents radio buttons or checkboxes
                if (i == 0 && is_radio_or_checkbox) {
                    continue;
                }
                
                // Create a list item for each item in the array
                let item = list[i];
                let listItem = document.createElement('li');
                listItem.className = 'list-group-item ml-2 list-item mt-1 mb-1';
                listItem.style.borderRadius = '0.3rem';
                listItem.style.border = '1px solid #aaa';
                let iTag = document.createElement('i');
                iTag.className = 'fas fa-times custom-icon remove';
                iTag.id = i;

                // Define onclick behavior for the remove button
                iTag.onclick = function () {
                    // Remove the item from the array and update the input field value
                    list.splice(i, 1);
                    listItem.remove();
                    if (json_data[key].length == 0) {
                        delete json_data[key];
                        option_container.remove();
                        name.remove();
                    }
                    let to_save_data = JSON.stringify(json_data);
                    to_save_data = to_save_data.replace(/"/g, "'");
                    $(id_reference).val(`"${to_save_data}"`);
                };

                // Check if it's a radio button or checkbox
                if (is_radio_or_checkbox) {
                    let contain = false;
                    for (let k in list[i]) {
                        // Create input elements for each option
                        let input = document.createElement('input');
                        input.classList.add('mr-1');
                        input.name = key;
                        input.type = list[0];
                        input.disabled = true;
                        let label = document.createElement('label');
                        label.innerHTML = k;
                        if (list[i][k] == '1') {
                            input.checked = true;
                        }
                        // Add the input and label to the list item
                        listItem.appendChild(input);
                        listItem.appendChild(label);
                        listItem.appendChild(iTag);
                        contain = true;
                    }
                    // Check if the list item contains elements
                    if (!contain) {
                        continue;
                    }
                    // Add the list item to the option container
                    option_container.appendChild(listItem);
                } else {
                    // If it's not radio buttons or checkboxes, add the item as text
                    let p = document.createElement('p');
                    p.style.margin = '0';
                    p.style.fontSize = '1.2rem';
                    p.style.fontWeight = 'bold';
                    p.innerHTML = item;
                    // Add the paragraph and remove button to the list item
                    listItem.appendChild(p);
                    listItem.appendChild(iTag);
                    // Add the list item to the option container
                    option_container.appendChild(listItem);
                }
            }

            // Create a button to add new elements to the array
            let addButton = document.createElement('button');
            addButton.className = 'btn btn-primary ml-4';
            addButton.style.marginTop = '0.8rem';
            addButton.style.height = '50%';
            addButton.innerHTML = 'Add Element';
            addButton.onclick = function () {
                // Prompt the user to enter a new item and add it to the array
                let checked;
                let item;
                if (is_radio_or_checkbox) {
                    item = prompt('Enter the item');
                    checked = prompt('Enter 1 if checked else 0');
                } else {
                    item = prompt('Enter the item');
                }
                let obj = {};
                if (item != null) {
                    if (is_radio_or_checkbox) {
                        obj[item] = checked;
                        list.push(obj);
                    } else {
                        list.push(item);
                    }
                    // Create a new list item for the added element
                    let listItem = document.createElement('li');
                    listItem.className = 'list-group-item ml-2 list-item mt-1 mb-1';
                    listItem.style.borderRadius = '0.3rem';
                    listItem.style.border = '1px solid #aaa';
                    // Check if it's radio buttons or checkboxes
                    if (is_radio_or_checkbox) {
                        for (let k in obj) {
                            // Create input elements for each option
                            let input = document.createElement('input');
                            input.classList.add('mr-1');
                            let label = document.createElement('label');
                            label.innerHTML = k;
                            input.type = json_data[key][0]
                            if (obj[k] == '1') {
                                input.checked = true;
                            }
                            input.disabled = true;
                            // Add the input and label to the list item
                            listItem.appendChild(input);
                            listItem.appendChild(label);
                        }
                    } else {
                        // If it's not radio buttons or checkboxes, add the item as text
                        let p = document.createElement('p');
                        p.style.margin = '0';
                        p.style.fontSize = '1.2rem';
                        p.style.fontWeight = 'bold';
                        p.innerHTML = item;
                        // Add the paragraph to the list item
                        listItem.appendChild(p);
                    }
                    // Create a remove button for the added element
                    let iTag = document.createElement('i');
                    iTag.className = 'fas fa-times custom-icon remove';
                    iTag.id = list.length - 1;
                    // Define onclick behavior for the remove button
                    iTag.onclick = function () {
                        // Remove the item from the array and update the input field value
                        list.splice(list.length - 1, 1);
                        listItem.remove();
                        if (json_data[key].length == 0) {
                            delete json_data[key];
                            option_container.remove();
                            name.remove();
                        }
                        let to_save_data = JSON.stringify(json_data);
                        to_save_data = to_save_data.replace(/"/g, "'");
                        $(id_reference).val(`"${to_save_data}"`);
                    };
                    // Add the remove button to the list item
                    listItem.appendChild(iTag);
                    // Add the new list item before the add button
                    addButton.before(listItem);
                    // Update the input field value
                    let to_save_data = JSON.stringify(json_data);
                    to_save_data = to_save_data.replace(/"/g, "'");
                    $(id_reference).val(`"${to_save_data}"`);
                }
            };
            // Add the add button to the option container
            option_container.appendChild(addButton);
            // Add the option container to the list container
            listContainer.appendChild(option_container);
        } else {
            // If it's not an array, handle differently (e.g., input field)
            let input = document.createElement('input');
            input.disabled = true;
            input.classList.add('form-control', 'ml-2');
            input.value = json_data[key];
            // Define oninput behavior for the input field
            input.oninput = function () {
                // Update the value in the JSON data when the input changes
                json_data[key] = input.value;
                let to_save_data = JSON.stringify(json_data);
                to_save_data = to_save_data.replace(/"/g, "'");
                $(id_reference).val(`"${to_save_data}"`);
            };
            option_container.style.border = '';
            option_container.style.borderRadius = '';
            // Add the input field to the option container
            option_container.appendChild(input);
            // Add the option container to the list container
            listContainer.appendChild(option_container);
        }
    }
}
// Call the load_content function to initialize content loading


// Add an event listener to the content input field to perform changes on input
$('#id_content').on('input', function () {
    perform_content_changes();
});
$('#id_form').on('input', function () {
    perform_form_changes();
});