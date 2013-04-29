//
// LISTE CONTACT + EXTJS + CRSF_DJANGO
//

//image path
var IMG_MODIF = '/static/static/img/document-edit.png';
var IMG_DELETE = '/static/static/img/edit-delete.png';

//renderer function
//Pour affichage d'un lien sur une image (modif + effacement)
//
 function renderIcon_mod(val) {
	 return '<a href="/testl/mod/'+val+'"><img src="' + IMG_MODIF + '"></a>';
 }
 function renderIcon_del(val) {
	 return '<a href="/testl/del/'+val+'"><img src="' + IMG_DELETE + '"></a>';
 }

Ext.onReady(function(){
	   
	var limitParPage = 15;

	var mesChampsDeDonnees = [];

	var toto = Ext.Ajax.request({ url: '/testl/champ_liste/',
			success: function(response){
					mesChampsDeDonnees = Ext.decode(response.responseText);
					},
			failure: function(response){ 
					Ext.Msg.alert('CHAMPS DE DONNEES', 'ERREUR RECUPERATION'+response.responseText); }
	        });

	Ext.Msg.alert('CHAMPS DE DONNEES', mesChampsDeDonnees);
	Ext.Msg.alert('TOTO', toto);

	var monStore = new Ext.data.JsonStore({
		root: 'rows',
		idProperty: 'id',
		fields:mesChampsDeDonnees,
		remoteSort : true,
		autoLoad:{
					params:{
						limit:limitParPage,
		            }
				},
		url:'/testl/liste',
		sortInfo:{
			"field": "id",
			"direction": "ASC"
			}
	});

	// Necessaire pour utiliser le CRSF de django
	// sinon Erreur 403
	// On recupere la valeur du cookie csrftoken
	var CSRF_TOKEN = Ext.util.Cookies.get('csrftoken');
	// et on ajoute ce token dans les parametres transmis
	// a chaque requete
	monStore.setBaseParam('csrfmiddlewaretoken', CSRF_TOKEN );

    // Description des colonnes de la grille
	var mesColonnes = [
			{header: 'Id', width: 20, dataIndex: 'id',sortable: true},
			{header: 'Code', width: 100, dataIndex: 'cod_contact',sortable: true},
			{header: 'Nom', width: 200, dataIndex: 'nom_contact',sortable: true},
			{header: 'Tel', width: 200, dataIndex: 'tel_contact',sortable: true},
			{header: 'Type', width: 100, dataIndex: 'typ_contact',sortable: true},
			{header: 'Edit', width: 50, dataIndex: 'id',sortable: false, renderer: renderIcon_mod },
			{header: 'Delete', width: 50, dataIndex: 'id',sortable: false, renderer: renderIcon_del }
		];

     // L'objet pagination en bas de grille
	 var maPagination = new Ext.PagingToolbar({
		         store: monStore,  
		         pageSize: limitParPage,
		         displayInfo: true    
		     });

    // La description de la grille
	var monGridPanel = new Ext.grid.GridPanel({
		viewConfig: {
			forceFit: true
		},
		// sinon pas de scrolling vertical
		autoHeight:false,
		renderTo:Ext.getBody(),
		store: monStore,
		columns:mesColonnes,
		tbar: new Ext.Toolbar(),
		width: 800,
		height: 500,
		frame: true,
		title: 'Liste des contacts',
		bbar: maPagination
	});

    //
    // Toolbar avec
    // HOME => Retour a l'accueil
    // NEW  => Nouveau contact
    // PRINT => Liste des contacts
    //
	var toolbar = monGridPanel.getTopToolbar();
	    toolbar.add(new Ext.Toolbar.Button({
						text:'HOME',
						handler: function(){
								       Ext.Msg.alert('BUTTON', 'HOME');
									      }
						}
						));  

	    toolbar.add(new Ext.Toolbar.Button({
						text:'NEW',
						handler: function(){
                                          window.location = '/testl/cr';
									      }
						}
						));  

	    toolbar.add(new Ext.Toolbar.Button({
						text:'PRINT',
						handler: function(){
								       Ext.Msg.alert('BUTTON', 'PRINT');
									      }
						}
						));  

	monGridPanel.show();
}); 
