function creationformulaire() {

    Ext.QuickTips.init();

    var formulaire = new Ext.FormPanel({
		url: 'http://localhost:8000/hello_extjs/p1',
	renderTo: Ext.getBody(),
	frame: true,
	title: 'Titre du formulaire',
	width: 400,
	items: [
	{
		hidden: true,				// csrf_token
		contentEl: "hidden-csrf"
	},{
	    xtype: 'textfield',
	    fieldLabel: 'Thème',
	    name: 'theme',
	    allowBlank: false
	},{
	    xtype: 'textfield',
	    fieldLabel: 'Lieu',
	    name: 'lieu',
	    allowBlank: false
	},{
	    xtype: 'datefield',
	    fieldLabel: 'Date',
	    name: 'date'
	}],
	buttons: [{
	    text: 'Sauve',
	    handler: function() {
			formulaire.getForm().submit({
				success: function(form, action){ Ext.Msg.alert('Success', 'ça marche !'); },
				failure: function(form, action){ Ext.Msg.alert('Failure', action.success+'/'+action.errmsg); }
			});
		}
	    },{ 
	    text: 'Annule',
	    handler: function() { 
		// on part sur une autre page
		alert("C'est parti");
		var redirect = 'http://localhost:8000/hello_extjs/';
		window.location = redirect;
	    }
	    },{ 
	    text: 'Reset',
	    handler: function() { 
		alert("RESET");
	    }
	    }]  
        }); 

	formulaire.getForm().findField('theme').setValue('ExtJS');
}

Ext.onReady(creationformulaire);                                                                      
