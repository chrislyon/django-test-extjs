from django.utils import simplejson
from collections import OrderedDict

def ext_grid( champs, titre="LISTE", data=[] ):
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
    scripts += model % simplejson.dumps(champs.keys())
    ## Definition du store
    store = """
    var GStore = Ext.create('Ext.data.Store', {
    model: GModel,
    data: %s
    });
    """
    scripts += store % simplejson.dumps(data)
    ## Definition de la grille
    grid_debut = """
    Ext.create('Ext.grid.Panel', {
        renderTo: Ext.getBody(),
        store: GStore,
        width: 400,
        height: 200,
        title: '%s',
        columns:[
    """
    grid_fin = " ]});"
    scripts += grid_debut % titre
    cols = [ simplejson.dumps(c) for c in champs.values() ]
    scripts += ','.join(cols)
    scripts += grid_fin

    return ENTETE+scripts+FIN

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

if __name__ == '__main__':
    test()
