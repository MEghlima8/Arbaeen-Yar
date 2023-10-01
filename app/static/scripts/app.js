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

app_methods.change_panel = function(panel,manager_panel){
    this.search_bar_val = '',
    this.username = '';
    this.password = '';
    this.fullname = '';
    this.UsersExcelFile = '';
    this.show_location = 'false'
    this.panel = panel;
    this.manager_panel = manager_panel;
    this.show_res_upload_excel = false;

    if (manager_panel != 'registered-locations'){ this.show_all_users_locations_on_map = false };
    if(manager_panel != 'souvenir-photos') { this.show_all_users_souvenir_album = false; }
    
}

app_methods.isActivePanel = function(panel){
    if (this.manager_panel == panel) { return true } else {return false}
}


app_methods.isActivePage = function(index){
    return index === this.activeIndexPage;
}


// Function to generate a random RGB color
app_methods.getRandomColor = function () {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Search with fullname or username
app_methods.onClick_search = function(){
    if (this.search_bar_val != null){
        this.pages = null;
    
        if (this.manager_panel == 'show-all-users-info') {
            this.showAllUsersInfo(1)
        }
        else if (this.manager_panel == 'souvenir-photos'){
            this.getSouvenirPhotos(1);
        }
        else if (this.manager_panel == 'registered-locations'){
            this.getRegisteredLocations(1)
        }
    }
}


app_methods.receivedMessages = function(page){
    if (this.selected_karavan_uuid == ''){
        this.change_panel('manager', 'received-messages')
        return
    }
    this.activeIndexPage = page;
    data = {'karavan_uuid': this.selected_karavan_uuid, 'page_index':page, 'time':this.selected_time, 'search_value':this.search_bar_val}
    axios.post('/get-karavan-messages', data).then(response => {
        if (response.data['status-code'] == 200) {
            this.messages = response.data['result']
            this.pages = response.data['count_pages']
        }
        else{
            this.registered_locations = null;
            this.pages = null;
        }
        this.change_panel('manager', 'received-messages')
    })
}



// retrieve karavan users locations
app_methods.getRegisteredLocations = function(page){
    if (this.selected_karavan_uuid == ''){
        this.change_panel('manager', 'registered-locations')
        return
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


app_methods.getSouvenirPhotos = function(page){
    if (this.selected_karavan_uuid == ''){
        this.change_panel('manager', 'souvenir-photos')
        return
    }
    
    this.activeIndexPage = page;
    data = {'karavan_uuid': this.selected_karavan_uuid, 'page_index':page, 'time':this.selected_time, 'event':this.selected_event, 'search_value':this.search_bar_val}
    axios.post('/get-souvenir-photos', data).then(response => {

        if (response.data['status-code'] == 200) {
            var events;
            this.souvenir_photos = response.data['result']
            events = response.data['events']

            for (var i=0 ; i < this.souvenir_photos.length;i++ ){
                for (var key in events) {
                    if (events[key] === this.souvenir_photos[i][4]['event']) {
                        this.souvenir_photos[i][4]['event']= key;
                    }
                }
            }

            this.karavan_events = response.data['events']
            this.pages = response.data['count_pages']
            this.change_panel('manager', 'souvenir-photos')

            this.$nextTick(() => {
                $(function () {
                    $('#lightgallery').lightGallery({
                        thumbnail: true,
                        selector: 'a'
                    });
                    $('.lightgallery').lightGallery({
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


app_methods.showAllUsersInfo = function(page){
    if (this.selected_karavan_uuid == ''){
        this.change_panel('manager', 'show-all-users-info')
        return
    }
    this.activeIndexPage = page;
    
    data = {'karavan_uuid': this.selected_karavan_uuid, 'page_index':page, 'search_value':this.search_bar_val}
    axios.post('/get-karavan-users-info', data).then(response => {
        
        if (response.data['status-code'] == 200) {
            this.users_info = response.data['result']
            this.pages = response.data['count_pages']
            this.change_panel('manager', 'show-all-users-info')
            }
        else {
            Swal.fire({title:'خطا' ,text:'خطای نامشخص', icon:'error', confirmButtonText:'تایید'})
        }
    })
}


app_methods.edit_user_info_panel = function(user_uuid,fullname,username){
    this.current_user_uuid = user_uuid;
    this.current_user_username = username;
    this.current_user_fullname = fullname;
    this.$nextTick(() => {
        this.username = username;
        this.fullname = fullname;
    })
    this.change_panel('manager','edit-user-info')
}

app_methods.editUserInfo = function(){
    if (this.fullname == '' && this.username == '' && this.password == ''){
        Swal.fire({title:'خطا' ,text:'حداقل یکی از فیلد ها باید پر باشد', icon:'error', confirmButtonText:'تایید'})
        return;
    }
    data = {'fullname':this.fullname, 'username':this.username,
            'password':this.password, 'uuid':this.current_user_uuid}
    axios.post('/edit-user-info', data).then(response => {

        if (response.data['status-code'] == 200){
            Swal.fire({title:'موفق' ,text:'تغییر اطلاعات با موفقیت انجام شد', icon:'success', confirmButtonText:'تایید'});
            this.showAllUsersInfo(1);
        }
        else if (response.data['result'] == 'no_valid_fullname') {Swal.fire({title:'خطا' ,text:'نام و نام خانوادگی را فقط به فارسی وارد کنید', icon:'error', confirmButtonText:'تایید'})}
    
        else if (response.data['result'] == 'empty_username') {Swal.fire({title:'خطا' ,text:'لطفا یک نام کاربری انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'duplicate_username' ) {Swal.fire({title:'خطا' ,text:'نام کاربری وارد شده از قبل در سیستم وجود دارد. لطفا نام کاربری دیگری را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'length_username') {Swal.fire({title:'خطا' ,text:'طول نام کاربری باید بین 3 تا 20 کاراکتر باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'char_username') {Swal.fire({title:'خطا' ,text:'نام کاربری فقط می تواند شامل حروف کوچک و بزرگ انگلیسی و اعداد و نقطه و زیرخط(آندرلاین) باشد', icon:'error', confirmButtonText:'تایید'})}
    
        else{ Swal.fire({title:'خطا' ,text:'خطای نامشخص', icon:'error', confirmButtonText:'تایید'}) }
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

                this.map = L.map('all_users_locs_on_map').setView([this.registered_locations[0][4]['lat'], this.registered_locations[0][4]['lon']], 14);
                
                L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    maxZoom: 19,
                }).addTo(this.map);

                
                for (var i=0 ; i < this.registered_locations.length;i++ ){
                    if (remained_icons.length == 0) { remained_icons = [...this.map_icons_name] }

                    if(this.registered_locations[i][1] in users_icons){
                        // An icon is selected for the user
                        var userIcon = L.icon({iconUrl: './static/css/images/' + users_icons[this.registered_locations[i][1]]['color_icon'],shadowUrl: '/static/css/images/marker-shadow.png',iconSize:[38, 40],shadowSize:[38, 40],});
                        this.marker = L.marker([ this.registered_locations[i][4]['lat'], this.registered_locations[i][4]['lon']],
                        {icon: userIcon}).addTo(this.map);
                        users_icons[this.registered_locations[i][1]]['coordinates'].push(this.marker.getLatLng())
                    }

                    // Select an icon for the user
                    else{
                        users_icons[this.registered_locations[i][1]] = {}
                        users_icons[this.registered_locations[i][1]]['color_icon'] = remained_icons.pop();
                        users_icons[this.registered_locations[i][1]]['coordinates'] = []
                        //  Ex: users_icons['username'] = {'color_icon':icon, 'coordinates':[]}
                        var userIcon = L.icon({iconUrl: './static/css/images/' + users_icons[this.registered_locations[i][1]]['color_icon'],shadowUrl: '/static/css/images/marker-shadow.png',iconSize:[38, 40],shadowSize:[38, 40],});
                        
                        this.marker = L.marker([ this.registered_locations[i][4]['lat'], this.registered_locations[i][4]['lon']],
                        {icon: userIcon}).addTo(this.map);
                        users_icons[this.registered_locations[i][1]]['coordinates'].push(this.marker.getLatLng())

                    }
                    this.marker.bindPopup(
                        "<h6>نام: " + this.registered_locations[i][0] + "</h6>" +
                        "<h6>طول جغرافیایی: " + this.registered_locations[i][4]['lon'] + "</h6>" +
                        "<h6>عرض جغرافیایی: " + this.registered_locations[i][4]['lat'] + "</h6>" +
                    "<div style='margin-bottom: 5px;'></div>" + "<h6>تاریخ: " + this.registered_locations[i][3]['date'] + "</h6>" +
                    "<div style='margin-bottom: 5px;'></div>" + "<h6>زمان: " + this.registered_locations[i][3]['time'] + "</h6>"
                    );
                }
                for (const key in users_icons) {
                    L.polyline(users_icons[key]['coordinates'], {color: this.getRandomColor()}).addTo(this.map);
                };
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
                
                this.map = L.map('user_all_locs_map').setView([this.userAllLocations[0][2]['lat'], this.userAllLocations[0][2]['lon']], 14);
                L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    maxZoom: 19,
                }).addTo(this.map);
                
            
                var blueIcon = L.icon({iconUrl: './static/css/images/blue.png',shadowUrl: '/static/css/images/marker-shadow.png',
                iconSize:[38, 40],shadowSize:[38, 40],
                });
            
                // Define an array of LatLng points for the polyline
                var latlngs = [];

                this.marker = L.marker([this.userAllLocations[0][2]['lat'], this.userAllLocations[0][2]['lon']]).addTo(this.map);
                latlngs.push(this.marker.getLatLng())

                this.marker.bindPopup(
                                "<h6>طول جغرافیایی: " + this.userAllLocations[0][2]['lon'] + "</h6>" +
                                "<h6>عرض جغرافیایی: " + this.userAllLocations[0][2]['lat'] + "</h6>" +
                                "<h6>تاریخ: " + this.userAllLocations[0][3]['date'] + "</h6>" +
                                "<h6>زمان: " + this.userAllLocations[0][3]['time'] + "</h6>"
                                );
                            
                if (this.userAllLocations.length != 1){
                    for (var i=1 ; i < this.userAllLocations.length;i++ ){
                        this.marker = L.marker([ this.userAllLocations[i][2]['lat'], this.userAllLocations[i][2]['lon']], {icon: blueIcon}).addTo(this.map);
                        latlngs.push(this.marker.getLatLng())

                        this.marker.bindPopup(
                        "<h6>طول جغرافیایی: " + this.userAllLocations[i][2]['lon'] + "</h6>" +
                        "<h6>عرض جغرافیایی: " + this.userAllLocations[i][2]['lat'] + "</h6>" +
                        "<h6>تاریخ: " + this.userAllLocations[i][3]['date'] + "</h6>" +
                        "<h6>زمان: " + this.userAllLocations[i][3]['time'] + "</h6>"
                        );
                    }
                    // Create a polyline and add it to the map
                    L.polyline(latlngs, {color: 'red'}).addTo(this.map);
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


app_methods.showLocation = function(lon,lat){
    if (this.show_location == 'true'){
        this.show_location = 'false';
    }
    else {
        this.show_location = 'true';
        this.$nextTick(() => {
            var map = L.map('map').setView([lat, lon ], 14);
            
            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19,
            }).addTo(map);
            this.marker = L.marker([lat, lon]).addTo(map);
            this.marker.bindPopup(
            "<h6>طول جغرافیایی: " + lon + "</h6>" +
            "<h6>عرض جغرافیایی: " + lat + "</h6>"
            );

        })
    }
}


app_methods.addManagerToKaravan = function(){
    if (this.selected_karavan_uuid == ''){
        Swal.fire({title:'خطا' ,text:'ابتدا کاروان مورد نظر خود را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})
        return;
    }

    Swal.fire({
        title: 'نام کاربری مدیر مورد نظر را وارد کنید',
        input: 'text',
        inputPlaceholder: 'مثال : m_eghlima8',
      }).then( (input) => {
          
        data = {'input_manager_username': input.value, 'karavan_uuid': this.selected_karavan_uuid}
        if (input.value != null && input.value != ''){
            axios.post('/add-manager-to-karavan', data).then(response => {
                if (response.data['status-code'] == 200){
                    Swal.fire({title:'موفقیت آمیز' ,text:'این کاربر به عنوان مدیر به کاروان اضافه شد', icon:'success', confirmButtonText:'تایید'})
                }
                else {
                    Swal.fire({title:'ناموفق' ,text:'چنین نام کاربری وجود ندارد یا این نام کاربری متعلق به یک عضو کاروان می باشد نه یک مدیر', icon:'error', confirmButtonText:'تایید'})
                }
            })
        }
})}


app_methods.addUserToKaravan = function(){
    this.change_panel('manager', 'add-user-to-karavan');
}

app_methods.handleExcelFile = function(event){
    this.UsersExcelFile = event.target.files[0]
}

app_methods.sendUserInfoToAddToKaravan = function(type){

    if (type == 'input'){
        if (this.fullname == '' || this.username == '' || this.password == ''){
            Swal.fire({title:'خطا' ,text:'لطفا همه ی فیلد ها را پر کنید', icon:'error', confirmButtonText:'تایید'})
            return;
        }

        data = {'fullname': this.fullname ,'username': this.username, 'password':this.password ,'karavan_uuid': this.selected_karavan_uuid}
        axios.post('/add-new-user-to-karavan', data).then(response => {  
        if (response.data['status-code'] == 201){
            this.showAllUsersInfo(1)
            Swal.fire({title:'موفقیت آمیز' ,text:'کاربر با موفقیت اضافه شد', icon:'success', confirmButtonText:'تایید'})
        }
        else if (response.data['result'] == 'no_valid_fullname') {Swal.fire({title:'خطا' ,text:'نام و نام خانوادگی را فقط به فارسی وارد کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'empty_fullname') {Swal.fire({title:'خطا' ,text:'لطفا نام و نام خانوادگی خود را وارد کنید', icon:'error', confirmButtonText:'تایید'})}

        else if (response.data['result'] == 'empty_password') {Swal.fire({title:'خطا' ,text:'لطفا یک رمز عبور انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'char_password') {Swal.fire({title:'خطا' ,text:'طول رمز عبور باید بیشتر از 8 کاراکتر و فقط شامل حرف کوچک انگلیسی و کاراکتر خاص و عدد باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'used_info_in_password') {Swal.fire({title:'خطا' ,text:'رمز عبور شما مطابقت زیادی با ایمیل یا نام کاربری تان دارد. لطفا رمز عبور دیگری را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        
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
                if (response.data['status-code'] == 422){
                    Swal.fire({title:'نامعتبر' ,text:'لطفا فایل نمونه را مشاهده و طبق آن اطلاعات را ارسال کنید', icon:'error', confirmButtonText:'تایید'})
                    return
                }
                this.res_upload_excel_href = response.data['path_result_excel']
                
                Swal.fire({
                    title: 'فایل دریافت شد',
                    text: 'جهت دانلود و مشاهده نتیجه بر روی تایید کلیک کنید',
                    icon: 'success',
                    confirmButtonText: 'تایید',
                  }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = this.res_upload_excel_href;
                    }
                });
                this.showAllUsersInfo(1)
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


app_methods.addEventToKaravan = function(){
    if (this.selected_karavan_uuid == ''){
        Swal.fire({title:'خطا' ,text:'ابتدا کاروان مورد نظر خود را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})
        return;
    }

    Swal.fire({
        title: 'یک نام برای رویداد انتخاب کنید',
        input: 'text',
        inputPlaceholder: 'مثال : اربعین',
      }).then( (input) => {
          
        data = {'event_name': input.value, 'karavan_uuid': this.selected_karavan_uuid}
        if (input.value != null && input.value != ''){
            axios.post('/add-event-to-karavan', data).then(response => {  
                if (response.data['status-code'] == 200){
                    Swal.fire({title:'ثبت رویداد' ,text:'رویداد جدید با موفقیت اضافه شد', icon:'success', confirmButtonText:'تایید'})
                }
                else {
                    Swal.fire({title:'ناموفق' ,text:'نام رویداد تکراری است. لطفا نام دیگری را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})
                }
            })
        }
})}


app_methods.showKaravanManagers = function(page){
    if (this.selected_karavan_uuid == ''){
        Swal.fire({title:'خطا' ,text:'ابتدا کاروان مورد نظر خود را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})
        return;
    }
    data = {'page_index':page, 'karavan_uuid': this.selected_karavan_uuid}
    this.activeIndexPage = page;

    axios.post('/get-karavan-managers', data).then(response => { 
        if (response.data['status-code'] == 200){
            this.karavan_managers = response.data['result']
            this.change_panel('manager', 'karavan-managers')
            this.pages = response.data['count_pages']
        }
    })

}


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
            this.static_fullname = response.data['fullname'];
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
    if (this.fullname == '' || this.username == '' || this.password ==''){
        Swal.fire({title:'خطا' ,text:'لطفا همه ی فیلد ها را پر کنید', icon:'error', confirmButtonText:'تایید'})
        return;
    }
    var data = {'fullname' : this.fullname,'username' : this.username,'password' : this.password,}    

    axios.post('/signup-manager', data).then(response => {  
        if (response.data['status-code'] == 201) { 
            //  Signup was succesful
            Swal.fire({title:'تایید ثبت نام' ,text:'ثبت نام با موفقیت انجام شد. حالا می توانید وارد حساب کاربری خود شوید', icon:'success', confirmButtonText:'تایید'})
            this.change_panel('sign-in',null)
        }        
        else if (response.data['result'] == 'no_valid_fullname') {Swal.fire({title:'خطا' ,text:'نام و نام خانوادگی خود را فقط به فارسی وارد کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'empty_fullname') {Swal.fire({title:'خطا' ,text:'همه باید نام و نام خانوادگی شان ثبت شده باشد', icon:'error', confirmButtonText:'تایید'})}

        else if (response.data['result'] == 'empty_password') {Swal.fire({title:'خطا' ,text:'همه باید رمز عبور داشته باشند', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'char_password') {Swal.fire({title:'خطا' ,text:'طول رمز عبور باید بیشتر از 8 کاراکتر و فقط شامل حرف کوچک انگلیسی و کاراکتر خاص و عدد باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'used_info_in_password') {Swal.fire({title:'خطا' ,text:'رمز عبور شما مطابقت زیادی با نام کاربری تان دارد. لطفا رمز عبور دیگری را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        
        else if (response.data['result'] == 'empty_username') {Swal.fire({title:'خطا' ,text:'همه اعضا باید نام کاربری داشته باشند', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'duplicate_username' ) {Swal.fire({title:'خطا' ,text:'نام کاربری وارد شده از قبل در سیستم وجود دارد. لطفا نام کاربری دیگری را انتخاب کنید', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'length_username') {Swal.fire({title:'خطا' ,text:'طول نام کاربری شما باید بین 3 تا 20 کاراکتر باشد', icon:'error', confirmButtonText:'تایید'})}
        else if (response.data['result'] == 'char_username') {Swal.fire({title:'خطا' ,text:'نام کاربری فقط می تواند شامل حروف کوچک و بزرگ انگلیسی و اعداد و نقطه و زیرخط(آندرلاین) باشد', icon:'error', confirmButtonText:'تایید'})}
        else{ Swal.fire({title:'خطا' ,text:'خطای نامشخص', icon:'error', confirmButtonText:'تایید'}) }
    })
};


app_methods.changeUserAccountStatus = function(user_uuid, new_status){
    data = {'user_uuid':user_uuid, 'new_status':new_status, 
            'karavan_uuid':this.selected_karavan_uuid, 'page_index':this.activeIndexPage}

    axios.post('/change-account-status', data).then(response => {
        if (response.data['status-code'] == 200){
            this.users_info = response.data['result']
            this.pages = response.data['count_pages']
        }
    })
}


app_methods.changeSelectedKaravan = function(){
    if (this.selected_karavan_uuid == ''){return;}

    switch(this.manager_panel){
        case 'manager-dashboard':
            this.getKaravanGeneralInfo();
            return;
        case 'show-all-users-info':
            this.showAllUsersInfo(1);
            return;
        case 'souvenir-photos':
            this.getSouvenirPhotos(1);
            return;
        case 'registered-locations':
            this.getRegisteredLocations(1);
            return;
        case 'add-user-to-karavan':
            this.addUserToKaravan();
            return;
        case 'karavan-managers':
            this.showKaravanManagers(1);
            return;
    }

    if(this.manager_panel == 'manager-dashboard'){ this.getKaravanGeneralInfo() }
    else if(this.manager_panel == 'show-all-users-info'){ this.showAllUsersInfo(1) }
    else if(this.manager_panel == 'souvenir-photos'){ this.getSouvenirPhotos(1) }
    else if(this.manager_panel == 'registered-locations'){ this.getRegisteredLocations(1) }
    else if(this.manager_panel == 'add-user-to-karavan'){ this.addUserToKaravan() }
}


app_methods.getKaravanGeneralInfo = function(){
    this.change_panel('manager', 'manager-dashboard')
    if (this.selected_karavan_uuid == ''){
        return
    }

    data = {'karavan_uuid': this.selected_karavan_uuid}
    axios.post('/get-karavan-general-info', data).then(response => {
        if (response.data['status-code'] == 200){
            this.count_karavan_locations = response.data['type']['/send-my-location']
            this.count_karavan_souvenir_photos = response.data['type']['/souvenir-photo']
            
            this.count_karavan_active_accounts = response.data['account']['active']
            this.count_karavan_no_active_accounts = response.data['account']['noactive']


            $("#donut_chart").empty();
            Morris.Donut({
                element: 'donut_chart',
                data: [
                    {
                        label: 'حساب های فعال',
                        value: this.count_karavan_active_accounts
                    },
                    {
                        label: 'حساب های غیرفعال',
                        value: this.count_karavan_no_active_accounts
                    },
                ],
                colors: ['rgb(0, 188, 212)', 'rgb(233, 30, 99)'],
                formatter: function (y) {
                    return y + ' حساب '
                },
            });

        }
    });  
}



app_methods.gallery_image_description = function(fullname, username, date, time){
    return 'نام: ' + fullname + '  |  نام کاربری: ' + username + 
           '  |  تاریخ: ' + date + '  |  زمان: ' + time
}


Vue.createApp({
    data(){ return {        
        panel: 'sign-in',
        manager_panel: '',

        manager_karavans_info: '',
        users_info:'' ,
        karavan_name: '',
        karavan_managers: '',
        
        karavan_events: '',

        //  Sign in/up Info
        username: '',
        password: '',
        fullname: '',

        // Signin manager
        static_fullname: '',

        // Handle user to edit info
        current_user_uuid: null,
        current_user_fullname: null,
        current_user_username: null,

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

        show_res_upload_excel: false,
        res_upload_excel_href: '',

        // Information for dashboard panel
        count_karavan_souvenir_photos: 0,
        count_karavan_locations: 0,
        count_karavan_active_accounts: 0,
        count_karavan_no_active_accounts: 0,

        // To add event to karavan
        event_name: '',

        // Karavan messages
        messages: '',

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