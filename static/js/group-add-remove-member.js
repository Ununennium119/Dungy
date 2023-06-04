let members_fields_count_input = document.getElementsByName("members_fields_count")[0];
let members_fields_count = Number(members_fields_count_input.value);

let add_btn = document.getElementById("add-extra-member");
add_btn.addEventListener("click", add_extra_member);

for (let i = 0; i < members_fields_count; i++) {
    let remove_btn = document.getElementById(`remove-member_${i}`);
    if (remove_btn) {
        remove_btn.addEventListener("click", remove_member);
    }
}

function add_extra_member(e) {
    e.preventDefault();

    let field_name = `member_${members_fields_count}`

    let container = document.createElement("div");
    container.id = `${field_name}-container`;

    let element = document.createElement("div");
    element.innerHTML += `<label for="id_${field_name}" class="form-label">Member</label>\n`;
    element.innerHTML += `<input type="email" name="${field_name}" id="id_${field_name}" autocomplete="off">\n`;

    let remove_btn = document.createElement("button");
    remove_btn.id = `remove-${field_name}`;
    remove_btn.dataset.fieldName = `${field_name}`;
    remove_btn.innerHTML = "X";
    remove_btn.classList.add("remove-btn", "red-btn"); // Add the necessary classes for styling
    element.append(remove_btn)

    element.innerHTML += "<div><ul></ul></div>\n"
    container.append(element)
    document.getElementById("members-container").append(container);

    remove_btn = document.getElementById(`remove-member_${members_fields_count}`);
    remove_btn.addEventListener("click", remove_member);

    members_fields_count++;
    members_fields_count_input.value = members_fields_count;
}

function remove_member(e) {
    e.preventDefault();
    console.log(e.target);
    let element = document.getElementById(`${e.target.dataset.fieldName}-container`);
    element.remove();
}
