function sliderValueDisplay(event, slider_id) {
    const slider = document.querySelector(slider_id);
    const label = document.querySelector(slider_id + '-label');
    label.innerHTML = slider.value;

}

function runSimulation(event) {
    const outputTable = document.querySelector('table#output-table');
    const N = document.querySelector('#total-pop').value;
    const Istart = document.querySelector('#Istart').value;
    const di = document.querySelector('#i-slider').value;
    const dr = document.querySelector('#r-slider').value;
    outputTable.style.display = 'table;'

    // Reset table
    outputTable.innerHTML = `
    <tr class="math-font">
                <th>Time</th>
                <th>S(t)</th>
                <th>I(t)</th>
                <th>R(t)</th>
            </tr>
    `

    // Initial conditions
    let time = 0;
    let S = N - Istart;
    let I = Istart;
    let R = 0;

    while (time <= 15 && I != 0) {
    // Display row
    outputTable.innerHTML += `
    <tr>
        <td>${time}</td>
        <td>${S}</td>
        <td>${I}</td>
        <td>${R}</td>
    </tr>
    `

    // Calculate next values
    new_infections = Math.round(I * di);
    new_recoveries = Math.round(I * dr);

    if (new_infections > S) {new_infections = S;}
    if (new_recoveries > I) {new_recoveries = I;}

    S = S - new_infections;
    R = R + new_recoveries;
    I = I - new_recoveries;
    I = I + new_infections;
    sum = S + I + R;

    time++;
    }

}



document.addEventListener('DOMContentLoaded', function(e) {
    iSliderId = '#i-slider';
    document.querySelector(iSliderId).addEventListener('input', function(event) {
        sliderValueDisplay(event, iSliderId);
        runSimulation(event);
    });
    rSliderId = '#r-slider';
    document.querySelector(rSliderId).addEventListener('input', function(event) {
        sliderValueDisplay(event, rSliderId);
        runSimulation(event);
    });
});
