/* Desired behavior: 
- default languages shown at start
- category selected: all included languages selected (OR logic)
- category unselected: all included languages selected if not still covered by other selected categories
- language/row selected: no side effect; categories unchanged (i.e. language/row un-/selection overrides category selections)
- language/row selected: unselected, unless implied by a selected category
*/

const table = document.getElementById("categoryTable");
const rowNames = Object.freeze(Array.from(document.querySelectorAll('.row_menu input[type="checkbox"]')).map(input => input.value));
const colNames = Object.freeze(Array.from(document.querySelectorAll('.col_menu input[type="checkbox"]')).map(input => input.value));
const helpButton = document.getElementById("helpButton");
const rowsButton = document.getElementById('rowsButton');
const columnsButton = document.getElementById('columnsButton');
const displayButton = document.getElementById('displayButton');
const outputToggle = document.getElementById("outputToggle");
const outputPrefixToggle = document.getElementById('outputPrefixToggle');
const titleToggle = document.getElementById('titleToggle');
// console.log("rowNames", rowNames);
// console.log("colNames", colNames);

const langClasses = {
    compiled: ['rust', 'haskell'],
    interpreted: ['python', 'haskell'],
};
const subsections = {
    '0': ['0.0', '0.0.0', '0.1', '0.1.0', '0.1.1'],
    '0.0': ['0.0.0'],
    '0.1': ['0.1.0', '0.1.1']
};

const categoryHierarchy = {
    prim_types: ['integer', 'boolean'],
};

// HELPER/GENERIC FUNCTIONS ==========================================================================================================

function hideAll(className) {
    document.querySelectorAll(`.${className}`).forEach(cell => {
        cell.classList.add("hidden");
    });
}

function unhideAll(className) {
    document.querySelectorAll(`.${className}`).forEach(cell => {
        cell.classList.remove("hidden");
    });
}

function toggleHidden(className) {
    document.querySelectorAll(`.${className}`).forEach(cell => {
        cell.classList.toggle("hidden");
    });
}

function getCheckboxValues(className) {
    return Array.from(document.querySelectorAll(`.${className} input[type="checkbox"]`))
        .filter(input => input.checked)
        .map(input => input.value);
}

// FUNCTIONS ==========================================================================================================

function computeLanguages() {
    const selectedLanguages = getCheckboxValues('col_menu')
    console.log('selectedLanguages', selectedLanguages)

    return [...new Set(selectedLanguages.flatMap(item => langClasses[item] || item))];
}

function computeRows() {
    const selectedRows = getCheckboxValues('row_menu')
    console.log('selectedRows', selectedRows)

    return [...new Set(selectedRows.flatMap(item => [item].concat(subsections[item] || [item])))];
}

function toggleOutput(isSelected) {
    if (isSelected) {
        unhideAll('output_cell');
    }
    else {
        hideAll('output_cell');
    }
}

function toggleOutputPrefix(isSelected) {
    if (isSelected) {
        unhideAll('output_prefix');
    }
    else {
        hideAll('output_prefix');
    }
}

function toggleTitle(isSelected) {
    const titleBlock = document.getElementById('title');
    const tableBlock = document.getElementById('table-container');
    if (isSelected) {
        titleBlock.classList.add("hidden");
        tableBlock.style.top = '4rem';
        tableBlock.style.maxHeight = 'calc(100vh - 4rem)';
    }
    else {
        titleBlock.classList.remove("hidden");
        tableBlock.style.top = '8rem';
        tableBlock.style.maxHeight = 'calc(100vh - 8rem)';
    }
}

function toggleBoilerplate() {
    document.querySelectorAll('.boilerplate').forEach(el => {
        if (el.textContent === '') {
            text = el.getAttribute('data-original');
            console.log(text);
            el.textContent = text;
            el.appendChild(document.createElement("br"));
        } else {
            el.setAttribute('data-original', el.textContent);
            el.textContent = '';
        }
    });
    toggleHidden('boilerplate_indent');
}

function updateChildLanguages(selectedLangs) {
    document.querySelectorAll('.col_menu input[type="checkbox"]').forEach(checkbox => {
        if (selectedLangs.includes(checkbox.value)) {
            checkbox.checked = true;
        }
    });
}

function updateChildRows(selectedRows) {
    document.querySelectorAll('.row_menu input[type="checkbox"]').forEach(checkbox => {
        if (selectedRows.includes(checkbox.value)) {
            checkbox.checked = true;
        }
    });
}

function deselectChildRows(rowID) {
    if (rowID in subsections) {
        const toDeselect = subsections[rowID];
        document.querySelectorAll('.row_menu input[type="checkbox"]').forEach(checkbox => {
            if (toDeselect.includes(checkbox.value)) {
                checkbox.checked = false;
            }
        });
    }
}

function deselectChildLanguages(colID) {
    if (colID in langClasses) {
        const toDeselect = langClasses[colID];
        document.querySelectorAll('.col_menu input[type="checkbox"]').forEach(checkbox => {
            if (toDeselect.includes(checkbox.value)) {
                checkbox.checked = false;
            }
        });
    }
}

function filterTableRows() {
    const selectedRows = computeRows();
    console.log('selectedRows', selectedRows);
    updateChildRows(selectedRows);

    table.querySelectorAll("tbody tr").forEach(row => {
        const rowCategory = row.dataset.category;
        const hasMatch = selectedRows.includes(rowCategory);
        row.classList.toggle("hidden", !hasMatch);
    });
}


function filterLanguages() {
    selectedLanguages = computeLanguages();
    console.log(selectedLanguages);
    updateChildLanguages(selectedLanguages);

    table.querySelectorAll("thead th").forEach(th => {
        if (!th.classList.contains('row_name')) {
            if (selectedLanguages.includes(th.dataset.category)) {
                th.classList.remove("hidden");
            }
            else {
                th.classList.add("hidden");
            }
        }
    });

    table.querySelectorAll("tbody tr").forEach(row => {
        row.querySelectorAll("td").forEach(td => {
            console.log(td)
            if (!td.classList.contains('row_name')) {
                if (selectedLanguages.includes(td.dataset.category)) {
                    td.classList.remove("hidden");
                }
                else {
                    td.classList.add("hidden");
                }
            }
            else { console.log("nothing"); }
        });
    });
}

function getOpenDropdown() {
    const openDropdowns = document.querySelectorAll('.dropdown.open');

    return openDropdowns.length > 0 ? openDropdowns[0] : null;
}

function closeDropdowns() {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        dropdown.classList.remove('open');
    });
    console.log("open dropdown:", getOpenDropdown());
}

function getSelectedLabel(dropdown) {
    const labels = Array.from(dropdown.querySelectorAll("label"));
    const selectedLabelIndex = labels.findIndex(el => el.classList.contains("selected"));

    if (selectedLabelIndex !== -1) {
        return { label: labels[selectedLabelIndex], index: selectedLabelIndex };
    }

    return null;
}

function selectItem(index) {
    const openDropdown = getOpenDropdown();
    if (openDropdown) {
        const selectedLabelAndIndex = getSelectedLabel(openDropdown);
        if (!selectedLabelAndIndex) {
            console.log(openDropdown);
            console.log(selectedLabelAndIndex);
            const options = openDropdown.querySelectorAll("label");
            options.forEach((opt, i) => {
                opt.classList.toggle("selected", i === index);
            });
        }
    }
}


// EVENT LISTENERS FOR CLICKS ====================================================================================================

document.querySelectorAll('.row_menu input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener("change", (event) => {
        if (event.target.checked) {
            filterTableRows();
        } else {
            deselectChildRows(event.target.value);
            filterTableRows();
        }
    })
});

document.querySelectorAll('.col_menu input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener("change", (event) => {
        if (event.target.checked) {
            filterLanguages();
        } else {
            deselectChildLanguages(event.target.value);
            filterLanguages();
        }
    })
});

document.getElementById('boilerplateToggle').addEventListener('change', toggleBoilerplate);

outputToggle.addEventListener('change', (event) => {
    toggleOutput(event.target.checked);
});

outputPrefixToggle.addEventListener('change', (event) => {
    toggleOutputPrefix(event.target.checked);
});

titleToggle.addEventListener('change', (event) => {
    toggleTitle(event.target.checked);
});

document.querySelectorAll('.dropdown button').forEach(button => {
    button.addEventListener('click', () => {
        const dropdown = button.parentElement;
        dropdown.classList.toggle('open');
    });
});

document.addEventListener('click', (e) => {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        if (!dropdown.contains(e.target)) {
            dropdown.classList.remove('open');
        }
    });
});

// EVENT LISTENERS FOR KEYS ================================================================================================

function setKeybind(event, keyName, element) {
    if (event.key === keyName && !event.ctrlKey && !event.altKey && !event.metaKey) {
        event.preventDefault();
        if (element) {
            element.click();
        }
        selectItem(0);
    }
}

document.addEventListener("keydown", (event) => {
    setKeybind(event, 'b', boilerplateToggle);
    setKeybind(event, 'c', columnsButton);
    setKeybind(event, 'd', displayButton);
    setKeybind(event, 'i', helpButton);
    setKeybind(event, 'o', outputToggle);
    setKeybind(event, 'p', outputPrefixToggle);
    setKeybind(event, 'r', rowsButton);
    setKeybind(event, 't', titleToggle);
    if (event.key === 'Escape' && !event.ctrlKey && !event.altKey && !event.metaKey) {
        event.preventDefault();
        closeDropdowns();
    }
    if ((event.key === 'j' || event.key === 'k') && !event.ctrlKey && !event.altKey && !event.metaKey) {
        event.preventDefault();

        const openDropdown = getOpenDropdown();
        if (openDropdown) {
            const options = openDropdown.querySelectorAll("label");
            const lastIndex = options.length - 1;
            const selectedLabelAndIndex = getSelectedLabel(openDropdown);
            if (!selectedLabelAndIndex) {
                let selectedIndex = 0;
            }
            else {
                selectedIndex = selectedLabelAndIndex.index;
            }
            
            if (event.key === 'j') {
                selectedIndex++;
            }
            else {
                selectedIndex--;
            }

            selectedIndex = Math.max(0, Math.min(selectedIndex, lastIndex));
            console.log(selectedIndex);

            function updateSelection() {
                options.forEach((opt, i) => {
                    opt.classList.toggle("selected", i === selectedIndex);
                });
            }

            updateSelection();
            console.log(openDropdown);

        }
    }
    if (event.code === 'Space' && !event.ctrlKey && !event.altKey && !event.metaKey) {
        event.preventDefault();

        const openDropdown = getOpenDropdown();
        if (openDropdown) {
            const selectedLabelAndIndex = getSelectedLabel(openDropdown);
            if (selectedLabelAndIndex) {
                const selectedLabel = selectedLabelAndIndex.label;
                const checkbox = selectedLabel.querySelector("input");
                console.log(selectedLabel);

                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                }

                const changeEvent = new Event('change');
                checkbox.dispatchEvent(changeEvent);
            }
        }
    }
});

// INITIALIZATION =====================================================================================================

toggleOutput(false);
toggleOutputPrefix(false);
document.documentElement.style.setProperty('--cell-width-chars', '40');