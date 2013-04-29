// -----------------------------
// CREATION D'UN CONTACT
// -----------------------------

function creationformulaire() {

    Ext.QuickTips.init();

    var Store_typ_contact = new Ext.data.ArrayStore({
        fields:['idtypctc','type_ctc'],
        data:[['PRO','Professionnel'],['PERSO','Personnel'],['VIP','VIP'],['AUTRE','Autre']]
    });

    // Necessaire pour utiliser le CRSF de django
    // sinon Erreur 403
    // On recupere la valeur du cookie csrftoken
    var CSRF_TOKEN = Ext.util.Cookies.get('csrftoken');

    var formulaire = new Ext.FormPanel({
		url: '/contact/cr/',
	renderTo: Ext.getBody(),
	frame: true,
	title: 'NOUVEAU CONTACT',
	width: 600,
	items: [
	{
	    xtype: 'textfield',
	    fieldLabel: 'Code Contact',
	    name: 'cod_contact',
	    allowBlank: false
	},{
	    xtype: 'textfield',
	    fieldLabel: 'Nom du contact',
	    name: 'nom_contact',
	    allowBlank: false
	},{
	    xtype: 'textfield',
	    fieldLabel: 'Téléphone',
	    name: 'tel_contact',
	    allowBlank: true
	},{
	    xtype: 'combo',
	    fieldLabel: 'Type de Contact',
        mode: 'local',
	    hiddenName: 'typ_contact',
	    //name: 'typ_contact',
        store: Store_typ_contact,
        displayField: 'type_ctc',
        valueField: 'idtypctc',
	    allowBlank: true
	},{
	    xtype: 'textarea',
	    fieldLabel: 'Description',
	    name: 'description',
        width: 300,
	    allowBlank: true
	},{
	    xtype: 'textfield',
        hidden: true,
        name: 'csrfmiddlewaretoken',
	}],
	buttons: [{
	    text: 'Validation',
	    handler: function() {
			formulaire.getForm().submit({
				success: function(form, action){ 
                    Ext.Msg.alert('Success', 'ça marche !'); 
                    },
				failure: function(form, action){ 
                    Ext.Msg.alert('Failure', action.success+'/'+action.errmsg); 
                    }
			});
		}
	    },{ 
	    text: 'Annulation',
	    handler: function() { 
            // on part sur une autre page
            var redirect = '/contact';
            window.location = redirect;
	    }
	    },{ 
	    text: 'Reset',
	    handler: function() { 
            alert("RESET");
	    }
	    }]  
        }); 

    // on renseigne des valeurs par defaut
    // Le fameux CSRF_TOKEN par exemple ...
	formulaire.getForm().findField('csrfmiddlewaretoken').setValue(CSRF_TOKEN);
    //alert('ALERT'+CSRF_TOKEN);
}

Ext.onReady(creationformulaire);                                                                      
