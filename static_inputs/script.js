        // Get reference to the group checkboxes, group select element, and the example table
        var groupCheckboxes = document.querySelectorAll('#groupCheckboxes input[type="checkbox"]');
        var groupSelect = document.getElementById('groupSelect');
        var table = document.getElementById('exampleTable');
        
        // Add event listeners to the group checkboxes and group select element
        groupCheckboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', filterExamples);
        });
        
        groupSelect.addEventListener('change', filterExamples);
        
        // Function to filter the examples based on the selected groups
        function filterExamples() {
            // Get the selected groups
            var selectedGroups = Array.from(groupSelect.selectedOptions, option => option.value);
            
            // Show or hide table rows based on the selected groups
            Array.from(table.tBodies[0].rows).forEach(function(row) {
                var groups = row.getAttribute('data-groups').toLowerCase().split(' ');
                
                var shouldShow = selectedGroups.includes('all') || groups.some(function(group) {
                    return selectedGroups.includes(group);
                });
                
                row.style.display = shouldShow ? 'table-row' : 'none';
            });
            
            // Update the group checkboxes based on the selected groups in the dropdown
            groupCheckboxes.forEach(function(checkbox) {
                checkbox.checked = selectedGroups.includes(checkbox.value) || selectedGroups.includes('all');
            });
        }