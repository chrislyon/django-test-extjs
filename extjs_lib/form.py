### ------------------
### FORMULAIRE EXTJS
### ------------------

import sys
from django.utils import simplejson

class ExtForm(object):
    """
    La classe pour les formulaires
    """
    def __init__(self):
        self.titre = "TITRE A CHANGER"
        self.width = 600
        self.height = 300
        self.bodyPadding = 10
        self.renderTo = 'Ext.getBody()'
        self.mode = 'cr'
        self.url = '/'
        self.url_annul = '/'
        self.defaultType = 'textfield'
        self.zones = []
        self.data = []

    def add_zone(self, zone):
        self.zones.append(zone)

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
        S += "Ext.create('Ext.form.Panel', {"
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
                            Ext.Msg.alert('Failed', "ERREUR DJANGO");
                        }
                        });
                    } else { // display error alert if the data is invalid
                        Ext.Msg.alert('Invalid Data', 'Please correct form errors.')
                    }
                }
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
        F_FIN = "});"
        return F_DEBUT+S+F_FIN

class Zone(object):
    """
        Zone/Champ du formulaire
    """
    def __init__(self, name, **kwargs):
        self.name = name
        self.fieldLabel = kwargs.get('fieldLabel', 'Zone %s ' % name )
        self.width = kwargs.get('width',100)
        self.height = kwargs.get('width',None)
        self.hidden = kwargs.get('hidden', False)
        self.xtype = kwargs.get('xtype', None)
        self.data = kwargs.get('data', None)

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
                    valueField: 'value'
                    })
            """ % ( self.fieldLabel, self.name, self.data_to_json() )
            return d
        elif self.xtype == 'htmleditor':
            d = """
            Ext.create('Ext.form.field.HtmlEditor', { 
                    fieldLabel: '%s', 
                    name:'%s', 
                    width: %s,
                    height: %s
                    })
            """ % ( self.fieldLabel, self.name, self.width, self.height )
            return d
        else:
            d = { 'fieldLabel':self.fieldLabel, 'name':self.name }
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
    print f.render()


if __name__ == "__main__":
    test()
