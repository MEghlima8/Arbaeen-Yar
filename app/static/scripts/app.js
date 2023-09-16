var app_methods = {};


app_methods.showSearchBar = function(open){
    if (open){
        //Search button click event
        $('.search-bar').addClass('open');
        $('.search-bar').find('input[type="text"]').focus();
    }
    else{
        //Close search click event
        $('.search-bar').removeClass('open');
        this.search_bar_val = null;
    }
}


app_methods.change_panel = function(panel,manager_panel,change_section=false){
    this.search_bar_val = '',
    this.username = '';
    this.password = '';
    this.fullname = '';
    this.show_location = 'false'
    this.panel = panel;
    this.manager_panel = manager_panel;

    if (manager_panel != 'registered-locations'){ this.show_all_users_locations_on_map = false };
    if(manager_panel != 'souvenir-photos') { this.show_all_users_souvenir_album = false; }
    
}

app_methods.isActivePanel = function(panel){
    if (this.manager_panel == panel) { return true } else {return false}
}

app_methods.isActivePage = function(index){
    return index === this.activeIndexPage;
}


// Search with fullname or username
app_methods.onClick_searchBarAdvs = function(){
    if (this.search_bar_val != null){
        this.pages = null;
    
        if (this.manager_panel == 'manager-dashboard') {
            this.getKaravanUsersInfo(1)
        }
        else if (this.manager_panel == 'souvenir-photos'){
            this.getSouvenirPhotos(1);
        }
        else if (this.manager_panel == 'registered-locations'){
            this.getRegisteredLocations(1)
        }
        this.search_bar_val = null;
    }
}


app_methods.getSouvenirPhotos = function(page){
    if (this.selected_karavan_uuid == ''){
        Swal.fire({title:'انتخاب کاروان' ,text:'لطفا ابتدا کاروان مورد نظر خود را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})
        return;
    }
    this.activeIndexPage = page;
    data = {'karavan_uuid': this.selected_karavan_uuid, 'page_index':page, 'time':this.selected_time, 'event':this.selected_event, 'search_value':this.search_bar_val}
    axios.post('/get-souvenir-photos', data).then(response => {

        if (response.data['status-code'] == 200) {
            this.souvenir_photos = response.data['result']

            for (var i=0 ; i < this.souvenir_photos.length;i++ ){
                if (this.souvenir_photos[i][4]['event'] == 'arbaeen'){this.souvenir_photos[i][4]['event']='اربعین' }
                else if (this.souvenir_photos[i][4]['event'] == 'moharram'){this.souvenir_photos[i][4]['event']='محرم' }
                else if (this.souvenir_photos[i][4]['event'] == 'fetr'){this.souvenir_photos[i][4]['event']='فطر' }
                else if (this.souvenir_photos[i][4]['event'] == 'ghadir'){this.souvenir_photos[i][4]['event']='غدیر' }
                else if (this.souvenir_photos[i][4]['event'] == 'other'){this.souvenir_photos[i][4]['event']='سایر' }
            }

            this.pages = response.data['count_pages']
            this.change_panel('manager', 'souvenir-photos')
            this.$nextTick(() => {
                $(function () {
                    $('#aniimated-thumbnials').lightGallery({
                        thumbnail: true,
                        selector: 'a'
                    });
                });
            })        
            
        }
        else { Swal.fire({title:'ناموفق' ,text:'خطای نامشخص', icon:'info', confirmButtonText:'تایید'}) }
    })
}


app_methods.changePanelForAllUsersLocations = function(){
    this.show_all_users_locations_on_map = !this.show_all_users_locations_on_map;

    if (this.show_all_users_locations_on_map){
        this.showAllUsersLocationsOnMap();
    }
    else{
        this.getRegisteredLocations(1);
    }
}


app_methods.changePanelForAllUsersSouvenirPhotos = function(){
    this.show_all_users_souvenir_album = !this.show_all_users_souvenir_album;

    if (this.show_all_users_souvenir_album == false){
        this.getSouvenirPhotos(1);
    }
}


// retrieve karavan users locations
app_methods.getRegisteredLocations = function(page){
    if (this.selected_karavan_uuid == ''){
        Swal.fire({title:'انتخاب کاروان' ,text:'لطفا ابتدا کاروان مورد نظر خود را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})
        return;
    }
    if (this.show_all_users_locations_on_map == true){
        this.showAllUsersLocationsOnMap();
        return;
    }
    this.activeIndexPage = page;
    data = {'karavan_uuid': this.selected_karavan_uuid, 'page_index':page, 'time':this.selected_time, 'search_value':this.search_bar_val}
    axios.post('/get-registered-locations', data).then(response => {  
        if (response.data['status-code'] == 200) {
            this.registered_locations = response.data['result']
            this.pages = response.data['count_pages']
        }
        else {
            this.registered_locations = null;
            this.pages = null;
        }
        this.change_panel('manager', 'registered-locations')
    })
}   


app_methods.getKaravanUsersInfo = function(page){
    if (this.selected_karavan_uuid == ''){return;}
    this.activeIndexPage = page;
    
    data = {'karavan_uuid': this.selected_karavan_uuid, 'page_index':page, 'search_value':this.search_bar_val}
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
                this.change_panel('manager', 'manager-dashboard')
            }
        else {
            Swal.fire({title:'خطا' ,text:'خطای نامشخص', icon:'error', confirmButtonText:'تایید'})
        }
    })
}


app_methods.showAllUsersLocationsOnMap = function(){
    data = {'karavan_uuid': this.selected_karavan_uuid, 'page_index':'all', 'time':this.selected_time, 'search_value':this.search_bar_val}
    axios.post('/get-registered-locations', data).then(response => {

        var remained_icons = [...this.map_icons_name];
        var users_icons = {};

        if (response.data['status-code'] == 200) {
            this.registered_locations = response.data['result']

            this.$nextTick(() => {

                if (this.map != null) {
                    this.map.off(); this.map.remove();
                };

                this.map = L.map('all_users_locs_on_map').setView([this.registered_locations[0][4]['latitude'], this.registered_locations[0][4]['longitude']], 13);
                
                L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    maxZoom: 19,
                }).addTo(this.map);

                
                for (var i=0 ; i < this.registered_locations.length;i++ ){
                    if (remained_icons.length == 0) { remained_icons = [...this.map_icons_name] }

                    if(this.registered_locations[i][1] in users_icons){
                        var userIcon = L.icon({iconUrl: './static/css/images/' + users_icons[this.registered_locations[i][1]],shadowUrl: '/static/css/images/marker-shadow.png',iconSize:[38, 40],shadowSize:[38, 40],});
                        this.marker = L.marker([ this.registered_locations[i][4]['latitude'], this.registered_locations[i][4]['longitude']],
                        {icon: userIcon}).addTo(this.map);
                    }
                    else{
                        users_icons[this.registered_locations[i][1]] = remained_icons.pop();
                        var userIcon = L.icon({iconUrl: './static/css/images/' + users_icons[this.registered_locations[i][1]],shadowUrl: '/static/css/images/marker-shadow.png',iconSize:[38, 40],shadowSize:[38, 40],});
                        
                        this.marker = L.marker([ this.registered_locations[i][4]['latitude'], this.registered_locations[i][4]['longitude']],
                        {icon: userIcon}).addTo(this.map);

                    }
                    this.marker.bindPopup(
                        "<h6>نام: " + this.registered_locations[i][0] + "</h6>" +
                    "<div style='margin-bottom: 5px;'></div>" + "<h6>تاریخ: " + this.registered_locations[i][3]['date'] + "</h6>" +
                    "<div style='margin-bottom: 5px;'></div>" + "<h6>زمان: " + this.registered_locations[i][3]['time'] + "</h6>"
                    );
                }
            })
        }
        // Without registered location
        else{
            if (this.map != null){
                this.map.off();
                this.map.remove();
                this.map = L.map('all_users_locs_on_map').setView([27.1963, 56.2884], 14);
                L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19,
                }).addTo(this.map);
            }

            Swal.fire({title:'بدون موقعیت مکانی' ,text:'موقعیت مکانی ثبت شده ای وجود ندارد', icon:'info', confirmButtonText:'تایید'})
        }
    })
}

// retrieve all registered locations of the user
app_methods.showUserAllLocations = function(user_uuid,check_selected_time){
    if (check_selected_time == false) {this.user_locations_selected_time = 'all'}

    data = {'user_uuid': user_uuid, 'time':this.user_locations_selected_time}
    axios.post('/get-user-all-locations', data).then(response => {  

        if (response.data['status-code'] == 200) {
            this.change_panel('manager', 'user-all-locations')
            this.userAllLocations = response.data['result']
            
            this.$nextTick(() => {
                if (this.map != null) {
                    this.map.off(); this.map.remove();
                };
                
                this.map = L.map('user_all_locs_map').setView([this.userAllLocations[0][2]['latitude'], this.userAllLocations[0][2]['longitude']], 14);
                L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    maxZoom: 19,
                }).addTo(this.map);
                
            
                var blueIcon = L.icon({iconUrl: './static/css/images/blue.png',shadowUrl: '/static/css/images/marker-shadow.png',
                iconSize:[38, 40],shadowSize:[38, 40],
                });
            

                this.marker = L.marker([this.userAllLocations[0][2]['latitude'], this.userAllLocations[0][2]['longitude']]).addTo(this.map);
                this.marker.bindPopup("<h6>آخرین موقعیت مکانی ثبت شده</h6>" +
                                "<div style='margin-bottom: 5px;'></div>" + "<h6>تاریخ: " + this.userAllLocations[0][3]['date'] + "</h6>" +
                                "<div style='margin-bottom: 5px;'></div>" + "<h6>زمان: " + this.userAllLocations[0][3]['time'] + "</h6>"
                                );
                            
                if (this.userAllLocations.length != 1){
                    for (var i=1 ; i < this.userAllLocations.length;i++ ){
                        this.marker = L.marker([ this.userAllLocations[i][2]['latitude'], this.userAllLocations[i][2]['longitude']], {icon: blueIcon}).addTo(this.map);
                        this.marker.bindPopup(
                        "<div style='margin-bottom: 5px;'></div>" + "<h6>تاریخ: " + this.userAllLocations[i][3]['date'] + "</h6>" +
                        "<div style='margin-bottom: 5px;'></div>" + "<h6>زمان: " + this.userAllLocations[i][3]['time'] + "</h6>"
                        );
                    }
                }       
            })
        }
        // Without registered location
        else{
            try{
                if (this.map != null){
                    this.map.off();
                    this.map.remove();
                    this.map = L.map('user_all_locs_map').setView([27.1963, 56.2884], 14);
                    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    maxZoom: 19,
                    }).addTo(this.map);
                }
            }
            finally{
                Swal.fire({title:'بدون موقعیت مکانی' ,text:'موقعیت مکانی ثبت شده ای وجود ندارد', icon:'info', confirmButtonText:'تایید'})
            }
    }})    
}



app_methods.showLocation = function(longitude,latitude){
    if (this.show_location == 'true'){
        this.show_location = 'false';
    }
    else {
        this.show_location = 'true';
        this.$nextTick(() => {
            var map = L.map('map').setView([latitude, longitude ], 14);
            
            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19,
            }).addTo(map);
            L.marker([latitude, longitude]).addTo(map);
        })
    }
}


app_methods.changeSelectedKaravan = function(){

    if (this.selected_karavan_uuid == ''){
        this.users_info = null;
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
            this.show_all_users_locations_on_map = false;
            this.getRegisteredLocations(1);
            break;
        }
        
}


app_methods.addUserToKaravan = function(){
    if (this.selected_karavan_uuid == ''){
        Swal.fire({title:'انتخاب کاروان' ,text:'لطفا ابتدا کاروان مورد نظر خود را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})
        return;
    }
    this.change_panel('manager', 'add-user-to-karavan');
}

app_methods.handleExcelFile = function(event){
    this.UsersExcelFile = event.target.files[0]
}

app_methods.sendUserInfoToAddToKaravan = function(type){
    if (type == 'input'){
        data = {'fullname': this.fullname ,'username': this.username ,'karavan_uuid': this.selected_karavan_uuid}
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

    // User sent excel file
    else {

        if (this.UsersExcelFile === '') {
            Swal.fire({title:'نامعتبر' ,text:'لطفاً فایل را آپلود کنید.', icon:'warning', confirmButtonText:'تایید'})
            return ;
        }
        else if(this.UsersExcelFile.type !== 'text/csv'){
            Swal.fire({title:'نامعتبر' ,text:'فرمت فایل باید csv. باشد', icon:'warning', confirmButtonText:'تایید'})
            return ;
        }
        else{
            const fd = new FormData();
            fd.append('UsersExcelFile', this.UsersExcelFile)
            fd.append('karavan_uuid', this.selected_karavan_uuid)
    
            axios.post('/add-new-user-to-karavan', fd).then(response => {

                if (response.data['status-code'] == 201){
                    this.getKaravanUsersInfo(1)
                    Swal.fire({title:'موفقیت آمیز' ,text:'کاربران با موفقیت اضافه شدند', icon:'success', confirmButtonText:'تایید'})
                }
                else if (response.data['result'] == 'no_valid_fullname') {Swal.fire({title:'خطا' ,text:'همه اعضا باید نام و نام خانوادگی و به فارسی داشته باشند' , icon:'error', confirmButtonText:'تایید'})}
            
                else if (response.data['result'] == 'empty_username') {Swal.fire({title:'خطا' ,text:'همه اعضا باید نام کاربری داشته باشند', icon:'error', confirmButtonText:'تایید'})}
                else if (response.data['result'] == 'duplicate_username' ) {Swal.fire({title:'خطا' ,text:'نام کاربری ' + response.data['username'] + ' از قبل در سیستم وجود دارد ', icon:'error', confirmButtonText:'تایید'})}
                else if (response.data['result'] == 'length_username') {Swal.fire({title:'خطا' ,text:'نام کاربری ' + response.data['username'] + ' معتبر نمی باشد. نام کاربری باید بین 3 تا 20 کاراکتر باشد ' , icon:'error', confirmButtonText:'تایید'})}
                else if (response.data['result'] == 'char_username') {Swal.fire({title:'خطا' ,text:'نام کاربری ' + response.data['username'] + ' معتبر نیست.نام کاربری فقط می تواند شامل حروف کوچک و بزرگ انگلیسی و اعداد و نقطه و زیرخط(آندرلاین) باشد', icon:'error', confirmButtonText:'تایید'})}
            
                else{ Swal.fire({title:'خطا' ,text:'خطای نامشخص', icon:'error', confirmButtonText:'تایید'}) }
                })
            }
    }
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
        this.$nextTick(() => {
            new DataTable('#users_info_table',{
                "bPaginate": false,
                "bLengthChange": false,
                "bFilter": true,
                "bInfo": false,
                "searching": false,
                "ordering": false,
                retrieve: true,
                language : {
                    "zeroRecords": " "
                },
            });
        })
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
            this.getKaravansName();
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
        

        manager_karavans_info: '',
        users_info:'' ,

        //  Sign in/up manager Info
        username: '',
        password: '',
        fullname: '',


        // search-bar
        search_bar_val: null,

        // count of the current manager_panel pages for pagination
        pages: '',
        activeIndexPage: '',

        // selected karavan name
        selected_karavan_uuid: '',

        // selected time to filter by time for all panels
        selected_time: 'all',
        user_locations_selected_time: 'all',
        selected_event: 'all',

        map: null,
        marker: null,
        shipLayer: null,
        show_location: '',

        souvenir_photos: '',
        registered_locations: '',
        show_all_users_locations_on_map: false,
        show_all_users_souvenir_album: false,

        userAllLocations: '',

        UsersExcelFile: '',

        map_icons_name:[
                        'pink2.png', 'purple.png', 'brown.png', 
                        'yellow.png', 'white.png', 'gray.png',
                        'black.png', 'red.png', 'orange.png', 'blue.png',
                        'green.png', 'orange2.png','caribbean-blue.png', 'pink.png', 
                        ]
    } },
    
    delimiters: ["${", "}$"],    
    methods:app_methods,
    
}).mount('#app')