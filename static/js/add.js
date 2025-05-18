document.getElementById('SHT_Register').addEventListener('change', function () {
    var register = this.value.trim();

    if (register) {
        const encodedRegister = encodeURIComponent(register);

        fetch('/get_latest_num_late?register=' + encodeURIComponent(register))
            .then(response => response.json())
            .then(data => {
                console.log('Fetched:', data);
                document.getElementById('SHT_Num_First').value = data.SHT_Num_Late || 0;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                document.getElementById('SHT_Num_First').value = 0;
            });
    }
});