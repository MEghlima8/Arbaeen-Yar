var app_methods = {};

app_methods.change_panel = function(panel,manager_panel){
    // this.search_bar_val = '',
    this.panel = panel,
    this.manager_panel = manager_panel
}


// var map = L.map('map').setView([32.62132477920994, 44.03612973588855], 12);

// L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
//     maxZoom: 19,
// }).addTo(map);


// app_methods.isActivePage = function(index){
//     return index === this.activeIndexPage;
// }


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
            axios.post('/add-new-user-to-karavan', result.value).then(response => {  
                if (response.data['status-code'] == 201){
                    this.getKaravanUsersInfo()
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


app_methods.getKaravanUsersInfo = function(){
    data = {'karavan_uuid': this.selected_karavan_uuid}
    axios.post('/get-karavan-users-info', data).then(response => {
        
        if (response.data['status-code'] == 200) {
            this.users_info = response.data['result']
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
        this.users_info_panel = '';
    } 
    else {
        this.getKaravanUsersInfo()
        }
    this.users_info_panel = 'true'
}



app_methods.addKaravan = function(){
    Swal.fire({
        title: 'یک نام برای کاروان خود انتخاب کنید',
        input: 'text'
      }).then( (input) => {
        data = {'new_karavan_name': input.value}
        if (input.value != null){
            axios.post('/add-new-karavan', data).then(response => {  
                if (response.data['status-code'] == 200){
                    this.getKaravansName()
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
        users_info_panel: '',  // In the dashboard

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

        // count of the current admin_panel pages for pagination
        pages: '',
        activeIndexPage: '',

        // selected karavan name
        selected_karavan_uuid: '',

        map: '',
    } },
    
    delimiters: ["${", "}$"],    
    methods:app_methods,
    
}).mount('#app')