### ------------------
### FORMULAIRE EXTJS
### ------------------

##
## Probleme avec extjs 4
## => Dans la gestion des boutons
## si j'ai une redirection apres un message 
## alors pas d'attente pour le msg.alert

import sys
from django.utils import simplejson

class ExtForm(object):
    """
    La classe pour les formulaires
    """
    def __init__(self, mode='cr'):
        self.titre = "TITRE A CHANGER"
        self.width = 600
        self.height = 300
        self.bodyPadding = 10
        self.renderTo = 'Ext.getBody()'
        self.mode = mode
        self.url = '/'
        self.url_annul = '/'
        self.defaultType = 'textfield'
        self.zones = []
        self.dzones = {}
        self.data = []

    def add_zone(self, zone):
        self.zones.append(zone)
        self.dzones[zone.name] = zone

    def mod_zone(self, k, attr, val):
        if k in self.dzones:
            t = self.dzones[k]
            try:
                setattr(t, attr, val)
            except:
                pass

    def liste_zones(self):
        return ",".join([ c.to_form() for c in self.zones ])

    def render(self):
        F_DEBUT = """
        Ext.require('Ext.form.Panel');
        Ext.require('Ext.form.field.Date');
        Ext.onReady(function() {
        var CSRF_TOKEN = Ext.util.Cookies.get('csrftoken');
        Ext.tip.QuickTipManager.init();  // enable tooltips
        """

        S = ""
        S += "var form = new Ext.form.Panel({"
        S += "renderTo: %s, " % self.renderTo
        S += "url: '%s', " % self.url
        S += "height: %s, " % self.height
        S += "width: %s, " % self.width
        S += "frame: true, "
        S += "bodyPadding: %s, " % self.bodyPadding
        S += "title: '%s', " % self.titre
        S += "defaultType: '%s', " % self.defaultType

        S += """
            items: [
            """
        S += self.liste_zones()
        S += """
            ],
            baseParams: {'csrfmiddlewaretoken':CSRF_TOKEN},
        buttons: [
        """
        if self.mode == 'del':
            S += """
            {
                text: 'Confirmer la suppression',
                    formBind: true,
                    handler: function(){
                            var form = this.up('form').getForm(); // get the basic form
                            if(form.isValid()){
                                    form.submit({
                                            url: '%s/',
                                            //waitMsg: 'Submitting your data...',
                                            success: function(form, action){
                                                // server responded with success = true
                                                // var result = action.result;
                                                alert("Effacement Confirme");
                                                var redirect = '%s';
                                                window.location = redirect;
                                                },
                                            failure: function(form, action){
                                                if (action.failureType === Ext.form.action.Action.CONNECT_FAILURE) {
                                                    Ext.Msg.alert('Error',
                                                        'Status:'+action.response.status+': '+
                                                        action.response.statusText);
                                                    }
                                                if (action.failureType === Ext.form.action.Action.SERVER_INVALID){
                                                    // server responded with success = false
                                                    Ext.Msg.alert('Invalid', action.result.errormsg);
                                                    }
                                                }
                                            })
                                }
                            }
            """ % ( self.url, self.url_annul )
        else:
            S += """
                {
                    text: 'Submit',
                    handler: function() {
                        var form = this.up('form').getForm(); // get the basic form
                        if (form.isValid()) { // make sure the form contains valid data before submitting
                            form.submit({
                            success: function(form, action) {
                                Ext.Msg.alert('Success', action.result.msg);
                            },
                            failure: function(form, action) {
                            Ext.Msg.alert('Failed', "Erreur : "+action.response.responseText);
                            }
                            });
                        } else { // display error alert if the data is invalid
                            Ext.Msg.alert('Invalid Data', 'Please correct form errors.')
                        }
                    }
                """
                #""" % self.url_annul
        ## Dans tout les cas
        S += """
                },{ 
                    text: 'Annulation',
                    handler: function() { 
                        // on part sur une autre page
                        var redirect = '%s';
                        window.location = redirect;
                        }
                }
            ]
            });
        """ % self.url_annul
        for z in self.zones:
            if z.def_value:
                S += "form.getForm().findField('%s').setValue('%s');\n" % (z.name, z.def_value)
        F_FIN = "});"
        return F_DEBUT+S+F_FIN

class ZBox(object):
    """
        Container de zone
    """
    def __init__(self, name, **kwargs):
        self.name = name
        self.title = name
        self.layout = kwargs.get('layout','hbox')
        self.xtype = kwargs.get('xtype','container')
        self.hideLabel = kwargs.get('hideLabel',False)
        self.zones = []
        self.def_value = False
        self.dzones = {}

    def add_zone(self, zone):
        self.zones.append(zone)
        self.dzones[zone.name] = zone

    def mod_zone(self, k, attr, val):
        if k in self.dzones:
            t = self.dzones[k]
            try:
                setattr(t, attr, val)
            except:
                pass

    def to_form(self):
        R = ''
        R += "{ xtype: '%s', defaultType: 'textfield', layout: '%s'," % (self.xtype, self.layout)
        R += """
            items: [
            """
        R +=  ",".join([ c.to_form() for c in self.zones ])
        if self.hideLabel:
            R += """
                ],
                """
            R += " defaults: { hideLabel: 'true' }"
        else:
            R += """
                ]
                """
        R += "}"
        return R


class Zone(object):
    """
        Zone/Champ du formulaire
    """
    def __init__(self, name, **kwargs):
        self.name = name
        self.fieldLabel = kwargs.get('fieldLabel', 'Zone %s ' % name )
        self.width = kwargs.get('width',200)
        self.height = kwargs.get('height',None)
        self.hidden = kwargs.get('hidden', False)
        self.readOnly = kwargs.get('readOnly', False)
        self.xtype = kwargs.get('xtype', None)
        self.data = kwargs.get('data', None)
        self.def_value = kwargs.get('def_value', None)

    def data_to_json(self):
        T =  ','.join([ "{value:'%s',display:'%s'}" % d for d in self.data ])
        return T

    def to_form(self):
        if self.xtype == "combo":
            d = """
            Ext.create('Ext.form.field.ComboBox', { 
                    fieldLabel: '%s', 
                    name:'%s', 
                    store: {
                        fields: ['value', 'display'],
                        data : [ %s ]
                        },
                    queryMode: 'local',
                    displayField: 'display',
                    readOnly: %s,
                    valueField: 'value',
                    value: '%s'
                    })
            """ % ( self.fieldLabel, self.name, self.data_to_json(), str(self.readOnly).lower(), self.def_value )
            return d
        elif self.xtype == 'htmleditor':
            d = """
            Ext.create('Ext.form.field.HtmlEditor', { 
                    fieldLabel: '%s', 
                    name:'%s', 
                    width: %s,
                    height: %s,
                    readOnly: %s
                    })
            """ % ( self.fieldLabel, self.name, self.width, self.height, str(self.readOnly).lower() )
            return d
        else:
            d = { 'fieldLabel':self.fieldLabel, 'name':self.name, 'width': self.width, 'readOnly':self.readOnly }
        return simplejson.dumps(d)


def test():

    TYP_CTC = ( 
            ( 'PRO', 'PROFESSIONEL'),
            ( 'PERSO', 'PERSONNEL' ),
            ( 'VIP', 'VIP'),
            ( 'AUTRE', 'AUTRE'),
    )

    

    #print simplejson.dumps(T)
    #sys.exit()

    f = ExtForm()
    f.add_zone(Zone( 'Nom' ))
    f.add_zone(Zone( 'prenom', fieldLabel="Prenom" ))
    f.add_zone(Zone( 'description', fieldLabel="Commentaire" ))
    f.add_zone(Zone( 'typ_contact', fieldLabel="Type Contact", xtype='combo', data = TYP_CTC ))
    ZB = ZBox( 'Tags en Hbox', layout='hbox' )
    ZB.add_zone(Zone( 'Tag1', fieldLabel="Tag1" ))
    ZB.add_zone(Zone( 'Tag1', fieldLabel="Tag2" ))
    ZB.add_zone(Zone( 'Tag1', fieldLabel="Tag3" ))
    f.add_zone(ZB)
    print f.render()


if __name__ == "__main__":
    test()
