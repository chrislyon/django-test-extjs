Ext.define('AM.store.Users', {
	    extend: 'Ext.data.Store',
	    model: 'AM.model.User',
	    autoLoad: true,

	    proxy: {
			type: 'ajax',
			// Mettre ici le lien django
	        url: '/static/t2/account_manager/data/users.json',
	        reader: { type: 'json', root: 'users', successProperty: 'success' }
		}
});
