// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
console.log("=====")
document.addEventListener('DOMContentLoaded', function() {
    console.log("Dom active")

    var ctx = document.getElementById('categoryChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categoryLabels,

            datasets: [{
                label: 'Category Distribution',
                data: categoryData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
    
    console.log("========== fnDataCount ->", fnDataCount);

    var ctx = document.getElementById('fakeNewsPie').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: fnlabelName,

            datasets: [{
                label: 'FakeNews Distribution',
                data: fnDataCount,
                backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    
    console.log("==========");
    console.log("categoryLabels:", categoryLabels);
    console.log("fake_Counts:", fake_Counts);
    console.log("real_Counts:", real_Counts);
    var ctxBar = document.getElementById('categoryChartBar').getContext('2d');
    var myChartBar = new Chart(ctxBar, {
        type: 'bar',
        data: { 
            labels: categoryNames,
            datasets: [{
                label: 'Fake Counts',
                data: fake_Counts,
                backgroundColor: 'rgba(255, 159, 64, 0.2)', // Màu cam nhạt
                borderColor: 'rgba(255, 159, 64, 1)', // Màu cam
                borderWidth: 1
            }, {
                label: 'Real Counts',
                data: real_Counts,
                backgroundColor: 'rgba(153, 102, 255, 0.2)', // Màu tím nhạt
                borderColor: 'rgba(153, 102, 255, 1)', // Màu tím
                borderWidth: 1
            }]
            
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
});

