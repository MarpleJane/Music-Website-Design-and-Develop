var navHTML = "\
    <div class=""layout"">\
      <layout>\
        <i-header>\
          <i-menu mode=""horizontal"" theme=""dark"">\
            <div class=""layout-logo""></div>\
            <div class=""layout-nav"">\
              <menu-item name=""signin"">\
                登录\
              </menu-item>\
              <menu-item name=""signup"">\
                注册\
              </menu-item>\
            </div>\
          </i-menu>\
        </i-header>\
      </layout>\
    </div>"

document.getElementById("nav").innerHTML = navHTML

define(["Vue", "VueRouter"], function(Vue, VueRouter) {
	var Component = Vue.extend(navData);
	new Component().$mount("#nav");
})
