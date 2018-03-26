// require.config({
// 	path: {
// 		"Vue": "../vue/vue.js",
// 		"VueResource": "../vue/vue.js",
// 		"VueRouter": "../vue/vue-router@3.0.1.js",
// 		"Iview": "../iview/iview2.9.2.min.js"
// 	}
// })

require.config({
	baseUrl: "statics/js"
	path: {
		"Vue": "vue/vue",
		"VueResource": "vue/vue-resource",
		"VueRouter": "vue/vue-router@3.0.1",
		"Iview": "iview/iview2.9.2.min",
		"Nav": "components/nav"
	},
	shim: {
		Vue: {
			exports: "Vue"
		},
		Iview: {
			deps: ["Vue"],
			exports: "Iview"
		},
		VueResource: {
			deps: ["Vue"],
			exports: "VueResource"
		},
		VueRouter: {
			deps: ["Vue"],
			exports: "VueRouter"
		}
	}
})