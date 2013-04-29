from django.utils import simplejson
from collections import OrderedDict

class ExtGrid(object):
    def __init__(self):
        self.titre = "TITRE A CHANGER"
        self.width = 800
        self.height = 400
        self.renderTo = 'Ext.getBody()'
        self.champs = []
        self.data = []

    def add_champ(self, champ):
        self.champs.append(champ)

    def liste_champ_name(self):
        return [ c.name for c in self.champs ]

    def render(self):
        scripts = ''
        ## Le debut et la fin
        ENTETE = "Ext.onReady(function(){ "
        FIN = """
        });
        """
        ## definition du model
        model = """
        Ext.define('GModel', {
        extend: 'Ext.data.Model',
        fields:%s
        });
        """
        ## Attention l'ordre des champs a de l'importance
        scripts += model % simplejson.dumps(self.liste_champ_name())
        ## Definition du store
        store = """
        var GStore = Ext.create('Ext.data.Store', {
        model: GModel,
        data: %s
        });
        """
        scripts += store % simplejson.dumps(self.data)
        ## Definition de la grille
        grid_debut = """
        Ext.create('Ext.grid.Panel', {
        """
        grid_debut += "renderTo: %s," % self.renderTo
        grid_debut += "store: GStore,"
        grid_debut += "width: %s," % self.width
        grid_debut += "height: %s," % self.height
        grid_debut += "title: '%s'," % self.titre
        grid_debut += "columns:["
        grid_fin = " ]});"
        scripts += grid_debut
        cols = [ c.to_grid() for c in self.champs ]
        scripts += ','.join(cols)
        scripts += grid_fin

        return ENTETE+scripts+FIN


class Champ(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.text = kwargs.get('text', 'Champ %s ' % name )
        self.dataIndex = kwargs.get('dataIndex', name)
        self.width = kwargs.get('width',100)
        self.hidden = kwargs.get('hidden', False)
        self.hideable = kwargs.get('hideable', True)

    def to_grid(self):
        return simplejson.dumps(self.__dict__)

#def ext_grid( champs, titre="LISTE", data=[] ):
#    scripts = ''
#    ## Le debut et la fin
#    ENTETE = "Ext.onReady(function(){ "
#    FIN = """
#    });
#    """
#    ## definition du model
#    model = """
#    Ext.define('GModel', {
#    extend: 'Ext.data.Model',
#    fields:%s
#    });
#    """
#    scripts += model % simplejson.dumps(champs.keys())
#    ## Definition du store
#    store = """
#    var GStore = Ext.create('Ext.data.Store', {
#    model: GModel,
#    data: %s
#    });
#    """
#    scripts += store % simplejson.dumps(data)
#    ## Definition de la grille
#    grid_debut = """
#    Ext.create('Ext.grid.Panel', {
#        renderTo: Ext.getBody(),
#        store: GStore,
#        width: 400,
#        height: 200,
#        title: '%s',
#        columns:[
#    """
#    grid_fin = " ]});"
#    scripts += grid_debut % titre
#    cols = [ simplejson.dumps(c) for c in champs.values() ]
#    scripts += ','.join(cols)
#    scripts += grid_fin
#
#    return ENTETE+scripts+FIN
#

def tchamp():
    a = Champ( 'toto' )
    print a.to_grid()

def test():
    champ = OrderedDict()
    champ['name'] = dict(
        text='Nom',
        dataIndex='name',
        width=100,
        hideable=False,
    )
    champ['email'] = dict(
        text='Email',
        dataIndex='email',
        width=150,
        hidden=True
    )
    champ['phone'] = dict(
        text='Telephone',
        dataIndex='phone',
        width=100,
    )
    champ['zipcode'] = dict(
        text='ZipCode',
        dataIndex='zipcode',
        width=50,
    )

    ## Pour Test
    data = [
        { 'name': 'Lisa', 'email': 'lisa@simpsons.com', 'phone': '555-111-1224' , 'zipcode':"010101" },
        { 'name': 'Bart', 'email': 'bart@simpsons.com', 'phone': '555-222-1234' , 'zipcode':"010101" },
        { 'name': 'Homer', 'email': 'home@simpsons.com', 'phone': '555-222-1244' , 'zipcode':"010101" },
        { 'name': 'Marge', 'email': 'marge@simpsons.com', 'phone': '555-222-1254' , 'zipcode':"010101" }
    ]

    S =  ext_grid( champ , titre="Liste des contacts", data=data )
    print S

def test2():
    g = ExtGrid()
    g.add_champ( Champ('name') )
    g.add_champ( Champ('email') )
    g.add_champ( Champ('phone') )
    g.add_champ( Champ('zipcode') )
    g.titre = "Nouvelle Grille Auto"

    ## Pour Test
    g.data = [
        { 'name': 'Lisa', 'email': 'lisa@simpsons.com', 'phone': '555-111-1224' , 'zipcode':"010101" },
        { 'name': 'Bart', 'email': 'bart@simpsons.com', 'phone': '555-222-1234' , 'zipcode':"010101" },
        { 'name': 'Homer', 'email': 'home@simpsons.com', 'phone': '555-222-1244' , 'zipcode':"010101" },
        { 'name': 'Marge', 'email': 'marge@simpsons.com', 'phone': '555-222-1254' , 'zipcode':"010101" }
    ]
    print g.render()


if __name__ == '__main__':
    #tchamp()
    #test()
    test2()
