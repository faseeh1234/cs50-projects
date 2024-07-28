// table CSS setup
// document.addEventListener('DOMContentLoaded', function(e) {
//     const table = document.querySelector('table#todo-list');
//     const columns = document.querySelectorAll('th');
//     const colWidth = [1, 3, 2, 2, 2];
//     let fullWidth = 0;
//     colWidth.forEach( num => {
//         fullWidth += num;
//       })

//     for (let i = 0; i < colWidth.length; i++) {
//         columns[i].style.width = '${(colWidth[i] / fullWidth) * 100}%';
//     }
// });



document.addEventListener('DOMContentLoaded', function(e) {
    let taskCount = 0;
    const table = document.querySelector('table#todo-list');
    const tbody = table.children[1];

    const button = document.querySelector('#task-input > button#add-task');
    button.addEventListener('click', function(e) {
        const taskName = document.querySelector('#task-input > input#task');
        const priority = document.querySelector('#task-input > select#priority');
        const dueDate = document.querySelector('#task-input > input#due-date');

        // check for empty task
        if (taskName.value == '') {
            return;
        }
        console.log(taskName.value);

        taskCount++;
        const newTask = document.createElement('tr')
        newTask.innerHTML += `
            <td>${taskCount}</td>
            <td>${taskName.value}</td>
            <td>${priority.value}</td>
            <td>${dueDate.value}</td>
            <td>
                <input type='checkbox'>
            </td>
        `
        tbody.appendChild(newTask)

    });
});

