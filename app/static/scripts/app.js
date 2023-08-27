var app_methods = {};

app_methods.change_panel = function(panel,manager_panel){
    // this.search_bar_val = '',
    this.username = '';
    this.password = '';
    this.fullname = '';
    this.show_location = 'false'
    this.panel = panel;
    this.manager_panel = manager_panel;
}

app_methods.isActivePanel = function(panel){
    if (this.manager_panel == panel) { return true } else {return false}
}

app_methods.isActivePage = function(index){
    return index === this.activeIndexPage;
}


app_methods.getSouvenirPhotos = function(page){
    if (this.selected_karavan_uuid == ''){
        Swal.fire({title:'انتخاب کاروان' ,text:'لطفا ابتدا کاروان مورد نظر خود را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})
        return;
    }
    this.activeIndexPage = page;
    data = {'karavan_uuid': this.selected_karavan_uuid, 'page_index':page}
    axios.post('/get-souvenir-photos', data).then(response => {  
        if (response.data['status-code'] == 200) {
            this.souvenir_photos = response.data['result']
            this.pages = response.data['count_pages']
            this.change_panel('manager', 'souvenir-photos')
        }
        else { Swal.fire({title:'ناموفق' ,text:'خطای نامشخص', icon:'info', confirmButtonText:'تایید'}) }
    })
}


app_methods.getRegisteredLocations = function(page){
    if (this.selected_karavan_uuid == ''){
        Swal.fire({title:'انتخاب کاروان' ,text:'لطفا ابتدا کاروان مورد نظر خود را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})
        return;
    }
    this.activeIndexPage = page;
    data = {'karavan_uuid': this.selected_karavan_uuid, 'page_index':page}
    axios.post('/get-registered-locations', data).then(response => {  
        if (response.data['status-code'] == 200) {
            this.registered_locations = response.data['result']
            this.pages = response.data['count_pages']
            this.change_panel('manager', 'registered-locations')
        }
        else { Swal.fire({title:'ناموفق' ,text:'خطای نامشخص', icon:'info', confirmButtonText:'تایید'}) }
    })
}   


app_methods.getKaravanUsersInfo = function(page){
    this.activeIndexPage = page;
    data = {'karavan_uuid': this.selected_karavan_uuid, 'page_index':page}

    axios.post('/get-karavan-users-info', data).then(response => {
        
        if (response.data['status-code'] == 200) {
            this.users_info = response.data['result']
            this.pages = response.data['count_pages']
            for (let i=0; i < this.users_info.length; i++){                
                if (this.users_info[i][5] == 'true'){
                    this.users_info[i][5] = 'فعال'
                }
                else {
                    this.users_info[i][5] = 'غیر فعال'
                }}                    
        }
        else {
            Swal.fire({title:'خطا' ,text:'خطای نامشخص', icon:'error', confirmButtonText:'تایید'})
        }
    })
}


app_methods.changeSelectedKaravan = function(){
    if (this.selected_karavan_uuid == ''){
        this.show_panel = '';
        return
    } 
    switch (this.manager_panel){
        case 'manager-dashboard':
            this.getKaravanUsersInfo(1);  
            break;  
            
        case 'souvenir-photos':
            this.getSouvenirPhotos(1);
            break;
            
            case 'registered-locations':
            this.getRegisteredLocations(1);
            break;
        }
    this.show_panel = 'true'    
}

// setTimeout(()=>{this.showLocation()}, 100)


app_methods.showLocation = function(longitude,latitude){
    if (this.show_location == 'true'){
        this.show_location = 'false';
    }
    else {
        this.show_location = 'true';
        // debugger
        this.$nextTick(() => {
            var map = L.map('map').setView([latitude, longitude ], 14);
            
            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19,
            }).addTo(map);
            var marker = L.marker([latitude, longitude]).addTo(map);
        })
    }
}


// app_methods.getUserLocations = function(user_uuid){
//     data = {'user_uuid': user_uuid}
//     axios.post('/get-user-locations', data).then(response => {  
//         if (response.data['status-code'] == 200) {
//             console.log(response.data)
//         }
//         else { Swal.fire({title:'ثبت نشده' ,text:'این عضو تا به حال موقعیت مکانی خود را ارسال نکرده است', icon:'info', confirmButtonText:'تایید'}) }
//     })
// }

app_methods.addUserToKaravan = function(){
    if (this.selected_karavan_uuid == ''){
        Swal.fire({title:'انتخاب کاروان' ,text:'لطفا ابتدا کاروان مورد نظر خود را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})
        return;
    }
    Swal.fire({
        title: 'افزودن عضو به کاروان',
        html: `<input v-model="user_fullname" type="text" id="add-user-to-karavan-fullname" class="swal2-input" placeholder="نام و نام خانوادگی">
        <input v-model="user_username" type="text" id="add-user-to-karavan-username" class="swal2-input" placeholder="نام کاربری">`,
        inputPlaceholder: 'مثال : محمد اقلیما',
        confirmButtonText: 'افزودن',
        focusConfirm: false,
        preConfirm: () => {
            const fullname = Swal.getPopup().querySelector('#add-user-to-karavan-fullname').value
            const username = Swal.getPopup().querySelector('#add-user-to-karavan-username').value
            if (!fullname || !username) {
                Swal.showValidationMessage(`لطفا اطلاعات را تکمیل کنید`)
            }
            return { fullname: fullname, username: username }
        }
    }).then((result) => {
        if (result.value != null){
            data = {'fullname': result.value.fullname ,
                    'username': result.value.username ,
                    'karavan_uuid': this.selected_karavan_uuid
                }
            axios.post('/add-new-user-to-karavan', data).then(response => {  
                if (response.data['status-code'] == 201){
                    this.getKaravanUsersInfo(1)
                    Swal.fire({title:'موفقیت آمیز' ,text:'کاربر با موفقیت اضافه شد', icon:'success', confirmButtonText:'تایید'})
                }
                else if (response.data['result'] == 'no_valid_fullname') {Swal.fire({title:'خطا' ,text:'نام و نام خانوادگی را فقط به فارسی وارد کنید', icon:'error', confirmButtonText:'تایید'})}
                
                else if (response.data['result'] == 'empty_username') {Swal.fire({title:'خطا' ,text:'لطفا یک نام کاربری انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
                else if (response.data['result'] == 'duplicate_username' ) {Swal.fire({title:'خطا' ,text:'نام کاربری وارد شده از قبل در سیستم وجود دارد. لطفا نام کاربری دیگری را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
                else if (response.data['result'] == 'length_username') {Swal.fire({title:'خطا' ,text:'طول نام کاربری باید بین 3 تا 20 کاراکتر باشد', icon:'error', confirmButtonText:'تایید'})}
                else if (response.data['result'] == 'char_username') {Swal.fire({title:'خطا' ,text:'نام کاربری فقط می تواند شامل حروف کوچک و بزرگ انگلیسی و اعداد و نقطه و زیرخط(آندرلاین) باشد', icon:'error', confirmButtonText:'تایید'})}

                else{ Swal.fire({title:'خطا' ,text:'خطای نامشخص', icon:'error', confirmButtonText:'تایید'}) }
            })
        }
    })
}  


app_methods.addKaravan = function(){
    Swal.fire({
        title: 'یک نام برای کاروان خود انتخاب کنید',
        input: 'text',
        inputPlaceholder: 'مثال : کاروان حسینی ها',
      }).then( (input) => {
        data = {'new_karavan_name': input.value}
        if (input.value != null){
            axios.post('/add-new-karavan', data).then(response => {  
                if (response.data['status-code'] == 200){
                    this.getKaravansName(1)
                    Swal.fire({title:'ثبت کاروان' ,text:'کاروان جدید با موفقیت ایجاد شد', icon:'success', confirmButtonText:'تایید'})
                }
                else {
                    Swal.fire({title:'ناموفق' ,text:'ایجاد کاروان جدید ناموفق بود', icon:'error', confirmButtonText:'تایید'})
                }
            })
        }
})}


app_methods.getKaravansName = function(){
    axios.post('/get-karavans-name').then(response => {         
    this.change_panel('manager', 'manager-dashboard')
    this.manager_karavans_info = response.data['result']
})}


// Signin
app_methods.signinManager = function(){
    var data = {
        'username':this.username,
        'password':this.password,
    }
    axios.post('/signin-manager', data).then(response => {         
        if (response.data['status-code'] == 200) { 
            this.getKaravansName()
            // this.karavan_name = response.data['karavan_name']
            // this.showUserLocation()
        }        
        else {            
            //  Login was not succesfully
            if (response.data['status-code'] == 400){Swal.fire({title:'خطا' ,text:'نام کاربری یا رمز عبور اشتباه است', icon:'error', confirmButtonText:'تایید'})}
            this.panel = 'sign-in'
        }
    })
};


// Signup
app_methods.signupManager = function(){
    var data = {
        'fullname' : this.fullname,
        'username' : this.username,
        'password' : this.password,
    }    
    axios.post('/signup-manager', data).then(response => {  
        if (response.data['status-code'] == 201) { 
            //  Signup was succesful
            Swal.fire({title:'تایید ثبت نام' ,text:'ثبت نام با موفقیت انجام شد. حالا می توانید وارد حساب کاربری خود شوید', icon:'success', confirmButtonText:'تایید'})
            this.change_panel('sign-in',null)
        }        
        else if (response.data['result'] == 'no_valid_fullname') {Swal.fire({title:'خطا' ,text:'نام و نام خانوادگی خود را فقط به فارسی وارد کنید', icon:'error', confirmButtonText:'تایید'})}

        else if (response.data['result'] == 'password_length') {Swal.fire({title:'خطا' ,text:'رمز عبور باید شامل حروف انگلیسی و حداقل شامل 8 کاراکتر باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'empty_password') {Swal.fire({title:'خطا' ,text:'لطفا یک رمز عبور برای خودتان انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'used_info_in_password') {Swal.fire({title:'خطا' ,text:'رمز عبور شما مطابقت زیادی با نام کاربری تان دارد. لطفا رمز عبور دیگری را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        
        else if (response.data['result'] == 'empty_username') {Swal.fire({title:'خطا' ,text:'لطفا یک نام کاربری برای خودتان انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'duplicate_username' ) {Swal.fire({title:'خطا' ,text:'نام کاربری وارد شده از قبل در سیستم وجود دارد. لطفا نام کاربری دیگری را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'length_username') {Swal.fire({title:'خطا' ,text:'طول نام کاربری شما باید بین 3 تا 20 کاراکتر باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'char_username') {Swal.fire({title:'خطا' ,text:'نام کاربری فقط می تواند شامل حروف کوچک و بزرگ انگلیسی و اعداد و نقطه و زیرخط(آندرلاین) باشد', icon:'error', confirmButtonText:'تایید'})}
        else{ Swal.fire({title:'خطا' ,text:'خطای نامشخص', icon:'error', confirmButtonText:'تایید'}) }
    })
};


Vue.createApp({
    data(){ return {        
        panel: 'sign-in',
        manager_panel: '',
        show_panel: '',  // In the dashboard

        manager_karavans_info: '',
        // current_karavan_name: '',
        users_info:'' ,

        //  Sign in/up manager Info
        username: '',
        password: '',
        fullname: '',

        // user - in signup user to karavan
        user_fullname: '',
        user_username: '',

        // search-bar
        search_bar_val: null,

        // count of the current manager_panel pages for pagination
        pages: '',
        activeIndexPage: '',

        // selected karavan name
        selected_karavan_uuid: '',

        map: '',
        show_location: '',

        souvenir_photos: '',
        registered_locations: '',
    } },
    
    delimiters: ["${", "}$"],    
    methods:app_methods,
    
}).mount('#app')