
### ------------------
### FORMULAIRE EXTJS
### ------------------

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
        Ext.create('Ext.form.Panel', {
        """
        S = ""
        S += "renderTo: %s, " % self.renderTo
        S += "url: '%s', " % self.url
        S += "height: %s, " % self.height
        S += "width: %s, " % self.width
        S += "bodyPadding: %s, " % self.bodyPadding
        S += "title: '%s', " % self.titre
        S += "defaultType: '%s', " % self.defaultType

        S += """
            items: [
            """
        S += self.liste_zones()
        S += """
            ],
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
                            Ext.Msg.alert('Failed', action.result.msg);
                        }
                        });
                    } else { // display error alert if the data is invalid
                        Ext.Msg.alert('Invalid Data', 'Please correct form errors.')
                    }
                }
            }
            ]
            });
        """
        F_FIN = "});"
        return F_DEBUT+S+F_FIN

class Zone(object):
    """
        Colonne de la grille
    """
    def __init__(self, name, **kwargs):
        self.name = name
        self.fieldLabel = kwargs.get('fieldLabel', 'Zone %s ' % name )
        self.width = kwargs.get('width',100)
        self.hidden = kwargs.get('hidden', False)
        self.xtype = kwargs.get('xtype', None)

    def to_form(self):
        d = { 'fieldLabel':self.fieldLabel, 'name':self.name }
        return simplejson.dumps(d)


def test():
    f = ExtForm()
    f.add_zone(Zone( 'Nom' ))
    f.add_zone(Zone( 'prenom', fieldLabel="Prenom" ))
    f.add_zone(Zone( 'description', fieldLabel="Commentaire" ))
    print f.render()


if __name__ == "__main__":
    test()
